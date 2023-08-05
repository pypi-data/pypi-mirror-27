export declare type HTMLAttrs = {
    [name: string]: any;
};
export declare type HTMLChild = string | HTMLElement | (string | HTMLElement)[];
export declare function createElement(tag: string, attrs: HTMLAttrs, ...children: HTMLChild[]): HTMLElement;
export declare const div: (attrs?: HTMLAttrs, ...children: HTMLChild[]) => HTMLElement, span: (attrs?: HTMLAttrs, ...children: HTMLChild[]) => HTMLElement, link: (attrs?: HTMLAttrs, ...children: HTMLChild[]) => HTMLElement, style: (attrs?: HTMLAttrs, ...children: HTMLChild[]) => HTMLElement, a: (attrs?: HTMLAttrs, ...children: HTMLChild[]) => HTMLElement, p: (attrs?: HTMLAttrs, ...children: HTMLChild[]) => HTMLElement, pre: (attrs?: HTMLAttrs, ...children: HTMLChild[]) => HTMLElement, button: (attrs?: HTMLAttrs, ...children: HTMLChild[]) => HTMLElement, label: (attrs?: HTMLAttrs, ...children: HTMLChild[]) => HTMLElement, input: (attrs?: HTMLAttrs, ...children: HTMLChild[]) => HTMLElement, select: (attrs?: HTMLAttrs, ...children: HTMLChild[]) => HTMLElement, option: (attrs?: HTMLAttrs, ...children: HTMLChild[]) => HTMLElement, optgroup: (attrs?: HTMLAttrs, ...children: HTMLChild[]) => HTMLElement, canvas: (attrs?: HTMLAttrs, ...children: HTMLChild[]) => HTMLElement, ul: (attrs?: HTMLAttrs, ...children: HTMLChild[]) => HTMLElement, ol: (attrs?: HTMLAttrs, ...children: HTMLChild[]) => HTMLElement, li: (attrs?: HTMLAttrs, ...children: HTMLChild[]) => HTMLElement;
export declare const nbsp: Text;
export declare function removeElement(element: HTMLElement): void;
export declare function replaceWith(element: HTMLElement, replacement: HTMLElement): void;
export declare function prepend(element: HTMLElement, ...nodes: HTMLElement[]): void;
export declare function empty(element: HTMLElement): void;
export declare function show(element: HTMLElement): void;
export declare function hide(element: HTMLElement): void;
export declare function position(element: HTMLElement): {
    top: number;
    left: number;
};
export declare function offset(element: HTMLElement): {
    top: number;
    left: number;
};
export declare function matches(el: HTMLElement, selector: string): boolean;
export declare function parent(el: HTMLElement, selector: string): HTMLElement | null;
export declare enum Keys {
    Tab = 9,
    Enter = 13,
    Esc = 27,
    PageUp = 33,
    PageDown = 34,
    Up = 38,
    Down = 40,
}
