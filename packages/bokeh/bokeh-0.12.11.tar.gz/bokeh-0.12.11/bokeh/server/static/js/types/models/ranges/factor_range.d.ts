import { Range } from "./range";
export declare var map_one_level: (factors: any, padding: any, offset?: number) => {}[];
export declare var map_two_levels: (factors: any, outer_pad: any, factor_pad: any, offset?: number) => {}[];
export declare var map_three_levels: (factors: any, outer_pad: any, inner_pad: any, factor_pad: any, offset?: number) => {}[];
export declare class FactorRange extends Range {
    initialize(attrs: any, options: any): any;
    reset(): any;
    synthetic(x: any): any;
    v_synthetic(xs: any): any;
    _init(): any;
    _lookup(x: any): any;
}
