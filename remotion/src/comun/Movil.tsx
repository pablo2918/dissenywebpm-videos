import React from "react";
import { Img, staticFile } from "remotion";

/** Movil con una captura de web dentro. `scroll` en px CSS de la web; `anchoCss` = ancho de la web. */
export const Movil: React.FC<{
  src: string; ancho: number; anchoCss: number; scroll?: number; style?: React.CSSProperties; children?: React.ReactNode; gris?: number; fondo?: string;
}> = ({ src, ancho, anchoCss, scroll = 0, style, children, gris = 0, fondo = "#fff" }) => {
  const borde = ancho * 0.035;
  const pant = ancho - 2 * borde;
  const alto = ancho * 2.05;
  const k = pant / anchoCss; // px de video por px CSS de la web
  return (
    <div
      style={{
        position: "absolute", width: ancho, height: alto, borderRadius: ancho * 0.13, background: "#0b0b0e",
        boxShadow: "0 40px 90px rgba(0,0,0,.55), inset 0 0 0 3px #2c2f38", ...style,
      }}
    >
      <div style={{ position: "absolute", left: borde, top: borde, width: pant, height: alto - 2 * borde, borderRadius: ancho * 0.1, overflow: "hidden", background: fondo }}>
        <Img src={staticFile(src)} style={{ width: pant, position: "absolute", left: 0, top: -scroll * k, filter: gris ? `grayscale(${gris}) brightness(${1 - 0.35 * gris})` : undefined }} />
        <div style={{ position: "absolute", left: 0, top: -scroll * k, width: pant }}>
          {/* capa para marcar cosas en coordenadas CSS de la web */}
          <div style={{ position: "absolute", left: 0, top: 0, width: anchoCss, scale: `${k}`, transformOrigin: "0 0" }}>{children}</div>
        </div>
      </div>
      <div style={{ position: "absolute", left: "50%", top: borde + ancho * 0.025, width: ancho * 0.26, height: ancho * 0.065, marginLeft: -ancho * 0.13, borderRadius: 99, background: "#0b0b0e" }} />
    </div>
  );
};
