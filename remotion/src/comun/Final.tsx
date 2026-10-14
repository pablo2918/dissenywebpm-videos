import React from "react";
import { Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { AMARILLO, AZUL, DOMINIO, FUENTE, GRIS, Idioma, TELEFONO, TXT } from "./marca";
import { Titulo } from "./Texto";

/** Cierre: logo, frase, boton de WhatsApp que late, telefono y web. */
export const Final: React.FC<{ frase: string; idioma: Idioma }> = ({ frase, idioma }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ent = (d: number) => ({
    opacity: interpolate(f, [d, d + 8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
    translate: interpolate(f, [d, d + 10], ["0px 60px", "0px 0px"], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) }),
  });
  const late = 1 + 0.04 * Math.max(0, Math.sin((f - 20) / (fps * 0.18)));
  return (
    <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 46, paddingBottom: 120 }}>
      <Img src={staticFile("marca/logo.png")} style={{ width: 300, ...ent(0) }} />
      <div style={{ ...ent(4), padding: "0 70px" }}>
        <Titulo texto={frase} tam={96} />
      </div>
      <div
        style={{
          ...ent(9), scale: `${late}`, background: AMARILLO, color: AZUL, fontFamily: FUENTE, fontWeight: 900, fontSize: 58,
          padding: "30px 60px", borderRadius: 99, boxShadow: "0 20px 50px rgba(251,190,1,.35)",
        }}
      >
        {TXT[idioma].cta}
      </div>
      <div style={{ ...ent(13), textAlign: "center", fontFamily: FUENTE }}>
        <div style={{ color: AMARILLO, fontWeight: 900, fontSize: 80 }}>{TELEFONO}</div>
        <div style={{ color: GRIS, fontWeight: 600, fontSize: 42, marginTop: 10 }}>{DOMINIO}</div>
      </div>
    </div>
  );
};
