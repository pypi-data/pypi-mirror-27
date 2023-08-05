import { ActionTool } from "./action_tool";
export declare var HelpToolView: {
    new (options?: {}): {
        doit(): Window | null;
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
export declare class HelpTool extends ActionTool {
}
