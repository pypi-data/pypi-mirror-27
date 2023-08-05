import { LayoutCanvas } from "core/layout/layout_canvas";
import { DOMView } from "core/dom_view";
export declare class CanvasView extends DOMView {
    initialize(options: any): void;
    get_ctx(): any;
    get_canvas_element(): any;
    prepare_canvas(): void;
    set_dims([width, height]: [any, any]): any;
}
export declare class Canvas extends LayoutCanvas {
}
