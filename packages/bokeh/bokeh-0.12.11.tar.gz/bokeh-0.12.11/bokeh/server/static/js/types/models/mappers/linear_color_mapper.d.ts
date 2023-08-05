import { ColorMapper } from "./color_mapper";
export declare class LinearColorMapper extends ColorMapper {
    initialize(attrs: any, options: any): number | undefined;
    _get_values(data: any, palette: any, image_glyph?: boolean): any[];
}
