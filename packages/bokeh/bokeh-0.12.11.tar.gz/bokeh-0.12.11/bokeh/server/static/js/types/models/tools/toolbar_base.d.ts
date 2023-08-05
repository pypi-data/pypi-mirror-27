import { Model } from "model";
export declare var ToolbarBaseView: {
    new (options?: {}): {
        initialize(options: any): any[];
        connect_signals(): any;
        remove(): any;
        _build_tool_button_views(): any[];
        render(): any;
        layout(): void;
        renderTo(element: any, replace?: boolean): void;
        has_finished(): any;
        notify_finished(): any;
        _createElement(): HTMLElement;
        toString(): string;
        disconnect_signals(): void;
    };
    getters(specs: any): any[];
};
export declare class ToolbarBase extends Model {
    _active_change(tool: any): null;
}
