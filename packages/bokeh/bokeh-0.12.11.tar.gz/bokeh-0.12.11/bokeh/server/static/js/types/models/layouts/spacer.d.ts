import { LayoutDOM, LayoutDOMView } from "./layout_dom";
export declare class SpacerView extends LayoutDOMView {
    render(): string | undefined;
    get_height(): number;
}
export declare class Spacer extends LayoutDOM {
    get_constrained_variables(): any;
}
