import { AdaptiveTicker } from "./adaptive_ticker";
export declare class LogTicker extends AdaptiveTicker {
    get_ticks_no_defaults(data_low: any, data_high: any, cross_loc: any, desired_n_ticks: any): {
        major: any[];
        minor: number[];
    };
}
