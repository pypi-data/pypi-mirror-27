import { Renderer } from "../renderers/renderer";
export declare var GraphRendererView: {
    new (options?: {}): {
        initialize(options: any): any;
        connect_signals(): any;
        set_data(request_render?: boolean): any;
        render(): any;
        hit_test(geometry: any, final: any, append: any, mode?: string): any;
        request_render(): any;
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
export declare class GraphRenderer extends Renderer {
    get_selection_manager(): any;
}
