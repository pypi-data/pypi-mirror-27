import { DataRange } from "./data_range";
export declare class DataRange1d extends DataRange {
    initialize(attrs: any, options: any): any;
    computed_renderers(): any;
    _compute_plot_bounds(renderers: any, bounds: any): {
        minX: number;
        minY: number;
        maxX: number;
        maxY: number;
    };
    _compute_min_max(plot_bounds: any, dimension: any): number[];
    _compute_range(min: any, max: any): number[];
    update(bounds: any, dimension: any, bounds_id: any): any;
    reset(): any;
}
