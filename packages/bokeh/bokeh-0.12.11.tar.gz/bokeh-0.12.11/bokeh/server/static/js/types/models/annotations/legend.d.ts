import { Annotation, AnnotationView } from "./annotation";
import { BBox } from "core/util/bbox";
export declare class LegendView extends AnnotationView {
    initialize(options: any): boolean;
    connect_signals(): any;
    compute_legend_bbox(): {
        x: any;
        y: any;
        width: any;
        height: any;
    };
    bbox(): BBox;
    on_hit(sx: any, sy: any): boolean;
    render(): any;
    _draw_legend_box(ctx: any, bbox: any): any;
    _draw_legend_items(ctx: any, bbox: any): null;
    _get_size(): any;
}
export declare class Legend extends Annotation {
    cursor(): "pointer" | null;
    get_legend_names(): any[];
}
