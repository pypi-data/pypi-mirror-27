import { RBush } from "core/util/spatial";
import { Glyph } from "./glyph";
import * as hittest from "core/hittest";
export declare var PatchesView: {
    new (options?: {}): {
        _build_discontinuous_object(nanned_qs: any): {};
        _index_data(): RBush;
        _mask_data(all_indices: any): any;
        _render(ctx: any, indices: any, {sxs, sys}: {
            sxs: any;
            sys: any;
        }): any[];
        _hit_point(geometry: any): hittest.HitTestResult;
        _get_snap_coord(array: any): number;
        scx(i: any, sx: any, sy: any): number | null;
        scy(i: any, sx: any, sy: any): number | undefined;
        draw_legend_for_index(ctx: any, x0: any, x1: any, y0: any, y1: any, index: any): any;
        initialize(options: any): any;
        set_visuals(source: any): any;
        render(ctx: any, indices: any, data: any): any;
        has_finished(): boolean;
        notify_finished(): any;
        bounds(): any;
        log_bounds(): any;
        max_wh2_bounds(bds: any): {
            minX: number;
            maxX: any;
            minY: number;
            maxY: any;
        };
        get_anchor_point(anchor: any, i: any, [sx, sy]: [any, any]): {
            x: any;
            y: any;
        } | null;
        sdist(scale: any, pts: any, spans: any, pts_location?: string, dilate?: boolean): number[];
        _generic_line_legend(ctx: any, x0: any, x1: any, y0: any, y1: any, index: any): any;
        _generic_area_legend(ctx: any, x0: any, x1: any, y0: any, y1: any, index: any): any;
        hit_test(geometry: any): any;
        _hit_rect_against_index(geometry: any): hittest.HitTestResult;
        set_data(source: any, indices: any, indices_to_update: any): void;
        _set_data(): void;
        mask_data(indices: any): any;
        _bounds(bounds: any): any;
        map_data(): void;
        _map_data(): void;
        map_to_screen(x: any, y: any): any;
        remove(): any;
        toString(): string;
        connect_signals(): void;
        disconnect_signals(): void;
    };
    getters(specs: any): any[];
};
export declare class Patches extends Glyph {
}
