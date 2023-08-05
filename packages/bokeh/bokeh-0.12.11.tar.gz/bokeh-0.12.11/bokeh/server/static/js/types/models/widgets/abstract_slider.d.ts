import { Widget } from "./widget";
export declare var AbstractSliderView: {
    new (options?: {}): {
        initialize(options: any): any;
        connect_signals(): any;
        _calc_to(): void;
        _calc_from(values: any): void;
        render(): any;
        _slide(values: any): any;
        _change(values: any): any;
        remove(): any;
        has_finished(): boolean;
        notify_finished(): any;
        _calc_width_height(): any[];
        _init_solver(): boolean;
        _suggest_dims(width: any, height: any): any;
        resize(width?: null, height?: null): any;
        partial_layout(): any;
        layout(full?: boolean): any;
        _do_layout(full: any, width?: null, height?: null): any;
        _layout(final?: boolean): true | undefined;
        rebuild_child_views(): any;
        build_child_views(): any[];
        _render_classes(): any[] | undefined;
        position(): string;
        get_height(): void;
        get_width(): void;
        get_width_height(): any[];
        renderTo(element: any, replace?: boolean): void;
        _createElement(): HTMLElement;
        toString(): string;
        disconnect_signals(): void;
    };
    getters(specs: any): any[];
};
export declare class AbstractSlider extends Widget {
    _formatter(value: any, format: any): string;
    pretty(value: any): string;
}
