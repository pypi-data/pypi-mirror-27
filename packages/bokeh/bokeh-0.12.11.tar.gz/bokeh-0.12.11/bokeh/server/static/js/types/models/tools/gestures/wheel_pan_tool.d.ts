import { GestureTool } from "./gesture_tool";
export declare var WheelPanToolView: {
    new (options?: {}): {
        _scroll(e: any): null;
        _update_ranges(factor: any): null;
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
export declare class WheelPanTool extends GestureTool {
}
