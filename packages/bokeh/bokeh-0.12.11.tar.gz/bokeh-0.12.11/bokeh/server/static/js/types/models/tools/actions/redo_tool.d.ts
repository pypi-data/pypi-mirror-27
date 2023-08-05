import { ActionTool } from "./action_tool";
export declare var RedoToolView: {
    new (options?: {}): {
        initialize(options: any): any;
        doit(): any;
        connect_signals(): any;
        activate(): void;
        deactivate(): void;
        remove(): any;
        toString(): string;
        disconnect_signals(): void;
    };
    getters(specs: any): any[];
};
export declare class RedoTool extends ActionTool {
}
