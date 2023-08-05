import { Annotation, AnnotationView } from "./annotation";
export declare class TooltipView extends AnnotationView {
    initialize(options: any): void;
    connect_signals(): any;
    render(): string | void;
    _draw_tips(): string | void;
}
export declare class Tooltip extends Annotation {
    clear(): never[];
    add(sx: any, sy: any, content: any): any;
}
