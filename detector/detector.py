#!/usr/bin/env python3
"""Sybil Sweep — offline sybil farm detector (stdlib only).

Reads ClaimEvent lists (CSV or built-in demo), links wallets via shared-funder
and funding-burst signals, clusters with union-find, scores risk, and emits:
  - dashboard/graph_data.js
  - data/attestations.json

Usage:
  python3 detector/detector.py
  python3 detector/detector.py --csv data/test_wallets.csv
  python3 detector/detector.py --demo
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Tunables — adjust with Murtuza
BURST_SECONDS = 120
AMOUNT_TOL_BPS = 50  # 0.50% relative
GAS_TOL_BPS = 100  # 1.00% relative
MIN_CLUSTER_SIZE = 3
SYBIL_RISK_FLOOR = 55  # below this → treat as blue/unclustered for graph

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"
DATA_DIR = ROOT / "data"
DEFAULT_CSV = DATA_DIR / "test_wallets.csv"

# Human CSV units → int scale used by linking heuristics
AMOUNT_SCALE = 10**15
GAS_SCALE = 10**9

ZERO = "0x" + "0" * 40


@dataclass
class ClaimEvent:
    wallet: str
    funder: str
    funded_ts: int
    claim_ts: int
    amount: int
    gas_price: int
    is_farm: bool = False  # ground truth for demo metrics only


class UnionFind:
    def __init__(self, items: List[str]) -> None:
        self.parent = {x: x for x in items}
        self.rank = {x: 0 for x in items}

    def find(self, x: str) -> str:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1


def _addr(seed: str) -> str:
    h = hashlib.sha256(seed.encode()).hexdigest()
    return "0x" + h[:40]


def make_demo_dataset(seed: int = 42) -> List[ClaimEvent]:
    """Synthetic claimants with farms + hard cases (not 100% clean)."""
    rng = random.Random(seed)
    now = int(time.time())
    events: List[ClaimEvent] = []

    # --- Farm A: classic shared-funder burst (large) ---
    funder_a = _addr("funder-a")
    t0 = now - 3600
    for i in range(28):
        events.append(
            ClaimEvent(
                wallet=_addr(f"farm-a-{i}"),
                funder=funder_a,
                funded_ts=t0 + rng.randint(0, 45),
                claim_ts=t0 + 600 + rng.randint(0, 120),
                amount=10**16,  # 0.01 ETH-ish
                gas_price=50_000_000_000,
                is_farm=True,
            )
        )

    # --- Farm B: burst + identical amount/gas, mixed funders linked by burst ---
    funder_b1 = _addr("funder-b1")
    funder_b2 = _addr("funder-b2")
    t1 = now - 7200
    for i in range(12):
        events.append(
            ClaimEvent(
                wallet=_addr(f"farm-b-{i}"),
                funder=funder_b1 if i < 7 else funder_b2,
                funded_ts=t1 + rng.randint(0, 30),
                claim_ts=t1 + 400 + rng.randint(0, 90),
                amount=25 * 10**14,
                gas_price=42_000_000_000,
                is_farm=True,
            )
        )

    # --- Farm C: small noisy ring → amber "suspect", not high-conf attest ---
    funder_c = _addr("funder-c")
    t2 = now - 10_000
    for i in range(4):
        events.append(
            ClaimEvent(
                wallet=_addr(f"farm-c-{i}"),
                funder=funder_c,
                funded_ts=t2 + i * 900,  # staggered — weak burst
                claim_ts=t2 + 800 + i * 600,
                amount=(5 + i * 3) * 10**15,  # varied amounts
                gas_price=(40 + i * 8) * 10**9,
                is_farm=True,
            )
        )

    # --- Soft FN: 2 farm wallets funded separately (looks more like humans) ---
    for i in range(2):
        events.append(
            ClaimEvent(
                wallet=_addr(f"farm-miss-{i}"),
                funder=_addr(f"funder-miss-{i}"),
                funded_ts=now - 50_000 - i * 10_000,
                claim_ts=now - 40_000 - i * 8_000,
                amount=(15 + i * 7) * 10**15,
                gas_price=(33 + i * 11) * 10**9,
                is_farm=True,
            )
        )

    # --- Honest power-user who funds friends (must stay blue) ---
    whale = _addr("honest-whale")
    for i in range(5):
        events.append(
            ClaimEvent(
                wallet=_addr(f"friend-{i}"),
                funder=whale,
                funded_ts=now - 86_400 * (i + 1) + rng.randint(0, 3600),
                claim_ts=now - 86_400 * (i + 1) + 10_000,
                amount=rng.randint(3, 40) * 10**15,
                gas_price=rng.randint(20, 80) * 10**9,
                is_farm=False,
            )
        )

    # --- Independent honest claimants ---
    for i in range(40):
        events.append(
            ClaimEvent(
                wallet=_addr(f"honest-{i}"),
                funder=_addr(f"honest-funder-{i}"),
                funded_ts=now - rng.randint(3_600, 500_000),
                claim_ts=now - rng.randint(600, 3_000),
                amount=rng.randint(1, 50) * 10**15,
                gas_price=rng.randint(15, 90) * 10**9,
                is_farm=False,
            )
        )

    # One decoy: two honest wallets funded close in time with different amounts
    # (should NOT link via rule B)
    events.append(
        ClaimEvent(
            wallet=_addr("decoy-1"),
            funder=_addr("decoy-f1"),
            funded_ts=now - 2000,
            claim_ts=now - 1000,
            amount=11 * 10**15,
            gas_price=30_000_000_000,
            is_farm=False,
        )
    )
    events.append(
        ClaimEvent(
            wallet=_addr("decoy-2"),
            funder=_addr("decoy-f2"),
            funded_ts=now - 1980,
            claim_ts=now - 900,
            amount=37 * 10**15,
            gas_price=70_000_000_000,
            is_farm=False,
        )
    )

    rng.shuffle(events)
    return events


def _parse_ts(value: str) -> int:
    value = value.strip()
    if value.isdigit():
        return int(value)
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return int(datetime.strptime(value, fmt).timestamp())
        except ValueError:
            continue
    raise ValueError(f"unrecognized timestamp: {value!r}")


def load_csv(path: Path) -> List[ClaimEvent]:
    """Load Murtuza/Esa test_wallets.csv (human amounts/gas scaled internally)."""
    events: List[ClaimEvent] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"wallet_address", "funder", "amount"}
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise SystemExit(
                f"{path}: need columns wallet_address,funder,amount "
                f"(plus funded_time/claim_time or claim_time)"
            )
        for row in reader:
            funded_raw = row.get("funded_time") or row.get("funded_ts") or row.get("claim_time")
            claim_raw = row.get("claim_time") or row.get("claim_ts") or funded_raw
            if not funded_raw or not claim_raw:
                raise SystemExit(f"{path}: row missing funded_time/claim_time: {row}")
            gas_raw = row.get("gas_price") or "50"
            farm_raw = (row.get("is_farm") or "0").strip().lower()
            events.append(
                ClaimEvent(
                    wallet=row["wallet_address"].strip().lower(),
                    funder=row["funder"].strip().lower(),
                    funded_ts=_parse_ts(funded_raw),
                    claim_ts=_parse_ts(claim_raw),
                    amount=int(float(row["amount"])) * AMOUNT_SCALE,
                    gas_price=int(float(gas_raw)) * GAS_SCALE,
                    is_farm=farm_raw in ("1", "true", "yes", "y"),
                )
            )
    if not events:
        raise SystemExit(f"{path}: no rows")
    return events


def _near(a: int, b: int, tol_bps: int) -> bool:
    if a == 0 and b == 0:
        return True
    base = max(a, b, 1)
    return abs(a - b) * 10_000 // base <= tol_bps


def link_pairs(events: List[ClaimEvent]) -> List[Tuple[str, str, str]]:
    """Return (wallet_a, wallet_b, reason) edges to union."""
    by_wallet = {e.wallet: e for e in events}
    wallets = list(by_wallet)
    uf_edges: List[Tuple[str, str, str]] = []

    # Rule A: shared funder
    by_funder: Dict[str, List[str]] = defaultdict(list)
    for e in events:
        by_funder[e.funder].append(e.wallet)
    for funder, members in by_funder.items():
        if len(members) < 2:
            continue
        # Skip "honest whale funds friends over days" via burst filter later for scoring;
        # still link shared funder — scoring + min size / window will demote friend group.
        anchor = members[0]
        for other in members[1:]:
            uf_edges.append((anchor, other, "shared_funder"))

    # Rule B: funding burst + near-identical amount + gas
    ordered = sorted(events, key=lambda e: e.funded_ts)
    for i, a in enumerate(ordered):
        for b in ordered[i + 1 :]:
            if b.funded_ts - a.funded_ts > BURST_SECONDS:
                break
            if a.wallet == b.wallet:
                continue
            if _near(a.amount, b.amount, AMOUNT_TOL_BPS) and _near(
                a.gas_price, b.gas_price, GAS_TOL_BPS
            ):
                uf_edges.append((a.wallet, b.wallet, "burst_amount_gas"))

    return uf_edges


def score_cluster(members: List[str], by_wallet: Dict[str, ClaimEvent]) -> dict:
    evs = [by_wallet[w] for w in members]
    funders = {e.funder for e in evs}
    funded_ts = [e.funded_ts for e in evs]
    window = max(funded_ts) - min(funded_ts)
    amounts = [e.amount for e in evs]
    gases = [e.gas_price for e in evs]

    # Heuristic risk 0..100
    risk = 20
    if len(funders) == 1:
        risk += 35
    elif len(funders) == 2 and len(members) >= 8:
        risk += 20  # possible multi-funder farm
    if window <= BURST_SECONDS:
        risk += 25
    elif window <= BURST_SECONDS * 5:
        risk += 10
    if len(members) >= 20:
        risk += 15
    elif len(members) >= 8:
        risk += 10
    elif len(members) >= MIN_CLUSTER_SIZE:
        risk += 5

    # Amount / gas homogeneity
    if amounts:
        mean_a = sum(amounts) / len(amounts)
        if mean_a and max(abs(x - mean_a) for x in amounts) / mean_a < 0.02:
            risk += 10
    if gases:
        mean_g = sum(gases) / len(gases)
        if mean_g and max(abs(x - mean_g) for x in gases) / mean_g < 0.05:
            risk += 5

    # Demote slow friend-funding pattern (honest whale)
    if len(funders) == 1 and window > 86_400 and len(members) <= 8:
        risk = min(risk, 40)

    # Small staggered rings with heterogeneous params → amber, not attest
    if len(members) <= 4 and window > BURST_SECONDS * 3:
        risk = min(risk, 52)

    risk = max(0, min(100, risk))
    funder = next(iter(funders)) if len(funders) == 1 else ZERO
    return {
        "risk": risk,
        "confidenceBps": risk * 100,
        "funder": funder,
        "fundingWindowSecs": int(window),
        "size": len(members),
    }


def evidence_hash(members: List[str], funder: str, window: int) -> str:
    payload = "|".join(sorted(m.lower() for m in members)) + f"|{funder.lower()}|{window}"
    return "0x" + hashlib.sha256(payload.encode()).hexdigest()


def detect(events: List[ClaimEvent]) -> dict:
    by_wallet = {e.wallet: e for e in events}
    wallets = list(by_wallet)
    uf = UnionFind(wallets)
    edge_reasons: Dict[Tuple[str, str], str] = {}

    for a, b, reason in link_pairs(events):
        uf.union(a, b)
        key = tuple(sorted((a, b)))
        edge_reasons[key] = reason

    groups: Dict[str, List[str]] = defaultdict(list)
    for w in wallets:
        groups[uf.find(w)].append(w)

    # Build scored clusters (size filter + risk floor for "red" farms)
    raw_clusters = []
    for members in groups.values():
        if len(members) < MIN_CLUSTER_SIZE:
            continue
        meta = score_cluster(members, by_wallet)
        raw_clusters.append((members, meta))

    # Sort largest / riskiest first for stable IDs
    raw_clusters.sort(key=lambda x: (-x[1]["risk"], -x[1]["size"]))

    nodes = []
    links = []
    attestations = []
    wallet_cluster: Dict[str, int] = {w: -1 for w in wallets}

    dashboard_id = 0
    for members, meta in raw_clusters:
        is_sybil_visual = meta["risk"] >= SYBIL_RISK_FLOOR
        cid = dashboard_id if is_sybil_visual else -1
        if is_sybil_visual:
            for w in members:
                wallet_cluster[w] = dashboard_id
            onchain_id = dashboard_id + 1
            eh = evidence_hash(members, meta["funder"], meta["fundingWindowSecs"])
            attestations.append(
                {
                    "clusterId": onchain_id,
                    "members": sorted(members),
                    "size": meta["size"],
                    "confidenceBps": meta["confidenceBps"],
                    "funder": meta["funder"],
                    "fundingWindowSecs": meta["fundingWindowSecs"],
                    "evidenceHash": eh,
                }
            )
            dashboard_id += 1
        else:
            # amber/suspect kept in cards via separate list below
            pass

        # Always emit cluster card info for borderline too
        members_sorted = sorted(members)
        for w in members_sorted:
            e = by_wallet[w]
            nodes.append(
                {
                    "id": w,
                    "cluster": wallet_cluster[w],
                    "funder": e.funder,
                    "risk": meta["risk"] if is_sybil_visual else meta["risk"],
                    "isFarmTruth": e.is_farm,
                    "suspect": (not is_sybil_visual) and meta["risk"] >= 45,
                }
            )

    # Unclustered singles / pairs
    clustered = {n["id"] for n in nodes}
    for w, e in by_wallet.items():
        if w in clustered:
            continue
        nodes.append(
            {
                "id": w,
                "cluster": -1,
                "funder": e.funder,
                "risk": 0,
                "isFarmTruth": e.is_farm,
                "suspect": False,
            }
        )

    # Links: funder→wallet for graph + intra-cluster edges
    seen_link = set()
    funder_nodes: Dict[str, dict] = {}
    for w, e in by_wallet.items():
        key = (e.funder, w)
        if key in seen_link:
            continue
        seen_link.add(key)
        links.append({"source": e.funder, "target": w, "kind": "funding"})
        if e.funder not in by_wallet and e.funder not in funder_nodes:
            funder_nodes[e.funder] = {
                "id": e.funder,
                "cluster": wallet_cluster.get(w, -1),
                "funder": ZERO,
                "risk": 0,
                "isFarmTruth": False,
                "suspect": False,
                "isFunder": True,
            }
    nodes.extend(funder_nodes.values())

    for (a, b), reason in edge_reasons.items():
        if wallet_cluster.get(a, -1) >= 0 and wallet_cluster[a] == wallet_cluster.get(b, -1):
            links.append({"source": a, "target": b, "kind": reason})

    # Metrics vs ground truth (red farms + amber suspects both count as caught)
    farm_wallets = {e.wallet for e in events if e.is_farm}
    flagged = {n["id"] for n in nodes if n["cluster"] >= 0 and not n.get("isFunder")}
    suspects = {n["id"] for n in nodes if n.get("suspect") and not n.get("isFunder")}
    caught = flagged | suspects
    tp = len(caught & farm_wallets)
    fp = len(caught - farm_wallets)
    fn = len(farm_wallets - caught)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0

    cluster_cards = []
    for att in attestations:
        cluster_cards.append(
            {
                "clusterId": att["clusterId"] - 1,
                "onchainClusterId": att["clusterId"],
                "size": att["size"],
                "confidenceBps": att["confidenceBps"],
                "funder": att["funder"],
                "fundingWindowSecs": att["fundingWindowSecs"],
                "evidenceHash": att["evidenceHash"],
                "sampleMember": att["members"][0] if att["members"] else "",
            }
        )

    return {
        "nodes": nodes,
        "links": links,
        "clusters": cluster_cards,
        "attestations": attestations,
        "metrics": {
            "claimants": len(events),
            "farms_truth": len(farm_wallets),
            "flagged": len(flagged),
            "suspects": len(suspects),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "tp": tp,
            "fp": fp,
            "fn": fn,
        },
    }


def write_outputs(result: dict) -> None:
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    graph = {
        "generatedAt": int(time.time()),
        "metrics": result["metrics"],
        "clusters": result["clusters"],
        "nodes": result["nodes"],
        "links": result["links"],
    }
    js_path = DASHBOARD_DIR / "graph_data.js"
    js_path.write_text(
        "window.SYBIL_GRAPH = " + json.dumps(graph, indent=2) + ";\n",
        encoding="utf-8",
    )

    att_path = DATA_DIR / "attestations.json"
    att_path.write_text(
        json.dumps(
            {
                "generatedAt": graph["generatedAt"],
                "thresholdBpsDefault": 7000,
                "attestations": result["attestations"],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {js_path.relative_to(ROOT)} and {att_path.relative_to(ROOT)}")


def main(argv: Optional[List[str]] = None) -> None:
    ap = argparse.ArgumentParser(description="Sybil Sweep detector")
    ap.add_argument(
        "--csv",
        type=Path,
        default=None,
        help="Claimant CSV (default: data/test_wallets.csv if present)",
    )
    ap.add_argument(
        "--demo",
        action="store_true",
        help="Force built-in synthetic demo dataset (ignore CSV)",
    )
    args = ap.parse_args(argv)

    if args.demo:
        events = make_demo_dataset()
        print("Source: built-in demo dataset")
    else:
        csv_path = args.csv or (DEFAULT_CSV if DEFAULT_CSV.exists() else None)
        if csv_path is not None:
            events = load_csv(csv_path)
            print(f"Source: {csv_path}")
        else:
            events = make_demo_dataset()
            print("Source: built-in demo dataset (no CSV found)")

    result = detect(events)
    write_outputs(result)
    m = result["metrics"]
    print(
        f"Claimants: {m['claimants']} | truth farms: {m['farms_truth']} | "
        f"flagged: {m['flagged']} | precision: {m['precision']:.1%} | "
        f"recall: {m['recall']:.1%}"
    )
    print(f"Attestations ready: {len(result['attestations'])} cluster(s)")


if __name__ == "__main__":
    main()
