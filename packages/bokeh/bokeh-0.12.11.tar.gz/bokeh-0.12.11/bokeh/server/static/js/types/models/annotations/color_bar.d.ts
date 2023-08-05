import { Annotation } from "./annotation";
import { LinearScale } from "../scales/linear_scale";
export declare var ColorBarView: {
    new (options?: {}): {
        initialize(options: any): HTMLCanvasElement | undefined;
        connect_signals(): any;
        _get_size(): any;
        _set_canvas_image(): HTMLCanvasElement | undefined;
        compute_legend_dimensions(): {
            height: any;
            width: any;
        };
        compute_legend_location(): {
            sx: any;
            sy: any;
        };
        render(): any;
        _draw_bbox(ctx: any): any;
        _draw_image(ctx: any): any;
        _draw_major_ticks(ctx: any, tick_info: any): any;
        _draw_minor_ticks(ctx: any, tick_info: any): any;
        _draw_major_labels(ctx: any, tick_info: any): any;
        _draw_title(ctx: any): any;
        _get_label_extent(): number | undefined;
        _get_image_offset(): {
            x: any;
            y: any;
        };
        get_size(): any;
        request_render(): any;
        set_data(source: any): [number[][], number[][]] | undefined;
        map_to_screen(x: any, y: any): any;
        remove(): any;
        layout(): void;
        renderTo(element: any, replace?: boolean): void;
        has_finished(): any;
        notify_finished(): any;
        _createElement(): HTMLElement;
        toString(): string;
        disconnect_signals(): void;
    };
    getters(specs: any): any[];
};
export declare class ColorBar extends Annotation {
    initialize(attrs: any, options: any): void;
    _normals(): number[];
    _title_extent(): any;
    _tick_extent(): number;
    _computed_image_dimensions(): {
        "height": any;
        "width": any;
    };
    _tick_coordinate_scale(scale_length: any): LinearScale | undefined;
    _format_major_labels(initial_labels: any, major_ticks: any): any;
    tick_info(): {
        "ticks": any;
        "coords": {
            major: never[][];
            minor: never[][];
        };
        "labels": {
            major: any;
        };
    };
}
