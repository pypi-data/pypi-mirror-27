import { Annotation } from "./annotation";
export declare class ArrowHead extends Annotation {
    initialize(options: any): {
        warm_cache(source: any): any[];
        set_all_indices(all_indices: any): any[];
    };
    render(ctx: any, i: any): null;
    clip(ctx: any, i: any): null;
}
export declare class OpenHead extends ArrowHead {
    clip(ctx: any, i: any): any;
    render(ctx: any, i: any): any;
}
export declare class NormalHead extends ArrowHead {
    clip(ctx: any, i: any): any;
    render(ctx: any, i: any): any;
    _normal(ctx: any, i: any): any;
}
export declare class VeeHead extends ArrowHead {
    clip(ctx: any, i: any): any;
    render(ctx: any, i: any): any;
    _vee(ctx: any, i: any): any;
}
export declare class TeeHead extends ArrowHead {
    render(ctx: any, i: any): any;
}
