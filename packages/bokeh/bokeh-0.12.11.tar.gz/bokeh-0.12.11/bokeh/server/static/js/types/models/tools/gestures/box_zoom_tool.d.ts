import { GestureTool } from "./gesture_tool";
export declare var BoxZoomToolView: {
    new (options?: {}): {
        _match_aspect(base_point: any, curpoint: any, frame: any): any[][];
        _pan_start(e: any): null;
        _pan(e: any): null;
        _pan_end(e: any): null;
        _update([sx0, sx1]: [any, any], [sy0, sy1]: [any, any]): any;
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
export declare class BoxZoomTool extends GestureTool {
}
