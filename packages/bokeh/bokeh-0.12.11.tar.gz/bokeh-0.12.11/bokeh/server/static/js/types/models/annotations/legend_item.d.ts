import { Model } from "../../model";
export declare class LegendItem extends Model {
    constructor();
    _check_data_sources_on_renderers(): boolean;
    _check_field_label_on_data_source(): boolean;
    initialize(attrs: any, options: any): void;
    get_field_from_label_prop(): any;
    get_labels_list_from_label_prop(): any[];
}
