import { ToolbarBase } from "./toolbar_base";
import { LayoutDOM, LayoutDOMView } from "../layouts/layout_dom";
export declare class ProxyToolbar extends ToolbarBase {
    initialize(options: any): (boolean | undefined)[];
    _init_tools(): any[];
    _merge_tools(): (boolean | undefined)[];
}
export declare class ToolbarBoxView extends LayoutDOMView {
    initialize(options: any): any[];
    remove(): any;
    render(): any;
    get_width(): 30 | null;
    get_height(): 30 | null;
}
export declare class ToolbarBox extends LayoutDOM {
}
