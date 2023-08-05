import { DOMView } from "core/dom_view";
import { Tool } from "./tool";
export declare class ButtonToolButtonView extends DOMView {
    initialize(options: any): any;
    render(): any;
    _clicked(): void;
}
export declare var ButtonToolView: {
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
export declare class ButtonTool extends Tool {
}
