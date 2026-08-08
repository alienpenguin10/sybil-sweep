import { useCallback, useEffect, useMemo, useState } from "react";
import type { Address } from "viem";
import { ForceGraph } from "./components/ForceGraph";
import { getAirdropAddress, getRegistryAddress } from "./lib/chain";
import { explorerAddressUrl, probeWallet } from "./lib/registry";
import type { GraphPayload } from "./lib/types";

function short(a?: string, head = 6, tail = 4) {
  if (!a) return "—";
  if (a.length <= head + tail + 1) return a;
  return `${a.slice(0, head)}…${a.slice(-tail)}`;
}

export default function App() {
  const [data, setData] = useState<GraphPayload | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [beat, setBeat] = useState(3);
  const [probeStatus, setProbeStatus] = useState<string>("Waiting for registry…");
  const [pill, setPill] = useState<"off" | "wait" | "live">("off");
  const [pillLabel, setPillLabel] = useState("pending deploy");

  const registry = getRegistryAddress();
  const airdrop = getAirdropAddress();

  useEffect(() => {
    const graphUrl = `${import.meta.env.BASE_URL}graph_data.json`;
    fetch(graphUrl)
      .then(async (r) => {
        if (!r.ok) throw new Error(`graph_data.json HTTP ${r.status}`);
        return r.json() as Promise<GraphPayload>;
      })
      .then(setData)
      .catch((e: Error) => {
        setLoadError(
          `${e.message}. Run: python3 detector/detector.py  (writes dashboard/public/graph_data.json)`
        );
      });
  }, []);

  const probeWalletAddr = useMemo(() => {
    if (!data?.clusters?.length) return null;
    const sample = data.clusters[0].sampleMember;
    if (sample?.startsWith("0x")) return sample as Address;
    const hit = data.nodes.find((n) => n.cluster === 0 && !n.isFunder);
    return (hit?.id as Address) || null;
  }, [data]);

  const refreshEnforce = useCallback(async () => {
    if (!registry) {
      setPill("wait");
      setPillLabel("pending deploy");
      setProbeStatus(
        `Off-chain verdict ready · ${(data?.clusters || []).length} cluster(s) in attestations.json. Set VITE_SYBIL_REGISTRY in dashboard/.env`
      );
      return;
    }
    if (!probeWalletAddr) {
      setPill("wait");
      setPillLabel("no probe wallet");
      setProbeStatus("No sampleMember in graph data.");
      return;
    }
    setPill("wait");
    setPillLabel("probing…");
    try {
      const res = await probeWallet(probeWalletAddr);
      setPill("live");
      setPillLabel("live on monad");
      setBeat(4);
      const thr = (res.thresholdBps / 100).toFixed(0);
      const label = res.isSybil ? "SYBIL · blocked" : "not flagged yet";
      setProbeStatus(
        `Probe ${short(probeWalletAddr)} → ${label} · risk ${(res.riskBps / 100).toFixed(1)}% · threshold ${thr}%`
      );
    } catch (e) {
      setPill("wait");
      setPillLabel("rpc offline");
      setProbeStatus(`Could not reach RPC via viem. ${(e as Error).message}`);
    }
  }, [registry, probeWalletAddr, data]);

  useEffect(() => {
    void refreshEnforce();
  }, [refreshEnforce]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key >= "1" && e.key <= "4") setBeat(Number(e.key));
      if (e.key === "r" || e.key === "R") void refreshEnforce();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [refreshEnforce]);

  if (loadError) {
    return (
      <div className="boot-error">
        <h1>Sybil Sweep</h1>
        <p>{loadError}</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="boot-error">
        <h1>Sybil Sweep</h1>
        <p>Loading graph_data.json…</p>
      </div>
    );
  }

  const m = data.metrics;
  const recallPct = `${(m.recall * 100).toFixed(1)}%`;
  const explorerHref = registry
    ? explorerAddressUrl(registry)
    : import.meta.env.VITE_EXPLORER_URL || "https://testnet.monadvision.com";

  return (
    <>
      <header>
        <div className="brand">
          <h1>
            Sybil <span>Sweep</span>
          </h1>
          <p className="tagline">
            Detect → show → <strong>enforce</strong> · React + viem
          </p>
        </div>
        <div className="beats">
          {[1, 2, 3, 4].map((b) => (
            <span
              key={b}
              className={`beat${beat === b ? " on" : ""}${b < beat ? " done" : ""}`}
            >
              {b === 1 ? "1 input" : b === 2 ? "2 detect" : b === 3 ? "3 show" : "4 enforce"}
            </span>
          ))}
        </div>
      </header>

      <div className="layout">
        <div className="stage-wrap">
          <div className="hud">
            {m.claimants} claimants
            <span className="sub">
              {m.flagged} farm wallets · {recallPct} recall
            </span>
          </div>
          <ForceGraph nodes={data.nodes} links={data.links} />
          <footer className="foot">
            <span>
              {data.nodes.length} nodes · {data.links.length} edges · viem → Monad {import.meta.env.VITE_CHAIN_ID || 10143}
            </span>
            <span>keys: 1–4 beats · R re-probe</span>
          </footer>
        </div>

        <aside>
          <div className="metrics">
            <div className="metric hero">
              <span>Recall</span>
              <b>{recallPct}</b>
            </div>
            <div className="metric">
              <span>Claimants</span>
              <b>{m.claimants}</b>
            </div>
            <div className="metric">
              <span>Flagged farms</span>
              <b>{m.flagged}</b>
            </div>
            <div className="metric">
              <span>Precision</span>
              <b>{(m.precision * 100).toFixed(1)}%</b>
            </div>
          </div>

          <div className="legend">
            <span>
              <i className="dot red" />
              farm
            </span>
            <span>
              <i className="dot blue" />
              human
            </span>
            <span>
              <i className="dot amber" />
              suspect
            </span>
          </div>

          <h2>Enforce on Monad</h2>
          <div className="enforce">
            <div className="status">
              <b>Registry</b>
              <span className={`pill ${pill}`}>{pillLabel}</span>
            </div>
            <div className="line">
              {registry ? (
                <>
                  Registry <b>{short(registry)}</b>
                  {airdrop ? (
                    <>
                      {" "}
                      · airdrop <b>{short(airdrop)}</b>
                    </>
                  ) : null}
                </>
              ) : (
                <>
                  Paste deploy address into <b>dashboard/.env</b> as{" "}
                  <b>VITE_SYBIL_REGISTRY</b>
                </>
              )}
            </div>
            <div className="probe">{probeStatus}</div>
            <div className="btnrow">
              <button type="button" onClick={() => void refreshEnforce()}>
                Re-probe (viem)
              </button>
              <a className="linkbtn" href={explorerHref} target="_blank" rel="noreferrer">
                Explorer
              </a>
              <a
                className="linkbtn"
                href={`${import.meta.env.BASE_URL}fallback.html`}
                target="_blank"
                rel="noreferrer"
              >
                HTML fallback
              </a>
            </div>
          </div>

          <h2>Clusters ready to attest</h2>
          {(data.clusters || []).map((c) => (
            <div className="card" key={c.onchainClusterId}>
              <strong>
                Cluster #{c.onchainClusterId} ·{" "}
                <span className="conf">{(c.confidenceBps / 100).toFixed(1)}%</span>
              </strong>
              <div className="row">
                {c.size} wallets · funding window {c.fundingWindowSecs}s
              </div>
              <div className="row">funder {short(c.funder)}</div>
              <div className="row">sample {short(c.sampleMember, 10, 6)}</div>
            </div>
          ))}
          {!data.clusters?.length && (
            <div className="row muted">No clusters above risk floor.</div>
          )}
        </aside>
      </div>
    </>
  );
}
