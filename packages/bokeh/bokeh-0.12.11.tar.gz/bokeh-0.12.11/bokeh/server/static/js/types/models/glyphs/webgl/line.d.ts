import { BaseGLGlyph } from "./base";
export declare class LineGLGlyph extends BaseGLGlyph {
    init(): any;
    draw(indices: any, mainGlyph: any, trans: any): any;
    _set_data(): any;
    _set_visuals(): any;
    _bake(): number[];
    _update_scale(sx: any, sy: any): any;
}
