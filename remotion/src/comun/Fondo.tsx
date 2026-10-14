import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { AZUL, AZUL2 } from "./marca";

/** Fondo azul de marca con un brillo que se mueve despacio (que nunca este quieto). */
export const Fondo: React.FC<{ tono?: string }> = ({ tono = "rgba(251,190,1,.10)" }) => {
  const f = useCurrentFrame();
  const x = 50 + 25 * Math.sin(f / 70);
  const y = 35 + 15 * Math.cos(f / 90);
  return (
    <AbsoluteFill style={{ background: `radial-gradient(circle at ${x}% ${y}%, ${tono}, transparent 45%), linear-gradient(160deg, ${AZUL2}, ${AZUL} 60%)` }}>
      <AbsoluteFill style={{ backgroundImage: "radial-gradient(rgba(255,255,255,.06) 2px, transparent 2px)", backgroundSize: "44px 44px", translate: `0 ${-(f * 0.6) % 44}px` }} />
    </AbsoluteFill>
  );
};
