import { GestureTool } from "./gesture_tool";
export declare var PanToolView: {
    new (options?: {}): {
        _pan_start(e: any): any;
        _pan(e: any): any;
        _pan_end(e: any): any;
        _update(dx: any, dy: any): null;
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
export declare class PanTool extends GestureTool {
}
