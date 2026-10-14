export type Palabra = { texto: string; tramo: number; inicio: number; fin: number };
export type RotuloDef = { en: string; texto: string; color?: string };
export type Escena = {
  tipo: string;
  voz?: string;
  inicio: number;
  fin: number;
  finVoz?: number;
  palabras?: Palabra[];
  rotulos?: RotuloDef[];
  [k: string]: unknown;
};
export type Datos = {
  id: string;
  idioma: "es" | "ca";
  carpeta: string;
  audio: string;
  duracion: number;
  escenas: Escena[];
  [k: string]: unknown;
};

const limpia = (s: string) => s.toLowerCase().replace(/[^\p{L}\p{N}]/gu, "");

/** Momento (s) en que se dice la palabra `w` dentro de la escena (o su inicio si no está). */
export const cuando = (e: Escena, w: string) => {
  const p = (e.palabras ?? []).find((x) => limpia(x.texto).startsWith(limpia(w)));
  return p ? p.inicio : e.inicio;
};
