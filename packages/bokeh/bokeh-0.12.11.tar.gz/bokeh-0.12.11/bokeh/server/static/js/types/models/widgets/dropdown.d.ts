import { AbstractButton } from "./abstract_button";
export declare var DropdownView: {
    new (options?: {}): {
        connect_signals(): boolean;
        render(): any;
        _clear_menu(): boolean;
        _toggle_menu(): true | undefined;
        _button_click(event: any): any;
        _caret_click(event: any): true | undefined;
        _item_click(event: any): any;
        set_value(value: any): any;
        initialize(options: any): any;
        remove(): any;
        _render_button(...children: any[]): HTMLElement;
        change_input(): any;
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
export declare class Dropdown extends AbstractButton {
}
