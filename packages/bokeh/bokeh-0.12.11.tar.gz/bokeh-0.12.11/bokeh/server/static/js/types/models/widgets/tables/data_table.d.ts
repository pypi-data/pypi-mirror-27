import { TableWidget } from "./table_widget";
import { WidgetView } from "../widget";
export declare var DTINDEX_NAME: string;
export declare var DataProvider: {
    new (source: any, view: any): {
        getLength(): any;
        getItem(offset: any): {};
        setItem(offset: any, item: any): null;
        getField(offset: any, field: any): any;
        setField(offset: any, field: any, value: any): null;
        getItemMetadata(index: any): null;
        getRecords(): any;
        sort(columns: any): any;
        _update_source_inplace(): void;
    };
};
export declare class DataTableView extends WidgetView {
    initialize(options: any): boolean;
    connect_signals(): any;
    updateGrid(): any;
    updateSelection(): any;
    newIndexColumn(): {
        id: string;
        name: string;
        field: string;
        width: number;
        behavior: string;
        cannotTriggerInsert: boolean;
        resizable: boolean;
        selectable: boolean;
        sortable: boolean;
        cssClass: string;
    };
    render(): this;
}
export declare class DataTable extends TableWidget {
}
