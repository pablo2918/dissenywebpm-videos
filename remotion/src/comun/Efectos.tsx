import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from "remotion";
import { BLANCO, FUENTE, ROJO, VERDE } from "./marca";

/** Recuadro de color alrededor de algo (oscurece el resto). Coordenadas del contenedor. */
export const Marco: React.FC<{ caja: [number, number, number, number]; color: string; desde: number }> = ({ caja, color, desde }) => {
  const f = useCurrentFrame();
  const a = interpolate(f, [desde, desde + 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const [x, y, w, h] = caja;
  return (
    <div style={{ position: "absolute", left: x - 8, top: y - 8, width: w + 16, height: h + 16, border: `6px solid ${color}`, borderRadius: 14, opacity: a, scale: `${0.9 + 0.1 * a}`, boxShadow: `0 0 0 9999px rgba(0,0,0,${0.35 * a})` }} />
  );
};

export /** Dedo que toca: circulo que se encoge + onda. */
const Toque: React.FC<{ x: number; y: number }> = ({ x, y }) => {
  const f = useCurrentFrame();
  const onda = interpolate(f, [4, 20], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const dedo = interpolate(f, [0, 4, 9, 18], [0, 1, 0.8, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <>
      <div style={{ position: "absolute", left: x - 60, top: y - 60, width: 120, height: 120, borderRadius: 99, background: "rgba(255,255,255,.55)", border: "5px solid #fff", opacity: dedo, scale: `${1.3 - 0.3 * dedo}` }} />
      <div style={{ position: "absolute", left: x - 140, top: y - 140, width: 280, height: 280, borderRadius: 999, border: "8px solid #fff", opacity: 1 - onda, scale: `${0.3 + onda}` }} />
    </>
  );
};

/** Entrada de escena: zoom + desenfoque cortos (como un corte con golpe). */
export const Entrada: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill
      style={{
        scale: interpolate(f, [0, 8], [1.12, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) }),
        opacity: interpolate(f, [0, 4], [0, 1], { extrapolateRight: "clamp" }),
        filter: `blur(${interpolate(f, [0, 6], [14, 0], { extrapolateRight: "clamp" })}px)`,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

/** Sello redondo de bien (verde) o mal (rojo). */
export const Sello: React.FC<{ bien: boolean; x: number; y: number }> = ({ bien, x, y }) => {
  const f = useCurrentFrame();
  const k = interpolate(f, [0, 8], [2.2, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(2)) });
  return (
    <div style={{ position: "absolute", left: x - 110, top: y - 110, width: 220, height: 220, borderRadius: 999, background: bien ? VERDE : ROJO, color: BLANCO, fontFamily: FUENTE, fontWeight: 900, fontSize: 150, display: "flex", alignItems: "center", justifyContent: "center", scale: `${k}`, opacity: interpolate(f, [0, 3], [0, 1], { extrapolateRight: "clamp" }), boxShadow: "0 20px 50px rgba(0,0,0,.5)", border: "10px solid #fff" }}>
      {bien ? "✓" : "✗"}
    </div>
  );
};

