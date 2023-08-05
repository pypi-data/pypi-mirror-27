import { InspectTool } from "./inspect_tool";
import { Span } from "../../annotations/span";
export declare var CrosshairToolView: {
    new (options?: {}): {
        _move(e: any): any;
        _move_exit(e: any): any;
        _update_spans(x: any, y: any): any;
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
export declare class CrosshairTool extends InspectTool {
    initialize(attrs: any, options: any): {
        width: Span;
        height: Span;
    };
}
