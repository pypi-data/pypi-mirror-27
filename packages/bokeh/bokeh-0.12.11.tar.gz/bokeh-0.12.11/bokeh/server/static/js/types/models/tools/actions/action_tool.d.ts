import { ButtonTool } from "../button_tool";
import { Signal } from "core/signaling";
export declare var ActionToolButtonView: {
    new (options?: {}): {
        _clicked(): any;
        initialize(options: any): any;
        render(): any;
        remove(): any;
        layout(): void;
        renderTo(element: any, replace?: boolean): void;
        has_finished(): any;
        notify_finished(): any;
        _createElement(): HTMLElement;
        toString(): string;
        connect_signals(): void;
        disconnect_signals(): void;
    };
    getters(specs: any): any[];
};
export declare var ActionToolView: {
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
export declare class ActionTool extends ButtonTool {
    initialize(attrs: any, options: any): Signal<{}, this>;
}
