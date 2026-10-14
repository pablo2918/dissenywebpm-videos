import React from "react";
import { AbsoluteFill, Easing, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import { Fondo } from "./comun/Fondo";
import { Subtitulos } from "./comun/Subtitulos";
import { Rotulos } from "./comun/Rotulo";
import { Movil } from "./comun/Movil";
import { Camara, Toma } from "./comun/Camara";
import { Final } from "./comun/Final";
import { Titulo } from "./comun/Texto";
import { Entrada, Marco, Sello, Toque } from "./comun/Efectos";
import { AMARILLO, AZUL, BLANCO, FUENTE, ROJO, VERDE } from "./comun/marca";
import { cuando, Datos, Escena } from "./comun/tipos";

// Capturas reales de las dos webs de ejemplo (remotion/scripts/captura_web.mjs)
const VIEJA = { src: "antes_despues/vieja.png", css: 980 };
const NUEVA = { src: "antes_despues/nueva.png", css: 390 };

// Movil grande centrado: ancho 700, arriba 330 -> pantalla desde (214.5, 354.5)
const M = { x: 190, y: 330, w: 700 };
const PANT = { x: M.x + M.w * 0.035, y: M.y + M.w * 0.035, w: M.w * 0.93 };
/** De px CSS de una web a px del lienzo (con el movil grande y un scroll dado). */
const aLienzo = (css: number, cx: number, cy: number, scroll = 0) => {
  const k = PANT.w / css;
  return { x: PANT.x + cx * k, y: PANT.y + (cy - scroll) * k };
};

const local = (e: Escena, t: number) => t - e.inicio;

const Gancho: React.FC<{ e: Escena }> = ({ e }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  const busca = "panadería valladolid";
  const escrito = busca.slice(0, Math.floor(interpolate(t, [0.2, 1.4], [0, busca.length], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })));
  const tCual = local(e, cuando(e, "cuál"));
  const sube = (d: number) => interpolate(t, [d, d + 0.35], [500, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(1.2)) });
  const scrollV = interpolate(t, [1, 6], [0, 300], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const scrollN = interpolate(t, [1, 6], [0, 420], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const num = (n: string, x: number, d: number) => (
    <div style={{ position: "absolute", left: x + 215 - 50, top: 430, width: 100, height: 100, borderRadius: 99, background: AMARILLO, color: AZUL, fontFamily: FUENTE, fontWeight: 900, fontSize: 64, display: "flex", alignItems: "center", justifyContent: "center", translate: `0 ${sube(d)}px`, boxShadow: "0 10px 30px rgba(0,0,0,.4)", zIndex: 2 }}>{n}</div>
  );
  return (
    <AbsoluteFill>
      {t < tCual ? (
        <div style={{ position: "absolute", left: 90, right: 90, top: 190, height: 130, borderRadius: 99, background: BLANCO, display: "flex", alignItems: "center", padding: "0 50px", gap: 28, boxShadow: "0 20px 50px rgba(0,0,0,.4)" }}>
          <div style={{ width: 46, height: 46, borderRadius: 99, border: "8px solid #555", flexShrink: 0 }} />
          <div style={{ fontFamily: FUENTE, fontWeight: 600, fontSize: 52, color: "#222" }}>
            {escrito}
            <span style={{ opacity: Math.floor(t * 2.5) % 2 ? 0 : 1 }}>|</span>
          </div>
        </div>
      ) : (
        <Sequence from={Math.round(tCual * fps)} layout="none">
          <div style={{ position: "absolute", left: 40, right: 40, top: 150 }}>
            <Titulo texto={String(e.titulo)} tam={112} />
          </div>
          <Audio src={staticFile("sfx/pop.wav")} volume={0.55} />
        </Sequence>
      )}
      {num("1", 85, 0.05)}
      {num("2", 565, 0.15)}
      <Movil src={VIEJA.src} anchoCss={VIEJA.css} ancho={430} scroll={scrollV} fondo="#c9c9c9" style={{ left: 85, top: 490, translate: `0 ${sube(0)}px`, rotate: "-2deg" }} />
      <Movil src={NUEVA.src} anchoCss={NUEVA.css} ancho={430} scroll={scrollN} style={{ left: 565, top: 490, translate: `0 ${sube(0.1)}px`, rotate: "2deg" }} />
    </AbsoluteFill>
  );
};

const Vieja: React.FC<{ e: Escena; pie?: boolean }> = ({ e, pie }) => {
  const { fps } = useVideoConfig();
  const p = aLienzo(VIEJA.css, 490, 617);
  const h2 = aLienzo(VIEJA.css, 490, 213);
  const fin = aLienzo(VIEJA.css, 490, 1391);
  const tomas: Toma[] = pie
    ? [{ t: 0, x: 540, y: 960, s: 1 }, { t: 0.15, x: fin.x, y: fin.y, s: 2.3 }]
    : [
        { t: 0, x: 540, y: 960, s: 1 },
        { t: local(e, cuando(e, "diminuta")) - 0.2, x: p.x, y: p.y, s: 2.4 },
        { t: local(e, cuando(e, "Bienvenidos")) - 0.2, x: h2.x, y: h2.y, s: 2.1 },
        { t: local(e, cuando(e, "rastro")) - 0.2, x: 540, y: 1000, s: 1.05 },
      ];
  return (
    <Camara tomas={tomas}>
      <Movil src={VIEJA.src} anchoCss={VIEJA.css} ancho={M.w} fondo="#c9c9c9" style={{ left: M.x, top: M.y }}>
        {pie ? <Marco caja={[10, 1351, 960, 80]} color={ROJO} desde={Math.round(local(e, cuando(e, "buscar")) * fps)} /> : null}
      </Movil>
    </Camara>
  );
};

const Nueva: React.FC<{ e: Escena }> = ({ e }) => {
  const { fps } = useVideoConfig();
  const h1 = aLienzo(NUEVA.css, 195, 364);
  const wa = aLienzo(NUEVA.css, 195, 553);
  const tWa = local(e, cuando(e, "WhatsApp"));
  const tToque = local(e, cuando(e, "toque"));
  return (
    <>
      <Camara tomas={[{ t: 0, x: 540, y: 960, s: 1 }, { t: local(e, cuando(e, "arriba")) - 0.25, x: h1.x, y: h1.y, s: 1.3 }, { t: tWa - 0.3, x: wa.x, y: wa.y, s: 1.4 }]}>
        <Movil src={NUEVA.src} anchoCss={NUEVA.css} ancho={M.w} style={{ left: M.x, top: M.y }}>
          <Marco caja={[34, 293, 322, 143]} color={VERDE} desde={Math.round(local(e, cuando(e, "arriba")) * fps)} />
        </Movil>
        <Sequence from={Math.round((tToque - 0.15) * fps)} layout="none">
          <Toque x={wa.x} y={wa.y} />
          <Audio src={staticFile("sfx/clic.wav")} volume={0.8} />
        </Sequence>
      </Camara>
    </>
  );
};

const NuevaScroll: React.FC<{ e: Escena }> = ({ e }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = f / fps;
  const a = local(e, cuando(e, "Horario"));
  const b = local(e, cuando(e, "fotos"));
  const c = local(e, cuando(e, "zoom"));
  const scroll = interpolate(t, [0, a, a + 0.6, b, b + 0.6, c, c + 0.6], [380, 380, 520, 520, 860, 860, 921], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic),
  });
  return (
    <Camara tomas={[{ t: 0, x: 540, y: 1000, s: 1.06 }]}>
      <Movil src={NUEVA.src} anchoCss={NUEVA.css} ancho={M.w} scroll={scroll} style={{ left: M.x, top: M.y }} />
    </Camara>
  );
};

const Compara: React.FC<{ e: Escena }> = ({ e }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const tSi = local(e, cuando(e, "escribes"));
  const tNo = local(e, cuando(e, "otra"));
  const gris = interpolate(f / fps, [tNo, tNo + 0.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 40, right: 40, top: 170 }}>
        <Titulo texto="Mismo *pan*" tam={120} />
      </div>
      <Movil src={VIEJA.src} anchoCss={VIEJA.css} ancho={430} gris={gris} fondo="#c9c9c9" style={{ left: 85, top: 400, rotate: "-2deg" }} />
      <Movil src={NUEVA.src} anchoCss={NUEVA.css} ancho={430} style={{ left: 565, top: 400, rotate: "2deg", scale: `${1 + 0.05 * interpolate(f / fps, [tSi, tSi + 0.3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })}` }} />
      <Sequence from={Math.round(tSi * fps)} layout="none">
        <Sello bien x={780} y={840} />
        <Audio src={staticFile("sfx/acierto.wav")} volume={0.5} />
      </Sequence>
      <Sequence from={Math.round(tNo * fps)} layout="none">
        <Sello bien={false} x={300} y={840} />
        <Audio src={staticFile("sfx/fallo.wav")} volume={0.6} />
      </Sequence>
    </AbsoluteFill>
  );
};

export const AntesDespues: React.FC<Datos> = (d) => {
  const { fps } = useVideoConfig();
  const fr = (s: number) => Math.round(s * fps);
  const todas = d.escenas.flatMap((e) => e.palabras ?? []);
  const cta = d.escenas.find((e) => e.tipo === "cta");
  return (
    <AbsoluteFill style={{ background: AZUL }}>
      <Fondo />
      {d.escenas.map((e, i) => {
        const dur = Math.max(1, fr(e.fin) - fr(e.inicio));
        let cuerpo: React.ReactNode = null;
        if (e.tipo === "gancho") cuerpo = <Gancho e={e} />;
        if (e.tipo === "vieja") cuerpo = <Vieja e={e} />;
        if (e.tipo === "vieja_pie") cuerpo = <Vieja e={e} pie />;
        if (e.tipo === "nueva") cuerpo = <Nueva e={e} />;
        if (e.tipo === "nueva_scroll") cuerpo = <NuevaScroll e={e} />;
        if (e.tipo === "compara") cuerpo = <Compara e={e} />;
        if (e.tipo === "cta") return null;
        return (
          <Sequence key={i} from={fr(e.inicio)} durationInFrames={dur} name={`${i} ${e.tipo}`}>
            {i === 0 ? cuerpo : <Entrada>{cuerpo}</Entrada>}
            {i > 0 ? <Audio src={staticFile("sfx/whoosh.wav")} volume={0.35} /> : null}
          </Sequence>
        );
      })}
      {cta ? (
        <Sequence from={fr(cta.inicio)} name="cierre">
          <Entrada>
            <Final frase={String(cta.frase)} idioma={d.idioma} />
          </Entrada>
          <Audio src={staticFile("sfx/whoosh.wav")} volume={0.35} />
        </Sequence>
      ) : null}
      {/* rotulos de palabra clave (los de cada escena + los del cierre) */}
      {d.escenas.map((e, i) =>
        e.rotulos ? (
          <Rotulos key={`r${i}`} lista={e.rotulos.map((r) => ({ t: cuando(e, r.en), texto: r.texto, color: r.color }))} hasta={e.fin} />
        ) : null,
      )}
      {cta ? (
        <Rotulos
          lista={[
            { t: cuando(cta, "demo"), texto: "DEMO GRATIS EN 48 H" },
            { t: cuando(cta, "estés"), texto: "TODA ESPAÑA", color: "blanco" },
          ]}
          hasta={d.duracion}
          y={150}
        />
      ) : null}
      {/* subtitulos: en el gancho van debajo de los moviles; en el cierre no (ya esta el texto) */}
      <Subtitulos palabras={todas.filter((p) => d.escenas[0].palabras?.includes(p))} y={1450} />
      <Subtitulos palabras={todas.filter((p) => !d.escenas[0].palabras?.includes(p) && !cta?.palabras?.includes(p))} y={1230} />
      <Audio src={staticFile(d.audio)} />
    </AbsoluteFill>
  );
};
