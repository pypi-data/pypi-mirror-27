export declare class BaseGLGlyph {
    constructor(gl: any, glyph: any);
    set_data_changed(n: any): boolean;
    set_visuals_changed(): boolean;
    render(ctx: any, indices: any, mainglyph: any): boolean;
}
export declare var line_width: (width: any) => any;
export declare var fill_array_with_float: (n: any, val: any) => Float32Array;
export declare var fill_array_with_vec: (n: any, m: any, val: any) => Float32Array;
export declare var visual_prop_is_singular: (visual: any, propname: any) => boolean;
export declare var attach_float: (prog: any, vbo: any, att_name: any, n: any, visual: any, name: any) => any;
export declare var attach_color: (prog: any, vbo: any, att_name: any, n: any, visual: any, prefix: any) => any;
