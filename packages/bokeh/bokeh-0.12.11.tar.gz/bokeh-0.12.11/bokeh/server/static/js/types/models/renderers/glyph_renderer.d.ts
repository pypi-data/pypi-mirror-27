import { Renderer } from "./renderer";
export declare var GlyphRendererView: {
    new (options?: {}): {
        initialize(options: any): any;
        build_glyph_view(model: any): any;
        connect_signals(): any;
        have_selection_glyphs(): boolean;
        set_data(request_render: boolean | undefined, indices: any): any;
        render(): any;
        draw_legend(ctx: any, x0: any, x1: any, y0: any, y1: any, field: any, label: any): any;
        hit_test(geometry: any, final: any, append: any, mode?: string): any;
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
export declare class GlyphRenderer extends Renderer {
    initialize(options: any): any;
    get_reference_point(field: any, value: any): any;
    hit_test_helper(geometry: any, renderer_view: any, final: any, append: any, mode: any): boolean;
    get_selection_manager(): any;
}
