import React from "react";
import { AbsoluteFill, Easing, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { Fondo } from "./comun/Fondo";
import { Subtitulos } from "./comun/Subtitulos";
import { Final } from "./comun/Final";
import { Titulo } from "./comun/Texto";
import { Entrada } from "./comun/Efectos";
import { AMARILLO, AZUL, BLANCO, FUENTE, GRIS, ROJO, VERDE } from "./comun/marca";
import { Datos, Escena } from "./comun/tipos";

/* «Mito o verdad» 2.0: gancho «¿Cuánto sabes de SEO?», tres frases con
   cuenta atras (tic-tac), respuesta con sello y sonido, y marcador arriba. */

const rebote = Easing.out(Easing.back(2));
const cl = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

/** Las tres respuestas arriba: vacias hasta que se dicen. */
const Marcador: React.FC<{ escenas: Escena[] }> = ({ escenas }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  const resp = escenas.filter((e) => e.tipo === "respuesta");
  return (
    <div style={{ position: "absolute", top: 120, left: 0, right: 0, display: "flex", justifyContent: "center", gap: 26 }}>
      {resp.map((r, i) => {
        const k = interpolate(t, [r.inicio, r.inicio + 0.3], [0, 1], { ...cl, easing: rebote });
        const actual = escenas.find((e) => e.tipo === "pregunta" && e.n === r.n);
        const ahora = actual && t >= actual.inicio && t < r.fin;
        return (
          <div key={i} style={{ width: 120, height: 120, borderRadius: 99, border: `6px solid ${ahora ? AMARILLO : "#2f3a5c"}`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: FUENTE, fontWeight: 900, fontSize: 40, color: GRIS, position: "relative" }}>
            {i + 1}
            <div style={{ position: "absolute", inset: -6, borderRadius: 99, background: r.verdad ? VERDE : ROJO, color: BLANCO, display: "flex", alignItems: "center", justifyContent: "center", fontSize: r.verdad ? 21 : 27, scale: `${k}`, border: "6px solid #fff" }}>
              {r.verdad ? "VERDAD" : "MITO"}
            </div>
          </div>
        );
      })}
    </div>
  );
};

const Boton: React.FC<{ txt: string; color: string; lleno: boolean; k?: number }> = ({ txt, color, lleno, k = 1 }) => (
  <div style={{ width: 430, height: 150, borderRadius: 99, border: `8px solid ${color}`, background: lleno ? color : "transparent", color: lleno ? BLANCO : color, fontFamily: FUENTE, fontWeight: 900, fontSize: 64, display: "flex", alignItems: "center", justifyContent: "center", scale: `${k}` }}>
    {txt}
  </div>
);

/** Dibujito de lo que dice la frase (que se VEA de que hablamos). */
const Ilus: React.FC<{ tipo: string }> = ({ tipo }) => {
  const f = useCurrentFrame();
  const caja: React.CSSProperties = { width: 760, height: 330, borderRadius: 30, background: BLANCO, boxShadow: "0 20px 50px rgba(0,0,0,.4)", overflow: "hidden", position: "relative", fontFamily: FUENTE };
  if (tipo === "repetir") {
    const frase = "fontanero en Sevilla";
    return (
      <div style={{ ...caja, padding: 30, fontSize: 30, lineHeight: 1.5, color: "#555", fontWeight: 600 }}>
        {Array.from({ length: 9 }, (_, i) => (
          <span key={i} style={{ background: f > 6 + i * 4 ? "#ffe58f" : "transparent", color: "#222", padding: "0 4px", borderRadius: 6 }}>
            {frase}
            {i % 3 === 2 ? ". " : ", "}
          </span>
        ))}
      </div>
    );
  }
  if (tipo === "movil") {
    const k = interpolate(f, [8, 20], [0, 1], { ...cl, easing: rebote });
    return (
      <div style={{ ...caja, background: "transparent", boxShadow: "none", display: "flex", alignItems: "flex-end", justifyContent: "center", gap: 60 }}>
        <div style={{ width: 380, height: 250, borderRadius: 18, border: "14px solid #3a4566", background: "#e9edf7", opacity: 0.6 }} />
        <div style={{ width: 160, height: 320, borderRadius: 30, border: `14px solid ${AMARILLO}`, background: BLANCO, scale: `${0.8 + 0.25 * k}`, boxShadow: `0 0 ${60 * k}px rgba(251,190,1,.6)` }} />
      </div>
    );
  }
  // blog
  const tacha = interpolate(f, [10, 18], [0, 1], cl);
  return (
    <div style={{ ...caja, display: "flex", flexDirection: "column" }}>
      <div style={{ display: "flex", gap: 30, padding: "22px 30px", borderBottom: "3px solid #eee", fontSize: 34, fontWeight: 800, color: "#333" }}>
        <span>Inicio</span><span>Servicios</span><span>Contacto</span>
        <span style={{ position: "relative", color: ROJO }}>
          Blog
          <span style={{ position: "absolute", left: -6, right: -6, top: "50%", height: 6, background: ROJO, scale: `${tacha} 1`, transformOrigin: "left" }} />
        </span>
      </div>
      <div style={{ padding: 30, display: "flex", flexDirection: "column", gap: 18 }}>
        {[0.9, 0.7, 0.8].map((w, i) => (
          <div key={i} style={{ height: 26, width: `${w * 100}%`, background: "#e3e6ee", borderRadius: 8 }} />
        ))}
      </div>
    </div>
  );
};

const PreguntaV: React.FC<{ e: Escena }> = ({ e }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  const finVoz = (e.finVoz ?? e.fin) - e.inicio;
  const dur = e.fin - e.inicio;
  const q = interpolate(t, [finVoz, dur], [1, 0], cl);
  const bot = interpolate(t, [0.2, 0.5], [0, 1], { ...cl, easing: rebote });
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", top: 290, left: 0, right: 0, display: "flex", justifyContent: "center" }}>
        <div style={{ background: AMARILLO, color: AZUL, fontFamily: FUENTE, fontWeight: 900, fontSize: 40, padding: "10px 30px", borderRadius: 99 }}>{String(e.n)}/3 · ¿MITO O VERDAD?</div>
      </div>
      <div style={{ position: "absolute", top: 400, left: 70, right: 70, height: 440, display: "flex", alignItems: "center", justifyContent: "center" }}>
        <Titulo texto={`«${String(e.frase)}»`} tam={78} />
      </div>
      <div style={{ position: "absolute", top: 880, left: 0, right: 0, display: "flex", justifyContent: "center", scale: `${interpolate(f, [4, 14], [0.7, 1], { ...cl, easing: rebote })}`, opacity: interpolate(f, [4, 9], [0, 1], cl) }}>
        <Ilus tipo={String(e.ilus)} />
      </div>
      <div style={{ position: "absolute", top: 1290, left: 0, right: 0, display: "flex", justifyContent: "center", gap: 40, opacity: bot, translate: `0 ${40 * (1 - bot)}px` }}>
        <Boton txt="MITO" color={ROJO} lleno={false} />
        <Boton txt="VERDAD" color={VERDE} lleno={false} />
      </div>
      {t >= finVoz ? (
        <>
          <div style={{ position: "absolute", top: 1490, left: 140, width: 800, height: 22, borderRadius: 99, background: "#2a3557" }}>
            <div style={{ width: `${q * 100}%`, height: "100%", borderRadius: 99, background: AMARILLO }} />
          </div>
          <div style={{ position: "absolute", top: 1540, left: 0, right: 0, textAlign: "center", fontFamily: FUENTE, fontWeight: 800, fontSize: 48, color: "#c7cde0" }}>¿Tú qué dices?</div>
        </>
      ) : null}
      <Sequence from={Math.round(finVoz * fps)} layout="none">
        <Audio src={staticFile("sfx/tictac.wav")} volume={0.7} />
      </Sequence>
    </AbsoluteFill>
  );
};

const RespuestaV: React.FC<{ e: Escena; p: Escena }> = ({ e, p }) => {
  const f = useCurrentFrame();
  const verdad = Boolean(e.verdad);
  const color = verdad ? VERDE : ROJO;
  const st = interpolate(f, [0, 9], [1.8, 1], { ...cl, easing: rebote });
  const pq = interpolate(f, [8, 16], [0, 1], { ...cl, easing: Easing.out(Easing.cubic) });
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", top: 290, left: 0, right: 0, display: "flex", justifyContent: "center" }}>
        <div style={{ background: color, color: BLANCO, fontFamily: FUENTE, fontWeight: 900, fontSize: 40, padding: "10px 30px", borderRadius: 99 }}>{String(e.n)}/3 · {verdad ? "ES VERDAD" : "ES UN MITO"}</div>
      </div>
      <div style={{ position: "absolute", top: 400, left: 70, right: 70, height: 440, display: "flex", alignItems: "center", justifyContent: "center", opacity: 0.45 }}>
        <Titulo texto={`«${String(p.frase)}»`} tam={78} />
      </div>
      <div style={{ position: "absolute", top: 470, left: 0, right: 0, display: "flex", justifyContent: "center" }}>
        <div style={{ background: BLANCO, padding: 14, borderRadius: 40, rotate: "-7deg", scale: `${st}`, opacity: interpolate(f, [0, 3], [0, 1], cl), boxShadow: "0 30px 70px rgba(0,0,0,.5)" }}>
          <div style={{ background: color, color: BLANCO, fontFamily: FUENTE, fontWeight: 900, fontSize: 150, padding: "10px 60px", borderRadius: 30 }}>{verdad ? "¡VERDAD!" : "¡MITO!"}</div>
        </div>
      </div>
      <div style={{ position: "absolute", top: 940, left: 70, right: 70, opacity: pq, translate: `0 ${60 * (1 - pq)}px` }}>
        <div style={{ background: BLANCO, borderRadius: 34, padding: "40px 50px", borderLeft: `22px solid ${color}`, fontFamily: FUENTE, fontWeight: 800, fontSize: 64, lineHeight: 1.15, color: AZUL, textAlign: "center", boxShadow: "0 20px 50px rgba(0,0,0,.4)" }}>
          {String(e.porque)}
        </div>
      </div>
      <div style={{ position: "absolute", top: 1290, left: 0, right: 0, display: "flex", justifyContent: "center", gap: 40, opacity: 1 - pq }}>
        <Boton txt="MITO" color={ROJO} lleno={!verdad} k={!verdad ? st * 0.95 : 0.9} />
        <Boton txt="VERDAD" color={VERDE} lleno={verdad} k={verdad ? st * 0.95 : 0.9} />
      </div>
      <Audio src={staticFile(verdad ? "sfx/acierto.wav" : "sfx/fallo.wav")} volume={0.6} />
    </AbsoluteFill>
  );
};

const Gancho: React.FC<{ e: Escena }> = ({ e }) => {
  const f = useCurrentFrame();
  const sacude = f < 10 ? Math.sin(f * 2.2) * (10 - f) * 1.2 : 0;
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", padding: "0 60px" }}>
      <div style={{ translate: `${sacude}px 0`, scale: `${interpolate(f, [0, 8], [1.15, 1], { ...cl, easing: rebote })}`, marginTop: -120 }}>
        <Titulo texto={String(e.titulo)} tam={140} />
      </div>
      <div style={{ marginTop: 60, display: "flex", gap: 30, opacity: interpolate(f, [24, 32], [0, 1], cl) }}>
        <Boton txt="MITO" color={ROJO} lleno={false} k={0.85} />
        <Boton txt="VERDAD" color={VERDE} lleno={false} k={0.85} />
      </div>
    </AbsoluteFill>
  );
};

const Resultado: React.FC = () => {
  const f = useCurrentFrame();
  const filas = [["3/3", "Sabes más que muchos"], ["2/3", "Vas bien"], ["0–1", "Hablamos 😉"]];
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 34, paddingBottom: 200 }}>
      <Titulo texto="¿Cuántas has *acertado*?" tam={100} style={{ padding: "0 60px", marginBottom: 30 }} />
      {filas.map(([a, b], i) => (
        <div key={a} style={{ width: 880, display: "flex", gap: 40, alignItems: "center", background: "rgba(255,255,255,.08)", borderRadius: 30, padding: "24px 40px", opacity: interpolate(f, [8 + i * 5, 14 + i * 5], [0, 1], cl), translate: `${interpolate(f, [8 + i * 5, 16 + i * 5], [80, 0], { ...cl, easing: rebote })}px 0` }}>
          <div style={{ fontFamily: FUENTE, fontWeight: 900, fontSize: 70, color: AMARILLO, width: 200 }}>{a}</div>
          <div style={{ fontFamily: FUENTE, fontWeight: 800, fontSize: 50, color: BLANCO }}>{b.replace(" 😉", "")}</div>
        </div>
      ))}
    </AbsoluteFill>
  );
};

export const Mito: React.FC<Datos> = (d) => {
  const { fps } = useVideoConfig();
  const fr = (s: number) => Math.round(s * fps);
  const cta = d.escenas.find((e) => e.tipo === "cta");
  const preg = d.escenas.filter((e) => e.tipo === "pregunta");
  const marcadorDesde = d.escenas[1].inicio;
  const resultado = d.escenas.find((e) => e.tipo === "resultado");
  return (
    <AbsoluteFill style={{ background: AZUL }}>
      <Fondo />
      {d.escenas.map((e, i) => {
        if (e.tipo === "cta") return null;
        let cuerpo: React.ReactNode = null;
        if (e.tipo === "gancho") cuerpo = <Gancho e={e} />;
        if (e.tipo === "pregunta") cuerpo = <PreguntaV e={e} />;
        if (e.tipo === "respuesta") cuerpo = <RespuestaV e={e} p={preg.find((p) => p.n === e.n) ?? e} />;
        if (e.tipo === "resultado") cuerpo = <Resultado />;
        return (
          <Sequence key={i} from={fr(e.inicio)} durationInFrames={Math.max(1, fr(e.fin) - fr(e.inicio))} name={`${i} ${e.tipo}`}>
            {i === 0 || e.tipo === "respuesta" ? cuerpo : <Entrada>{cuerpo}</Entrada>}
            {i > 0 && e.tipo !== "respuesta" ? <Audio src={staticFile("sfx/whoosh.wav")} volume={0.35} /> : null}
          </Sequence>
        );
      })}
      <Sequence from={fr(marcadorDesde)} durationInFrames={fr((resultado?.inicio ?? d.duracion) - marcadorDesde)} layout="none">
        <Marcador escenas={d.escenas.map((e) => ({ ...e, inicio: e.inicio - marcadorDesde, fin: e.fin - marcadorDesde }))} />
      </Sequence>
      {cta ? (
        <Sequence from={fr(cta.inicio)} name="cierre">
          <Entrada>
            <Final frase={String(cta.frase)} idioma={d.idioma} />
          </Entrada>
          <Audio src={staticFile("sfx/whoosh.wav")} volume={0.35} />
        </Sequence>
      ) : null}
      {/* el texto ya esta en pantalla en casi todo; subtitulos solo en el resultado */}
      {resultado ? <Subtitulos palabras={resultado.palabras ?? []} y={1500} /> : null}
      <Audio src={staticFile(d.audio)} />
    </AbsoluteFill>
  );
};
