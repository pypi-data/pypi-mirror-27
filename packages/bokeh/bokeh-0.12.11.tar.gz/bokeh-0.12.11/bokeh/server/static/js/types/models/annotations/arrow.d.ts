import { Annotation } from "./annotation";
export declare var ArrowView: {
    new (options?: {}): {
        initialize(options: any): any;
        connect_signals(): any;
        set_data(source: any): any;
        _map_data(): any[][];
        render(): any;
        _arrow_body(ctx: any): any[] | undefined;
        _arrow_head(ctx: any, action: any, head: any, start: any, end: any): any[];
        _get_size(): Error;
        get_size(): any;
        request_render(): any;
        map_to_screen(x: any, y: any): any;
        remove(): any;
        layout(): void;
        renderTo(element: any, replace?: boolean): void;
        has_finished(): any;
        notify_finished(): any;
        _createElement(): HTMLElement;
        toString(): string;
        disconnect_signals(): void;
    };
    getters(specs: any): any[];
};
export declare class Arrow extends Annotation {
}
