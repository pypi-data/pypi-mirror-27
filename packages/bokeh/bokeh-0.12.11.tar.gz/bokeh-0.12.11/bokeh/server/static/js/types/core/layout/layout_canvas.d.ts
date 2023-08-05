import { Variable, Constraint } from "./solver";
import { HasProps } from "../has_props";
import { BBox } from "../util/bbox";
export interface ViewTransform {
    compute: (v: number) => number;
    v_compute: (vv: number[] | Float64Array) => Float64Array;
}
export declare class LayoutCanvas extends HasProps {
    _top: Variable;
    _left: Variable;
    _width: Variable;
    _height: Variable;
    _right: Variable;
    _bottom: Variable;
    _hcenter: Variable;
    _vcenter: Variable;
    initialize(attrs: any, options?: any): void;
    get_editables(): Variable[];
    get_constraints(): Constraint[];
    readonly bbox: BBox;
    readonly layout_bbox: {
        top: number;
        left: number;
        width: number;
        height: number;
        right: number;
        bottom: number;
        hcenter: number;
        vcenter: number;
    };
    readonly xview: ViewTransform;
    readonly yview: ViewTransform;
}
