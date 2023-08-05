import * as proj4 from "proj4/lib/core";
export { proj4 };
export declare var mercator: any;
export declare var wgs84: any;
export declare var mercator_bounds: {
    lon: number[];
    lat: number[];
};
export declare var clip_mercator: (low: any, high: any, dimension: any) => number[];
export declare var in_bounds: (value: any, dimension: any) => boolean;
