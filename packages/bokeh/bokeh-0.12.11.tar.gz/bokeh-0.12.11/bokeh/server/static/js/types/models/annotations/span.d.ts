import { Annotation } from "./annotation";
export declare var SpanView: {
    new (options?: {}): {
        initialize(options: any): void;
        connect_signals(): any;
        render(): any;
        _draw_span(): any;
        _get_size(): Error;
        get_size(): any;
        request_render(): any;
        set_data(source: any): [number[][], number[][]] | undefined;
        map_to_screen(x: any, y: any): any;
        remove(): any;
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
export declare class Span extends Annotation {
}
