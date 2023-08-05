import { Annotation } from "./annotation";
export declare var BandView: {
    new (options?: {}): {
        initialize(options: any): any;
        connect_signals(): any;
        set_data(source: any): any;
        _map_data(): any;
        render(): any;
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
export declare class Band extends Annotation {
}
