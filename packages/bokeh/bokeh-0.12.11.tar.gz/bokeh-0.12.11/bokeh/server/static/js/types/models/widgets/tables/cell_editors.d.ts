import { DOMView } from "core/dom_view";
import { Model } from "../../../model";
export declare class CellEditorView extends DOMView {
    constructor(options: any);
    initialize(options: any): this;
    render(): this;
    renderEditor(): void;
    disableNavigation(): any;
    destroy(): any;
    focus(): any;
    show(): void;
    hide(): void;
    position(): void;
    getValue(): any;
    setValue(val: any): any;
    serializeValue(): any;
    isValueChanged(): boolean;
    applyValue(item: any, state: any): any;
    loadValue(item: any): any;
    validateValue(value: any): any;
    validate(): any;
}
export declare class CellEditor extends Model {
}
export declare class StringEditorView extends CellEditorView {
    renderEditor(): any;
    loadValue(item: any): any;
}
export declare class StringEditor extends CellEditor {
}
export declare var TextEditorView: {
    new (options: any): {
        initialize(options: any): any;
        render(): any;
        renderEditor(): void;
        disableNavigation(): any;
        destroy(): any;
        focus(): any;
        show(): void;
        hide(): void;
        position(): void;
        getValue(): any;
        setValue(val: any): any;
        serializeValue(): any;
        isValueChanged(): boolean;
        applyValue(item: any, state: any): any;
        loadValue(item: any): any;
        validateValue(value: any): any;
        validate(): any;
        remove(): any;
        layout(): void;
        renderTo(element: any, replace?: boolean): void;
        has_finished(): any;
        notify_finished(): any;
        _createElement(): HTMLElement;
        toString(): string;
        connect_signals(): void;
        disconnect_signals(): void;
    };
    getters(specs: any): any[];
};
export declare class TextEditor extends CellEditor {
}
export declare class SelectEditorView extends CellEditorView {
    renderEditor(): any;
    loadValue(item: any): any;
}
export declare class SelectEditor extends CellEditor {
}
export declare var PercentEditorView: {
    new (options: any): {
        initialize(options: any): any;
        render(): any;
        renderEditor(): void;
        disableNavigation(): any;
        destroy(): any;
        focus(): any;
        show(): void;
        hide(): void;
        position(): void;
        getValue(): any;
        setValue(val: any): any;
        serializeValue(): any;
        isValueChanged(): boolean;
        applyValue(item: any, state: any): any;
        loadValue(item: any): any;
        validateValue(value: any): any;
        validate(): any;
        remove(): any;
        layout(): void;
        renderTo(element: any, replace?: boolean): void;
        has_finished(): any;
        notify_finished(): any;
        _createElement(): HTMLElement;
        toString(): string;
        connect_signals(): void;
        disconnect_signals(): void;
    };
    getters(specs: any): any[];
};
export declare class PercentEditor extends CellEditor {
}
export declare class CheckboxEditorView extends CellEditorView {
    renderEditor(): any;
    loadValue(item: any): any;
    serializeValue(): any;
}
export declare class CheckboxEditor extends CellEditor {
}
export declare class IntEditorView extends CellEditorView {
    renderEditor(): any;
    remove(): any;
    serializeValue(): number;
    loadValue(item: any): any;
    validateValue(value: any): any;
}
export declare class IntEditor extends CellEditor {
}
export declare class NumberEditorView extends CellEditorView {
    renderEditor(): any;
    remove(): any;
    serializeValue(): number;
    loadValue(item: any): any;
    validateValue(value: any): any;
}
export declare class NumberEditor extends CellEditor {
}
export declare var TimeEditorView: {
    new (options: any): {
        initialize(options: any): any;
        render(): any;
        renderEditor(): void;
        disableNavigation(): any;
        destroy(): any;
        focus(): any;
        show(): void;
        hide(): void;
        position(): void;
        getValue(): any;
        setValue(val: any): any;
        serializeValue(): any;
        isValueChanged(): boolean;
        applyValue(item: any, state: any): any;
        loadValue(item: any): any;
        validateValue(value: any): any;
        validate(): any;
        remove(): any;
        layout(): void;
        renderTo(element: any, replace?: boolean): void;
        has_finished(): any;
        notify_finished(): any;
        _createElement(): HTMLElement;
        toString(): string;
        connect_signals(): void;
        disconnect_signals(): void;
    };
    getters(specs: any): any[];
};
export declare class TimeEditor extends CellEditor {
}
export declare class DateEditorView extends CellEditorView {
    renderEditor(): any;
    destroy(): any;
    show(): void;
    hide(): void;
    position(position: any): void;
    getValue(): void;
    setValue(val: any): void;
}
export declare class DateEditor extends CellEditor {
}
