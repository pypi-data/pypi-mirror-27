import { View } from "core/view";
import { Model } from "../../model";
export declare class ToolView extends View {
    initialize(options: any): any;
    connect_signals(): any;
    activate(): void;
    deactivate(): void;
}
export declare class Tool extends Model {
    _get_dim_tooltip(name: any, dims: any): any;
    _get_dim_limits([sx0, sy0]: [any, any], [sx1, sy1]: [any, any], frame: any, dims: any): any[][];
}
