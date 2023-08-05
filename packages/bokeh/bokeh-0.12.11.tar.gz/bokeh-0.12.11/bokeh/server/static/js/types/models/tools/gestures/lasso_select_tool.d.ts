import { SelectTool } from "./select_tool";
export declare var LassoSelectToolView: {
    new (options?: {}): {
        initialize(options: any): null;
        _active_change(): any;
        _keyup(e: any): any;
        _pan_start(e: any): null;
        _pan(e: any): null | undefined;
        _pan_end(e: any): any;
        _clear_overlay(): any;
        _do_select(sx: any, sy: any, final: any, append: any): null;
        _emit_callback(geometry: any): void;
        _computed_renderers_by_data_source(): {};
        _select(geometry: any, final: any, append: any): null;
        _emit_selection_event(geometry: any, final?: boolean): any;
        connect_signals(): any;
        activate(): void;
        deactivate(): void;
        remove(): any;
        toString(): string;
        disconnect_signals(): void;
    };
    getters(specs: any): any[];
};
export declare class LassoSelectTool extends SelectTool {
}
