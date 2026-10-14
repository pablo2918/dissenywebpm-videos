import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

// Colores de Disseny Web PM (los mismos que el motor Python)
export const AZUL = "#090f20";
export const AZUL2 = "#14203f";
export const AMARILLO = "#fbbe01";
export const ROJO = "#d63031";
export const VERDE = "#25a35c";
export const BLANCO = "#ffffff";
export const GRIS = "#969eb2";
export const COLORES: Record<string, string> = { amarillo: AMARILLO, rojo: ROJO, verde: VERDE, blanco: BLANCO };

export const FUENTE = "Montserrat";
export const TELEFONO = "641 27 74 95";
export const DOMINIO = "dissenywebpm.com";
export const TXT = {
  es: { cta: "Escríbeme por WhatsApp", demo: "Demo gratis en 48 h", espana: "Webs para negocios de toda España" },
  ca: { cta: "Escriu-me per WhatsApp", demo: "Demo gratis en 48 h", espana: "Webs per a negocis de tot Espanya" },
};
export type Idioma = keyof typeof TXT;

const pesos: [string, string][] = [["Black", "900"], ["ExtraBold", "800"], ["Bold", "700"], ["SemiBold", "600"], ["Medium", "500"]];
export const fuentesListas = Promise.all(
  pesos.map(([n, w]) => loadFont({ family: FUENTE, url: staticFile(`marca/Montserrat-${n}.otf`), weight: w })),
);
