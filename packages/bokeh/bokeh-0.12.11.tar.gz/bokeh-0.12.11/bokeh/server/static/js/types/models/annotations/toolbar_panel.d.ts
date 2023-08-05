import { Annotation } from "./annotation";
export declare var ToolbarPanelView: {
    new (options?: {}): {
        initialize(options: any): any[];
        remove(): any;
        render(): void;
        _get_size(): number;
        get_size(): any;
        request_render(): any;
        set_data(source: any): [number[][], number[][]] | undefined;
        map_to_screen(x: any, y: any): any;
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
export declare class ToolbarPanel extends Annotation {
}
