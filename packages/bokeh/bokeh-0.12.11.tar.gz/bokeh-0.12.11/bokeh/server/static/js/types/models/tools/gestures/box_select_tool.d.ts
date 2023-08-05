import { SelectTool } from "./select_tool";
export declare var BoxSelectToolView: {
    new (options?: {}): {
        _pan_start(e: any): null;
        _pan(e: any): null;
        _pan_end(e: any): null;
        _do_select([sx0, sx1]: [any, any], [sy0, sy1]: [any, any], final: any, append?: boolean): null;
        _emit_callback(geometry: any): void;
        _computed_renderers_by_data_source(): {};
        _keyup(e: any): any[] | undefined;
        _select(geometry: any, final: any, append: any): null;
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
export declare class BoxSelectTool extends SelectTool {
}
