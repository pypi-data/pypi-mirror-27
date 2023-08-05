import { SelectTool } from "./select_tool";
export declare var TapToolView: {
    new (options?: {}): {
        _tap(e: any): null;
        _select(sx: any, sy: any, final: any, append: any): null;
        _computed_renderers_by_data_source(): {};
        _keyup(e: any): any[] | undefined;
        _emit_selection_event(geometry: any, final?: boolean): any;
        initialize(options: any): any;
        connect_signals(): any;
        activate(): void;
        deactivate(): void;
        remove(): any;
        toString(): string;
        disconnect_signals(): void;
    };
    getters(specs: any): any[];
};
export declare class TapTool extends SelectTool {
}
