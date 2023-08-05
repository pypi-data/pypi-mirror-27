import { TextAnnotation } from "./text_annotation";
import * as Visuals from "core/visuals";
export declare var TitleView: {
    new (options?: {}): {
        initialize(options: any): Visuals.Text;
        _get_location(): any[];
        render(): any;
        _get_size(): any;
        connect_signals(): any;
        _calculate_text_dimensions(ctx: any, text: any): any[];
        _calculate_bounding_box_dimensions(ctx: any, text: any): any[];
        _canvas_text(ctx: any, text: any, sx: any, sy: any, angle: any): any;
        _css_text(ctx: any, text: any, sx: any, sy: any, angle: any): void;
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
export declare class Title extends TextAnnotation {
}
