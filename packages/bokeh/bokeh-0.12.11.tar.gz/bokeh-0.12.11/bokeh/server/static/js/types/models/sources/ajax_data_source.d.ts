import { RemoteDataSource } from "./remote_data_source";
export declare class AjaxDataSource extends RemoteDataSource {
    constructor();
    destroy(): void;
    setup(): number | undefined;
    get_data(mode: any, max_size?: number, if_modified?: boolean): null;
}
