import { ColumnarDataSource } from "./columnar_data_source";
export declare class GeoJSONDataSource extends ColumnarDataSource {
    initialize(options: any): any;
    _update_data(): {
        'x': number[];
        'y': number[];
        'z': number[];
        'xs': never[][];
        'ys': never[][];
        'zs': never[][];
    };
    _get_new_list_array(length: any): never[][];
    _get_new_nan_array(length: any): number[];
    _flatten_function(accumulator: any, currentItem: any): any;
    _add_properties(item: any, data: any, i: any, item_count: any): any[];
    _add_geometry(geometry: any, data: any, i: any): any;
    _get_items_length(items: any): number;
    geojson_to_column_data(): {
        'x': number[];
        'y': number[];
        'z': number[];
        'xs': never[][];
        'ys': never[][];
        'zs': never[][];
    };
}
