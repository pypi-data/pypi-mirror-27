import { Transform } from "./transform";
export declare class CustomJSTransform extends Transform {
    compute(x: any): any;
    v_compute(xs: any): any;
    _make_transform(val: any, fn: any): Function;
    _make_values(): {}[];
}
