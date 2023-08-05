import { ButtonTool } from "../button_tool";
export declare var GestureToolView: {
    new (options?: {}): {
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
export declare class GestureTool extends ButtonTool {
}
