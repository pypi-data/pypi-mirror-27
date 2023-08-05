import { Scale } from "./scale";
export declare class LinearScale extends Scale {
    compute(x: any): any;
    v_compute(xs: any): Float64Array;
    invert(xprime: any): number;
    v_invert(xprimes: any): Float64Array;
    _compute_state(): any[];
}
