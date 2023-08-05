import { HasProps } from "./core/has_props";
export declare class Model extends HasProps {
    connect_signals(): any;
    _process_event(event: any): any;
    trigger_event(event: any): any;
    _update_event_callbacks(): any;
    _doc_attached(): any;
    select(selector: any): {}[];
    select_one(selector: any): {} | null;
}
