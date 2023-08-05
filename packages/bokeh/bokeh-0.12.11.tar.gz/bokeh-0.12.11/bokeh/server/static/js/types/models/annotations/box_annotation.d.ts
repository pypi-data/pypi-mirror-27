import { Annotation } from "./annotation";
import { Signal } from "core/signaling";
export declare var BoxAnnotationView: {
    new (options?: {}): {
        initialize(options: any): void;
        connect_signals(): any;
        render(): any;
        _css_box(sleft: any, sright: any, sbottom: any, stop: any): void;
        _canvas_box(sleft: any, sright: any, sbottom: any, stop: any): any;
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
export declare class BoxAnnotation extends Annotation {
    initialize(attrs: any, options: any): Signal<{}, this>;
    update({left, right, top, bottom}: {
        left: any;
        right: any;
        top: any;
        bottom: any;
    }): any;
}
