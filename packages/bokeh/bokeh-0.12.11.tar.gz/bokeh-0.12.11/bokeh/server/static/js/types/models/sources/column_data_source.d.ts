import { ColumnarDataSource } from "./columnar_data_source";
import { Set } from "core/util/data_structures";
export declare var concat_typed_arrays: (a: any, b: any) => any;
export declare var stream_to_column: (col: any, new_col: any, rollover: any) => any;
export declare var slice: (ind: any, length: any) => any[];
export declare var patch_to_column: (col: any, patch: any, shapes: any) => Set<{}>;
export declare class ColumnDataSource extends ColumnarDataSource {
    initialize(options: any): any;
    attributes_as_json(include_defaults?: boolean, value_to_json?: typeof ColumnDataSource._value_to_json): any;
    static _value_to_json(key: any, value: any, optional_parent_object: any): any;
    stream(new_data: any, rollover: any): any;
    patch(patches: any): any;
}
