import { SelectTool } from "./select_tool";
export declare var PolySelectToolView: {
    new (options?: {}): {
        initialize(options: any): {
            sx: never[];
            sy: never[];
        };
        _active_change(): any;
        _keyup(e: any): any;
        _doubletap(e: any): any;
        _clear_data(): any;
        _tap(e: any): any;
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
export declare class PolySelectTool extends SelectTool {
}
