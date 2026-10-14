import React from "react";
import { AbsoluteFill, Easing, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { Sfx } from "./comun/Sfx";
import { Fondo } from "./comun/Fondo";
import { Subtitulos } from "./comun/Subtitulos";
import { Rotulos } from "./comun/Rotulo";
import { Final } from "./comun/Final";
import { Entrada, Sello } from "./comun/Efectos";
import { AMARILLO, AZUL, BLANCO, FUENTE, ROJO } from "./comun/marca";
import { cuando, Datos, Escena } from "./comun/tipos";

/* «Pregunta de cliente»: la pregunta va en un rotulo rojo arriba todo el video
   (se entiende sin sonido) y la respuesta se dibuja en el centro. */

const GRIS_T = "#5f6368";
const AZUL_G = "#1a73e8";
const local = (e: Escena, w: string) => cuando(e, w) - e.inicio;
const sale = (f: number, d: number, k = 8) => ({
  opacity: interpolate(f, [d, d + k * 0.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
  translate: interpolate(f, [d, d + k], ["0px 50px", "0px 0px"], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(1.4)) }),
});

const Caja: React.FC<{ texto: string }> = ({ texto }) => {
  const f = useCurrentFrame();
  return (
    <div style={{ position: "absolute", left: 60, right: 60, top: 80, display: "flex", justifyContent: "center", rotate: `${0.6 * Math.sin(f / 25)}deg` }}>
      <div style={{ background: ROJO, color: BLANCO, fontFamily: FUENTE, fontWeight: 900, fontSize: 56, lineHeight: 1.08, padding: "22px 36px 26px", borderRadius: 22, textAlign: "center", border: "6px solid #fff", boxShadow: "0 20px 50px rgba(0,0,0,.45)" }}>
        «{texto}»
      </div>
    </div>
  );
};

const Estrellas: React.FC<{ n?: number; tam?: number; llenas?: number }> = ({ n = 5, tam = 30, llenas = 5 }) => (
  <span style={{ fontSize: tam, letterSpacing: 2 }}>
    {Array.from({ length: n }, (_, i) => (
      <span key={i} style={{ color: i < llenas ? "#fbbc04" : "#dadce0" }}>★</span>
    ))}
  </span>
);

const Pin: React.FC<{ x: number; y: number; color?: string; k?: number }> = ({ x, y, color = "#ea4335", k = 1 }) => (
  <div style={{ position: "absolute", left: x - 22, top: y - 44, width: 44, height: 44, background: color, borderRadius: "50% 50% 50% 0", rotate: "-45deg", scale: `${k}`, boxShadow: "0 4px 10px rgba(0,0,0,.3)", border: "4px solid #fff" }} />
);

const MapaFondo: React.FC<{ alto: number }> = ({ alto }) => (
  <div style={{ position: "relative", height: alto, background: "#e8eaed", overflow: "hidden" }}>
    <div style={{ position: "absolute", inset: 0, background: "repeating-linear-gradient(35deg,transparent 0 70px,#fff 70px 84px),repeating-linear-gradient(-55deg,transparent 0 110px,#fff 110px 122px)" }} />
    <div style={{ position: "absolute", left: "8%", top: "20%", width: 160, height: 110, background: "#c8e6c9", borderRadius: 20 }} />
    <div style={{ position: "absolute", right: "12%", bottom: "8%", width: 220, height: 90, background: "#aecbfa", borderRadius: 30 }} />
  </div>
);

const NEGOCIOS = [
  { n: "Peluquería Alba", e: 5 },
  { n: "Salón Lucía", e: 5 },
  { n: "Barbería Norte", e: 4 },
  { n: "Tu peluquería", e: 4, tu: true },
];

const Lista: React.FC<{ busqueda: string }> = ({ busqueda }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const flecha = 0.5 + 0.5 * Math.sin((f / fps) * 7);
  return (
    <div style={{ position: "absolute", left: 70, width: 940, top: 560, borderRadius: 36, overflow: "hidden", background: BLANCO, boxShadow: "0 30px 80px rgba(0,0,0,.5)", fontFamily: FUENTE }}>
      <div style={{ padding: "22px 30px", display: "flex", gap: 20, alignItems: "center", borderBottom: "2px solid #eee" }}>
        <div style={{ width: 34, height: 34, borderRadius: 99, border: `7px solid ${GRIS_T}` }} />
        <div style={{ fontSize: 38, fontWeight: 600, color: "#202124" }}>{busqueda}</div>
      </div>
      <div style={{ position: "relative" }}>
        <MapaFondo alto={250} />
        {[[180, 130], [420, 90], [650, 170], [820, 120]].map(([x, y], i) => (
          <Pin key={i} x={x} y={y} k={interpolate(f, [2 + i * 3, 8 + i * 3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(2)) })} color={i === 3 ? AMARILLO : undefined} />
        ))}
      </div>
      {NEGOCIOS.map((b, i) => (
        <div key={i} style={{ padding: "20px 30px", borderTop: "2px solid #eee", background: b.tu ? "#fff8e1" : BLANCO, position: "relative", ...sale(f, i * 3 - 4) }}>
          <div style={{ fontSize: 40, fontWeight: 800, color: "#202124" }}>{b.n}</div>
          <div style={{ fontSize: 28, fontWeight: 500, color: GRIS_T, display: "flex", gap: 14, alignItems: "center" }}>
            <Estrellas llenas={b.e} /> · Peluquería · <span style={{ color: "#188038" }}>Abierto</span>
          </div>
          {b.tu ? (
            <div style={{ position: "absolute", right: 30, top: 28, background: ROJO, color: BLANCO, fontWeight: 900, fontSize: 40, padding: "6px 24px", borderRadius: 14, translate: `${-20 * flecha}px 0` }}>← TÚ</div>
          ) : null}
        </div>
      ))}
    </div>
  );
};

const FACT = ["Relevancia", "Distancia", "Prominencia"];

/** Las tres cosas de Google; `marcas`: momento (local, s) de check/candado de cada una (resumen). */
const Tres: React.FC<{ desde: number; marcas?: (number | null)[] }> = ({ desde, marcas }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <div style={{ position: "absolute", left: 90, right: 90, top: 600, display: "flex", flexDirection: "column", gap: 40 }}>
      {FACT.map((x, i) => {
        const m = marcas?.[i];
        const apagado = marcas && m === null;
        return (
          <div key={x} style={{ ...sale(f, Math.round(desde * fps) + i * 5), height: 200, borderRadius: 36, background: apagado ? "#2a3350" : BLANCO, display: "flex", alignItems: "center", gap: 40, padding: "0 46px", position: "relative", boxShadow: "0 20px 50px rgba(0,0,0,.35)" }}>
            <div style={{ width: 110, height: 110, borderRadius: 99, background: apagado ? "#3d4766" : AMARILLO, color: AZUL, fontFamily: FUENTE, fontWeight: 900, fontSize: 70, display: "flex", alignItems: "center", justifyContent: "center" }}>{i + 1}</div>
            <div style={{ fontFamily: FUENTE, fontWeight: 900, fontSize: 76, color: apagado ? "#6b7591" : AZUL }}>{x}</div>
            {m != null ? (
              <Sequence from={Math.round(m * fps)} layout="none">
                <div style={{ position: "absolute", right: -30, top: -30 }}>
                  <div style={{ position: "relative", width: 1, height: 1, scale: "0.55", left: 0, top: 0 }}>
                    <Sello bien x={0} y={0} />
                  </div>
                </div>
                <Sfx nombre="acierto" volumen={0.35} />
              </Sequence>
            ) : null}
            {apagado ? <div style={{ position: "absolute", right: 46, fontFamily: FUENTE, fontWeight: 800, fontSize: 34, color: "#8a93ad" }}>no se toca</div> : null}
          </div>
        );
      })}
      <div style={{ ...sale(f, Math.round(desde * fps) + 18), textAlign: "center", fontFamily: FUENTE, fontWeight: 600, fontSize: 34, color: "#aab3cc" }}>Fuente: ayuda oficial de Google</div>
    </div>
  );
};

const Ficha: React.FC<{ e: Escena; modo: "relevancia" | "prominencia" }> = ({ e, modo }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  const tCat = local(e, "categoría");
  const cambia = interpolate(t, [tCat, tCat + 0.35], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const tRes = local(e, "Reseñas");
  const tFot = local(e, "fotos");
  const tWeb = local(e, "web");
  const llenas = Math.floor(interpolate(t, [tRes, tRes + 0.8], [0, 5], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  return (
    <div style={{ position: "absolute", left: 60, width: 960, top: 580, borderRadius: 36, overflow: "hidden", background: BLANCO, boxShadow: "0 30px 80px rgba(0,0,0,.5)", fontFamily: FUENTE, ...sale(f, 0) }}>
      <MapaFondo alto={200} />
      <div style={{ padding: "30px 44px 40px" }}>
        <div style={{ fontSize: 72, fontWeight: 900, color: "#202124" }}>Tu peluquería</div>
        {modo === "relevancia" ? (
          <>
            <div style={{ marginTop: 20, fontSize: 52, fontWeight: 700, color: GRIS_T, position: "relative", height: 70 }}>
              <span style={{ position: "absolute", opacity: 1 - cambia, textDecoration: cambia > 0 ? "line-through" : undefined, color: cambia > 0 ? ROJO : GRIS_T }}>Salón de belleza</span>
              <span style={{ position: "absolute", opacity: cambia, color: "#188038", translate: `0 ${20 * (1 - cambia)}px` }}>Peluquería ✓</span>
            </div>
            <div style={{ marginTop: 30, display: "flex", flexDirection: "column", gap: 18 }}>
              {["Corte y color en Sevilla centro", "Mechas, alisado y peinados", "Cita por WhatsApp"].map((x, i) => (
                <div key={x} style={{ fontSize: 46, fontWeight: 600, color: "#3c4043", ...sale(f, Math.round(local(e, "diga") * fps) + i * 5) }}>• {x}</div>
              ))}
            </div>
          </>
        ) : (
          <div style={{ marginTop: 22, display: "flex", flexDirection: "column", gap: 30 }}>
            <div style={{ ...sale(f, Math.round(tRes * fps)), display: "flex", gap: 20, alignItems: "center" }}>
              <Estrellas tam={84} llenas={llenas} />
              <span style={{ fontSize: 44, fontWeight: 700, color: GRIS_T }}>Reseñas</span>
            </div>
            <div style={{ display: "flex", gap: 16 }}>
              {[0, 1, 2, 3].map((i) => (
                <div key={i} style={{ width: 205, height: 180, borderRadius: 20, background: ["#f3d2c1", "#c9d6ea", "#e3c8e6", "#d4e7d0"][i], ...sale(f, Math.round(tFot * fps) + i * 3), display: "flex", alignItems: "center", justifyContent: "center", fontSize: 54 }}>
                  <div style={{ width: 70, height: 54, border: "6px solid rgba(0,0,0,.25)", borderRadius: 10 }} />
                </div>
              ))}
            </div>
            <div style={{ ...sale(f, Math.round(tWeb * fps)), alignSelf: "flex-start", background: AZUL_G, color: BLANCO, fontSize: 50, fontWeight: 800, padding: "22px 44px", borderRadius: 99 }}>Sitio web →</div>
          </div>
        )}
      </div>
    </div>
  );
};

const Distancia: React.FC<{ e: Escena }> = ({ e }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const onda = ((f / fps) % 1.4) / 1.4;
  const tEso = local(e, "Eso");
  const candado = interpolate(f / fps, [tEso, tEso + 0.3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(2)) });
  return (
    <div style={{ position: "absolute", left: 70, width: 940, top: 570, height: 820, borderRadius: 40, overflow: "hidden", boxShadow: "0 30px 80px rgba(0,0,0,.5)", ...sale(f, 0) }}>
      <MapaFondo alto={820} />
      <div style={{ position: "absolute", left: 470 - 300, top: 430 - 300, width: 600, height: 600, borderRadius: 999, background: "rgba(26,115,232,.12)", border: "4px solid rgba(26,115,232,.5)", scale: `${0.3 + 0.7 * onda}`, opacity: 1 - onda }} />
      <div style={{ position: "absolute", left: 470 - 28, top: 430 - 28, width: 56, height: 56, borderRadius: 99, background: AZUL_G, border: "8px solid #fff", boxShadow: "0 0 0 14px rgba(26,115,232,.25)" }} />
      <div style={{ position: "absolute", left: 470 - 160, top: 480, width: 320, textAlign: "center", fontFamily: FUENTE, fontWeight: 800, fontSize: 34, color: AZUL_G }}>el que busca</div>
      {[[250, 260], [700, 320], [330, 650], [760, 690]].map(([x, y], i) => (
        <Pin key={i} x={x} y={y} color={i === 3 ? AMARILLO : undefined} k={interpolate(f, [4 + i * 3, 10 + i * 3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })} />
      ))}
      <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", background: `rgba(9,15,32,${0.45 * candado})` }}>
        <div style={{ scale: `${candado}`, width: 200, height: 200, borderRadius: 40, background: ROJO, border: "10px solid #fff", display: "flex", alignItems: "center", justifyContent: "center" }}>
          <div style={{ width: 90, height: 70, background: BLANCO, borderRadius: 12, position: "relative", top: 20 }}>
            <div style={{ position: "absolute", left: 12, top: -56, width: 66, height: 70, border: "14px solid #fff", borderBottom: "none", borderRadius: "40px 40px 0 0" }} />
          </div>
        </div>
      </div>
    </div>
  );
};

export const Pregunta: React.FC<Datos> = (d) => {
  const { fps } = useVideoConfig();
  const fr = (s: number) => Math.round(s * fps);
  const todas = d.escenas.flatMap((e) => e.palabras ?? []);
  const cta = d.escenas.find((e) => e.tipo === "cta");
  return (
    <AbsoluteFill style={{ background: AZUL }}>
      <Fondo tono="rgba(214,48,49,.12)" />
      {d.escenas.map((e, i) => {
        if (e.tipo === "cta") return null;
        let cuerpo: React.ReactNode = null;
        if (e.tipo === "gancho") cuerpo = <Lista busqueda={String(d.busqueda)} />;
        if (e.tipo === "tres") cuerpo = <Tres desde={0.1} />;
        if (e.tipo === "relevancia") cuerpo = <Ficha e={e} modo="relevancia" />;
        if (e.tipo === "distancia") cuerpo = <Distancia e={e} />;
        if (e.tipo === "prominencia") cuerpo = <Ficha e={e} modo="prominencia" />;
        if (e.tipo === "resumen") cuerpo = <Tres desde={0} marcas={[local(e, "una"), null, local(e, "tres")]} />;
        return (
          <Sequence key={i} from={fr(e.inicio)} durationInFrames={Math.max(1, fr(e.fin) - fr(e.inicio))} name={`${i} ${e.tipo}`}>
            {i === 0 ? cuerpo : <Entrada>{cuerpo}</Entrada>}
            {i > 0 ? <Sfx nombre="whoosh" volumen={0.35} /> : null}
          </Sequence>
        );
      })}
      {/* la pregunta se queda arriba hasta el cierre */}
      <Sequence durationInFrames={cta ? fr(cta.inicio) : undefined} layout="none">
        <Caja texto={String(d.pregunta)} />
      </Sequence>
      {cta ? (
        <Sequence from={fr(cta.inicio)} name="cierre">
          <Entrada>
            <Final frase={String(cta.frase)} idioma={d.idioma} />
          </Entrada>
          <Sfx nombre="whoosh" volumen={0.35} />
        </Sequence>
      ) : null}
      {d.escenas.map((e, i) =>
        e.rotulos ? <Rotulos key={`r${i}`} lista={e.rotulos.map((r) => ({ t: cuando(e, r.en), texto: r.texto, color: r.color }))} hasta={e.fin} y={420} /> : null,
      )}
      {cta ? <Rotulos lista={[{ t: cuando(cta, "estés"), texto: "TODA ESPAÑA", color: "blanco" }]} hasta={d.duracion} y={150} /> : null}
      {/* en el gancho la pregunta ya esta escrita arriba: sin subtitulos */}
      <Subtitulos palabras={todas.filter((p) => p.tramo > 0 && !cta?.palabras?.includes(p))} y={1440} />
      <Audio src={staticFile(d.audio)} />
    </AbsoluteFill>
  );
};

