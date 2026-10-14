import { CalculateMetadataFunction, Composition } from "remotion";
import { AntesDespues } from "./AntesDespues";
import { Datos } from "./comun/tipos";
import { fuentesListas } from "./comun/marca";
import datosEjemplo from "../public/antes_despues_es/datos.json";

// La duracion la marca la voz: herramientas/remo.py deja datos.json con todo
const segunDatos: CalculateMetadataFunction<Datos> = async ({ props }) => {
  await fuentesListas;
  return { durationInFrames: Math.ceil(props.duracion * 30) };
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="AntesDespues"
        component={AntesDespues}
        width={1080}
        height={1920}
        fps={30}
        durationInFrames={900}
        defaultProps={datosEjemplo as unknown as Datos}
        calculateMetadata={segunDatos}
      />
    </>
  );
};
