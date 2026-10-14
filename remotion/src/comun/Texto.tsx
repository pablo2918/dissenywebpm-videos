import React from "react";
import { AMARILLO, AZUL, BLANCO, FUENTE } from "./marca";

/** Titulo con *resaltado* en amarillo (como en los carruseles). */
export const Titulo: React.FC<{ texto: string; tam?: number; color?: string; style?: React.CSSProperties }> = ({ texto, tam = 110, color = BLANCO, style }) => (
  <div style={{ fontFamily: FUENTE, fontWeight: 900, fontSize: tam, lineHeight: 1.04, color, textAlign: "center", letterSpacing: -1, ...style }}>
    {texto.split(/(\*[^*]+\*)/).map((t, i) =>
      t.startsWith("*") ? (
        <span key={i} style={{ background: AMARILLO, color: AZUL, padding: "0 14px", borderRadius: 14, boxDecorationBreak: "clone", WebkitBoxDecorationBreak: "clone" }}>
          {t.slice(1, -1)}
        </span>
      ) : (
        <span key={i}>{t}</span>
      ),
    )}
  </div>
);
