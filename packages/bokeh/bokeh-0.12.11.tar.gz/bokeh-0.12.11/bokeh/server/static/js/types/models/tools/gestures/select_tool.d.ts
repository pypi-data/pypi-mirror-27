import { GestureTool, GestureToolView } from "./gesture_tool";
export declare class SelectToolView extends GestureToolView {
    _computed_renderers_by_data_source(): {};
    _keyup(e: any): any[] | undefined;
    _select(geometry: any, final: any, append: any): null;
    _emit_selection_event(geometry: any, final?: boolean): any;
}
export declare class SelectTool extends GestureTool {
}
