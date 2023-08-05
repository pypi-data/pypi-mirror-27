import { Transform } from "../transforms";
export declare class Scale extends Transform {
    compute(x: any): void;
    v_compute(xs: any): void;
    invert(sx: any): void;
    v_invert(sxs: any): void;
    r_compute(x0: any, x1: any): void[];
    r_invert(sx0: any, sx1: any): void[];
}
