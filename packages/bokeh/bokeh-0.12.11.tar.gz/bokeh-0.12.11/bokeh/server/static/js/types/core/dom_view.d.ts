import { View } from "./view";
export declare class DOMView extends View {
    initialize(options: any): HTMLElement;
    remove(): any;
    layout(): void;
    render(): void;
    renderTo(element: any, replace?: boolean): void;
    has_finished(): any;
    notify_finished(): any;
    _createElement(): HTMLElement;
}
