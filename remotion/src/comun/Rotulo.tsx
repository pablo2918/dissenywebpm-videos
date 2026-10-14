import React from "react";
import { Easing, interpolate, Sequence, useCurrentFrame, useVideoConfig } from "remotion";
import { Sfx } from "./Sfx";
import { AMARILLO, AZUL, BLANCO, COLORES, FUENTE } from "./marca";

/** Rotulo grande arriba (la palabra clave que se esta diciendo), con «pop». */
export const Rotulo: React.FC<{ texto: string; color?: string; y?: number; tam?: number; giro?: number }> = ({
  texto, color = "amarillo", y = 170, tam = 92, giro = -3,
}) => {
  const f = useCurrentFrame();
  const fondo = COLORES[color] ?? AMARILLO;
  const tinta = color === "amarillo" || color === "blanco" ? AZUL : BLANCO;
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: y, display: "flex", justifyContent: "center" }}>
      <div
        style={{
          fontFamily: FUENTE, fontWeight: 900, fontSize: tam, color: tinta, background: fondo, padding: "14px 40px 18px",
          borderRadius: 26, boxShadow: "0 18px 40px rgba(0,0,0,.45)", maxWidth: 960, textAlign: "center", lineHeight: 1.05,
          scale: interpolate(f, [0, 7], [0.2, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(2.2)) }),
          rotate: `${giro}deg`,
        }}
      >
        {texto}
      </div>
    </div>
  );
};

/** Pinta los rotulos de una lista, cada uno desde su momento hasta el siguiente, con su «pop». */
export const Rotulos: React.FC<{ lista: { t: number; texto: string; color?: string }[]; hasta: number; y?: number }> = ({ lista, hasta, y }) => {
  const { fps } = useVideoConfig();
  return (
    <>
      {lista.map((r, i) => {
        const fin = i + 1 < lista.length ? lista[i + 1].t : hasta;
        return (
          <Sequence key={i} from={Math.round(r.t * fps)} durationInFrames={Math.max(1, Math.round((fin - r.t) * fps))} layout="none">
            <Rotulo texto={r.texto} color={r.color} y={y} giro={i % 2 ? 3 : -3} />
            <Sfx nombre="pop" volumen={0.55} />
          </Sequence>
        );
      })}
    </>
  );
};
