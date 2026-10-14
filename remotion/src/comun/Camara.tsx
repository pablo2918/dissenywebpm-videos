import React from "react";
import { Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

/** Punto de camara: en el segundo `t` (local de la escena), el punto (x, y) del
 *  lienzo queda en el centro de la pantalla con zoom `s`. */
export type Toma = { t: number; x: number; y: number; s: number };

const CX = 540;
const CY = 960;

/** Mueve y amplia lo que tiene dentro como una camara (zoom suave entre tomas). */
export const Camara: React.FC<{ tomas: Toma[]; dur?: number; children: React.ReactNode }> = ({ tomas, dur = 0.55, children }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  let x = tomas[0].x;
  let y = tomas[0].y;
  let s = tomas[0].s;
  for (let i = 1; i < tomas.length; i++) {
    const a = tomas[i - 1];
    const b = tomas[i];
    const k = interpolate(t, [b.t, b.t + dur], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
    if (t >= b.t) {
      x = a.x + (b.x - a.x) * k;
      y = a.y + (b.y - a.y) * k;
      s = a.s + (b.s - a.s) * k;
    }
  }
  // deriva muy lenta para que la imagen nunca este quieta
  const deriva = 1 + 0.012 * Math.sin(t * 0.9);
  return (
    <div style={{ position: "absolute", inset: 0, transformOrigin: "0 0", transform: `translate(${CX - x * s * deriva}px, ${CY - y * s * deriva}px) scale(${s * deriva})` }}>
      {children}
    </div>
  );
};
