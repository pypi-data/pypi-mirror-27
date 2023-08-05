import { Model } from "../../../model";
export declare class TableColumn extends Model {
    toColumn(): {
        id: string;
        field: any;
        name: any;
        width: any;
        formatter: any;
        editor: any;
        sortable: any;
        defaultSortAsc: boolean;
    };
}
