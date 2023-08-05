import { DOMView } from "core/dom_view";
import { Model } from "../../model";
export declare class RendererView extends DOMView {
    initialize(options: any): boolean;
    request_render(): any;
    set_data(source: any): [number[][], number[][]] | undefined;
    map_to_screen(x: any, y: any): any;
}
export declare class Renderer extends Model {
}
