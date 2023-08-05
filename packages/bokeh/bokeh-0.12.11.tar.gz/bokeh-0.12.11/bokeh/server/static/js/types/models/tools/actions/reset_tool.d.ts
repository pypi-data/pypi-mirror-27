import { ActionTool } from "./action_tool";
export declare var ResetToolView: {
    new (options?: {}): {
        doit(): any;
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
export declare class ResetTool extends ActionTool {
}
