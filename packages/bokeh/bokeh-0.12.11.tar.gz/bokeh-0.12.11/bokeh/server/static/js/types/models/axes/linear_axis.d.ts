import { ContinuousAxis } from "./continuous_axis";
export declare var LinearAxisView: {
    new (options?: {}): {
        render(): any;
        connect_signals(): any;
        _get_size(): any;
        get_size(): number;
        _draw_rule(ctx: any, extents: any, tick_coords: any): void;
        _draw_major_ticks(ctx: any, extents: any, tick_coords: any): void;
        _draw_minor_ticks(ctx: any, extents: any, tick_coords: any): void;
        _draw_major_labels(ctx: any, extents: any, tick_coords: any): void;
        _draw_axis_label(ctx: any, extents: any, tick_coords: any): void;
        _draw_ticks(ctx: any, coords: any, tin: any, tout: any, visuals: any): void;
        _draw_oriented_labels(ctx: any, labels: any, coords: any, orient: any, side: any, standoff: any, visuals: any, units?: string): void;
        _axis_label_extent(): number;
        _tick_extent(): any;
        _tick_label_extent(): number;
        _tick_label_extent(): number;
        _tick_label_extents(): number[];
        _oriented_labels_extent(labels: any, orient: any, side: any, standoff: any, visuals: any): number;
        initialize(options: any): boolean;
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
export declare class LinearAxis extends ContinuousAxis {
}
