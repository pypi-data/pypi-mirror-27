import { TextAnnotation } from "./text_annotation";
export declare var LabelSetView: {
    new (options?: {}): {
        initialize(options: any): any[] | undefined;
        connect_signals(): any;
        set_data(source: any): any;
        _map_data(): any[];
        render(): any[] | undefined;
        _get_size(): any;
        _v_canvas_text(ctx: any, i: any, text: any, sx: any, sy: any, angle: any): any;
        _v_css_text(ctx: any, i: any, text: any, sx: any, sy: any, angle: any): void;
        _calculate_text_dimensions(ctx: any, text: any): any[];
        _calculate_bounding_box_dimensions(ctx: any, text: any): any[];
        _canvas_text(ctx: any, text: any, sx: any, sy: any, angle: any): any;
        _css_text(ctx: any, text: any, sx: any, sy: any, angle: any): void;
        get_size(): any;
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
export declare class LabelSet extends TextAnnotation {
}
