// Type declarations for non-code side-effect imports handled by webpack loaders.
declare module "*.css";
declare module "*.scss";

// svg-gauge ships no types; only the constructor signature used by
// templates/status.html matters here.
declare module "svg-gauge/dist/gauge.min.js" {
  interface GaugeOptions {
    max?: number;
    min?: number;
    value?: number;
    dialStartAngle?: number;
    dialEndAngle?: number;
    label?: (value: number) => string;
  }

  interface GaugeInstance {
    setValue(value: number): void;
    setValueAnimated(value: number, duration: number): void;
  }

  function Gauge(element: HTMLElement | null, options: GaugeOptions): GaugeInstance;

  export default Gauge;
}
