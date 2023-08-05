import { Transform } from "../transforms/transform";
export declare class ColorMapper extends Transform {
    initialize(attrs: any, options: any): any;
    v_map_screen(data: any, image_glyph?: boolean): ArrayBuffer;
    compute(x: any): null;
    v_compute(xs: any): never[];
    _get_values(data: any, palette: any, image_glyph?: boolean): never[];
    _is_little_endian(): boolean;
    _build_palette(palette: any): Uint32Array;
}
