import { Renderer } from "../renderers/renderer";
export declare var DynamicImageView: {
    new (): {
        connect_signals(): any;
        get_extent(): any[];
        _set_data(): any[];
        _map_data(): any[];
        _on_image_load(e: any): any;
        _on_image_error(e: any): any;
        _create_image(bounds: any): HTMLImageElement;
        render(ctx: any, indices: any, args: any): number | undefined;
        _draw_image(image_key: any): any;
        _set_rect(): any;
        initialize(options: any): boolean;
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
export declare class DynamicImageRenderer extends Renderer {
}
