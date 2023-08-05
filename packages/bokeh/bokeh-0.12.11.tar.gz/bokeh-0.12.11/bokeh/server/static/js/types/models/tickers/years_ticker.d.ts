import { BasicTicker } from "./basic_ticker";
import { SingleIntervalTicker } from "./single_interval_ticker";
export declare class YearsTicker extends SingleIntervalTicker {
    initialize(attrs: any, options: any): BasicTicker;
    get_ticks_no_defaults(data_low: any, data_high: any, cross_loc: any, desired_n_ticks: any): {
        major: number[];
        minor: never[];
    };
}
