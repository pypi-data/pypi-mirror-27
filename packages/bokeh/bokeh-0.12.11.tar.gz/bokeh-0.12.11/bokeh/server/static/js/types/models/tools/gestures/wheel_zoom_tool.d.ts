import { GestureTool } from "./gesture_tool";
export declare var WheelZoomToolView: {
    new (options?: {}): {
        _pinch(e: any): null;
        _scroll(e: any): null;
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
export declare class WheelZoomTool extends GestureTool {
}
