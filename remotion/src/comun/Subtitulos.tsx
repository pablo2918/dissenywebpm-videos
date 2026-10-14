import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { AMARILLO, BLANCO, FUENTE } from "./marca";
import { Palabra } from "./tipos";

type Trozo = { ini: number; fin: number; ps: Palabra[] };

/** Agrupa en trozos de 1–3 palabras; corta en puntuacion. */
export const trocea = (ps: Palabra[], max = 3): Trozo[] => {
  const out: Trozo[] = [];
  let cur: Palabra[] = [];
  const cierra = () => {
    if (cur.length) out.push({ ini: cur[0].inicio, fin: cur[cur.length - 1].fin, ps: cur });
    cur = [];
  };
  ps.forEach((p, i) => {
    const largo = cur.map((x) => x.texto).join(" ").length;
    // si esta palabra no cabe en la linea, cierra antes (nada de palabras sueltas abajo)
    if (cur.length && (cur.length >= max || largo + 1 + p.texto.length > 15)) cierra();
    cur.push(p);
    const sig = ps[i + 1];
    if (/[.,:;?!…»]$/.test(p.texto) || !sig || sig.tramo !== p.tramo) cierra();
  });
  // cada trozo dura hasta que empieza el siguiente (si es de la misma frase)
  out.forEach((t, i) => {
    const s = out[i + 1];
    t.fin = s && s.ps[0].tramo === t.ps[0].tramo ? s.ini : t.fin + 0.3;
  });
  return out;
};

export const Subtitulos: React.FC<{ palabras: Palabra[]; y?: number; tam?: number }> = ({ palabras, y = 1180, tam = 88 }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  const trozos = React.useMemo(() => trocea(palabras), [palabras]);
  const tr = trozos.find((x) => x.ini <= t && t < x.fin);
  if (!tr) return null;
  const desde = Math.round(tr.ini * fps);
  return (
    <div
      style={{
        position: "absolute", left: 60, right: 60, top: y, display: "flex", justifyContent: "center", flexWrap: "wrap",
        gap: "0 22px", fontFamily: FUENTE, fontWeight: 900, fontSize: tam, lineHeight: 1.08, textAlign: "center",
        scale: interpolate(f, [desde, desde + 4], [0.82, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
      }}
    >
      {tr.ps.map((p, i) => (
        <span
          key={i}
          style={{
            color: p.inicio <= t ? (p === tr.ps.filter((x) => x.inicio <= t).slice(-1)[0] ? AMARILLO : BLANCO) : BLANCO,
            WebkitTextStroke: `${tam * 0.16}px #000`, paintOrder: "stroke fill",
            textShadow: "0 8px 0 rgba(0,0,0,.55)", textTransform: "uppercase",
          }}
        >
          {p.texto.replace(/[«»"“”]/g, "")}
        </span>
      ))}
    </div>
  );
};
