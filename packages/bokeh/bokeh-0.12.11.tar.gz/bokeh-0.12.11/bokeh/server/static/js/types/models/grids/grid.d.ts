import { GuideRenderer } from "../renderers/guide_renderer";
export declare var GridView: {
    new (options?: {}): {
        initialize(attrs: any, options: any): any;
        render(): any;
        connect_signals(): any;
        _draw_regions(ctx: any): void;
        _draw_grids(ctx: any): void;
        _draw_minor_grids(ctx: any): void;
        _draw_grid_helper(ctx: any, props: any, xs: any, ys: any): void;
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
export declare class Grid extends GuideRenderer {
    ranges(): any[];
    computed_bounds(): any[];
    grid_coords(location: any, exclude_ends?: boolean): never[][];
}
