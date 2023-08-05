import { Renderer } from "../renderers/renderer";
export declare var AnnotationView: {
    new (options?: {}): {
        _get_size(): Error;
        get_size(): any;
        initialize(options: any): boolean;
        request_render(): any;
        set_data(source: any): [number[][], number[][]] | undefined;
        map_to_screen(x: any, y: any): any;
        remove(): any;
        layout(): void;
        render(): void;
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
export declare class Annotation extends Renderer {
    add_panel(side: any): string | undefined;
    set_panel(panel: any): string;
}
