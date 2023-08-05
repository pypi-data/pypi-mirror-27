import { BasicTicker } from "./basic_ticker";
export declare class MercatorTicker extends BasicTicker {
    get_ticks_no_defaults(data_low: any, data_high: any, cross_loc: any, desired_n_ticks: any): {
        major: never[];
        minor: never[];
    };
}
