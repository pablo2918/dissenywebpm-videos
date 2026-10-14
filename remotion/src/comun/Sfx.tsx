import React from "react";
import { staticFile } from "remotion";
import { Audio } from "@remotion/media";
import { VOLUMEN_EFECTOS } from "./marca";

/** Efecto de sonido de public/sfx/ con el volumen general de efectos aplicado. */
export const Sfx: React.FC<{ nombre: string; volumen: number }> = ({ nombre, volumen }) => (
  <Audio src={staticFile(`sfx/${nombre}.wav`)} volume={volumen * VOLUMEN_EFECTOS} />
);
