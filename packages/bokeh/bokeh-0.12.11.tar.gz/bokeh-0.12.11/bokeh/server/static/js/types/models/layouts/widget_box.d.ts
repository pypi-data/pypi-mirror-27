import { LayoutDOM, LayoutDOMView } from "../layouts/layout_dom";
export declare class WidgetBoxView extends LayoutDOMView {
    connect_signals(): any;
    render(): string;
    get_height(): number;
    get_width(): any;
}
export declare class WidgetBox extends LayoutDOM {
    initialize(options: any): void;
    get_constrained_variables(): any;
    get_layoutable_children(): any;
}
