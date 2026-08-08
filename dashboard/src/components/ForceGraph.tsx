import { useEffect, useRef } from "react";
import type { GraphLink, GraphNode } from "../lib/types";

type Props = {
  nodes: GraphNode[];
  links: GraphLink[];
};

type SimNode = GraphNode & { x: number; y: number; vx: number; vy: number };

export function ForceGraph({ nodes, links }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const stageRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const stage = stageRef.current;
    if (!canvas || !stage) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const sim: SimNode[] = nodes.map((n, i) => ({
      ...n,
      x: Math.cos(i * 0.7) * 200 + 420,
      y: Math.sin(i * 1.3) * 160 + 300,
      vx: 0,
      vy: 0,
    }));
    const byId = Object.fromEntries(sim.map((n) => [n.id, n]));
    const edges = links
      .map((l) => ({ ...l, s: byId[l.source], t: byId[l.target] }))
      .filter((l) => l.s && l.t);

    let raf = 0;
    let alive = true;

    function tick() {
      const n = sim.length;
      for (let i = 0; i < n; i++) {
        for (let j = i + 1; j < n; j++) {
          const a = sim[i];
          const b = sim[j];
          let dx = a.x - b.x;
          let dy = a.y - b.y;
          let dist = Math.sqrt(dx * dx + dy * dy) || 0.01;
          let force = 420 / (dist * dist);
          if (a.cluster >= 0 && a.cluster === b.cluster) force *= 0.12;
          a.vx += (dx / dist) * force;
          a.vy += (dy / dist) * force;
          b.vx -= (dx / dist) * force;
          b.vy -= (dy / dist) * force;
        }
      }
      for (const l of edges) {
        let dx = l.t.x - l.s.x;
        let dy = l.t.y - l.s.y;
        let dist = Math.sqrt(dx * dx + dy * dy) || 0.01;
        const target = l.kind === "funding" ? 72 : 34;
        const f = (dist - target) * 0.012;
        l.s.vx += (dx / dist) * f;
        l.s.vy += (dy / dist) * f;
        l.t.vx -= (dx / dist) * f;
        l.t.vy -= (dy / dist) * f;
      }
      const dpr = window.devicePixelRatio || 1;
      const cx = canvas!.width / (2 * dpr);
      const cy = canvas!.height / (2 * dpr);
      for (const n of sim) {
        n.vx += (cx - n.x) * 0.0022;
        n.vy += (cy - n.y) * 0.0022;
        n.vx *= 0.86;
        n.vy *= 0.86;
        n.x += n.vx;
        n.y += n.vy;
      }
    }

    function color(n: SimNode) {
      if (n.suspect) return "#f59e0b";
      if (n.cluster >= 0) return "#ef4444";
      if (n.isFunder) return "#64748b";
      return "#3b82f6";
    }

    function draw() {
      if (!alive || !ctx || !canvas || !stage) return;
      const dpr = window.devicePixelRatio || 1;
      const w = stage.clientWidth;
      const h = stage.clientHeight;
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, w, h);
      for (let i = 0; i < 2; i++) tick();

      for (const l of edges) {
        const farm = l.s.cluster >= 0 && l.t.cluster >= 0;
        ctx.strokeStyle = farm ? "rgba(239,68,68,0.38)" : "rgba(59,130,246,0.12)";
        ctx.lineWidth = farm ? 1.25 : 1;
        ctx.beginPath();
        ctx.moveTo(l.s.x, l.s.y);
        ctx.lineTo(l.t.x, l.t.y);
        ctx.stroke();
      }
      for (const n of sim) {
        const r = n.isFunder ? 3.2 : n.cluster >= 0 ? 5.8 : 4;
        ctx.beginPath();
        ctx.fillStyle = color(n);
        ctx.globalAlpha = n.isFunder ? 0.5 : 0.95;
        ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
      }
      raf = requestAnimationFrame(draw);
    }

    draw();
    return () => {
      alive = false;
      cancelAnimationFrame(raf);
    };
  }, [nodes, links]);

  return (
    <div className="stage" ref={stageRef}>
      <canvas ref={canvasRef} />
    </div>
  );
}
