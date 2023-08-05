import { SingleIntervalTicker } from "./single_interval_ticker";
export declare class MonthsTicker extends SingleIntervalTicker {
    initialize(attrs: any, options: any): number;
    get_ticks_no_defaults(data_low: any, data_high: any, cross_loc: any, desired_n_ticks: any): {
        "major": any[];
        "minor": never[];
    };
}
