import { AbsoluteFill, Composition, interpolate, useCurrentFrame } from "remotion";

export const MyComposition = () => (
  <Composition id="Prueba" component={Prueba} durationInFrames={60} fps={30} width={1080} height={1920} />
);

export const Prueba: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ backgroundColor: "#0b1530", justifyContent: "center", alignItems: "center" }}>
      <div style={{ color: "white", fontSize: 120, fontWeight: 900, scale: interpolate(f, [0, 20], [0.5, 1], { extrapolateRight: "clamp" }) }}>Hola Pablo</div>
    </AbsoluteFill>
  );
};
