import { CalculateMetadataFunction, Composition } from "remotion";
import { AntesDespues } from "./AntesDespues";
import { Pregunta } from "./Pregunta";
import { Datos } from "./comun/tipos";
import { fuentesListas } from "./comun/marca";
import ejAntesDespues from "../public/antes_despues_es/datos.json";
import ejPregunta from "../public/pregunta_maps_es/datos.json";

// La duracion la marca la voz: herramientas/remo.py deja datos.json con todo
const segunDatos: CalculateMetadataFunction<Datos> = async ({ props }) => {
  await fuentesListas;
  return { durationInFrames: Math.ceil(props.duracion * 30) };
};

const comun = { width: 1080, height: 1920, fps: 30, durationInFrames: 900, calculateMetadata: segunDatos };

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition id="AntesDespues" component={AntesDespues} defaultProps={ejAntesDespues as unknown as Datos} {...comun} />
      <Composition id="Pregunta" component={Pregunta} defaultProps={ejPregunta as unknown as Datos} {...comun} />
    </>
  );
};
