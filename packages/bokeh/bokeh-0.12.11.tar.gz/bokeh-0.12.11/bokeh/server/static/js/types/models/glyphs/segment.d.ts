import * as hittest from "core/hittest";
import { RBush } from "core/util/spatial";
import { Glyph } from "./glyph";
export declare var SegmentView: {
    new (options?: {}): {
        _index_data(): RBush;
        _render(ctx: any, indices: any, {sx0, sy0, sx1, sy1}: {
            sx0: any;
            sy0: any;
            sx1: any;
            sy1: any;
        }): any[] | undefined;
        _hit_point(geometry: any): hittest.HitTestResult;
        _hit_span(geometry: any): hittest.HitTestResult;
        scx(i: any): number;
        scy(i: any): number;
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
        _mask_data(indices: any): any;
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
export declare class Segment extends Glyph {
}
