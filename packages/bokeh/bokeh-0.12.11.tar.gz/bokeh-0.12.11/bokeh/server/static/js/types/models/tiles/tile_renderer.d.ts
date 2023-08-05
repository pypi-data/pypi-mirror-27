import { Renderer } from "../renderers/renderer";
export declare var TileRendererView: {
    new (): {
        initialize(options: any): boolean;
        connect_signals(): any;
        get_extent(): any[];
        _set_data(): undefined;
        _add_attribution(): string | undefined;
        _map_data(): string | undefined;
        _on_tile_load(e: any): any;
        _on_tile_cache_load(e: any): any;
        _on_tile_error(e: any): boolean;
        _create_tile(x: any, y: any, z: any, bounds: any, cache_only?: boolean): any;
        _enforce_aspect_ratio(): boolean;
        has_finished(): boolean;
        render(ctx: any, indices: any, args: any): any;
        _draw_tile(tile_key: any): any;
        _set_rect(): any;
        _render_tiles(tile_keys: any): any;
        _prefetch_tiles(): any[];
        _fetch_tiles(tiles: any): any[];
        _update(): number;
        request_render(): any;
        set_data(source: any): [number[][], number[][]] | undefined;
        map_to_screen(x: any, y: any): any;
        remove(): any;
        layout(): void;
        renderTo(element: any, replace?: boolean): void;
        notify_finished(): any;
        _createElement(): HTMLElement;
        toString(): string;
        disconnect_signals(): void;
    };
    getters(specs: any): any[];
};
export declare class TileRenderer extends Renderer {
}
