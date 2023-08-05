import { DataSource } from "./data_source";
import { Signal } from "core/signaling";
export declare class ColumnarDataSource extends DataSource {
    initialize(options: any): Signal<{}, this>;
    get_column(colname: any): any;
    columns(): string[];
    get_length(soft?: boolean): {} | null;
    get_indices(): any;
}
