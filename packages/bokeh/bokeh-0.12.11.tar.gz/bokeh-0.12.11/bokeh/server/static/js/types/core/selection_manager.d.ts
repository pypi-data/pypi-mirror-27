import { HasProps } from "./has_props";
import * as hittest from "./hittest";
export declare class SelectionManager extends HasProps {
    initialize(attrs: any, options: any): {};
    select(renderer_views: any, geometry: any, final: any, append?: boolean): any;
    inspect(renderer_view: any, geometry: any): any;
    clear(rview: any): hittest.HitTestResult;
    get_or_create_inspector(rmodel: any): any;
}
