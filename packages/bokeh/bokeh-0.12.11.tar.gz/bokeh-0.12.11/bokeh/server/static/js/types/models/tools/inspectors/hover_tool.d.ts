import { InspectTool, InspectToolView } from "./inspect_tool";
export declare var _nearest_line_hit: (i: any, geometry: any, sx: any, sy: any, dx: any, dy: any) => any[];
export declare var _line_hit: (xs: any, ys: any, ind: any) => any[];
export declare class HoverToolView extends InspectToolView {
    initialize(options: any): {};
    remove(): any;
    connect_signals(): any;
    _compute_renderers(): any;
    _compute_ttmodels(): {};
    _clear(): any[];
    _move(e: any): void | any[];
    _move_exit(): any[];
    _inspect(sx: any, sy: any): void;
    _update([renderer_view, {geometry}]: [any, {
        geometry: any;
    }]): null | undefined;
    _emit_callback(geometry: any): void;
    _render_tooltips(ds: any, i: any, vars: any): any;
}
export declare class HoverTool extends InspectTool {
}
