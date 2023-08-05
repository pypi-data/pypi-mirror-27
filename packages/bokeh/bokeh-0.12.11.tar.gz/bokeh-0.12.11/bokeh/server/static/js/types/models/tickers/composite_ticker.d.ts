import { ContinuousTicker } from "./continuous_ticker";
export declare class CompositeTicker extends ContinuousTicker {
    get_best_ticker(data_low: any, data_high: any, desired_n_ticks: any): any;
    get_interval(data_low: any, data_high: any, desired_n_ticks: any): any;
    get_ticks_no_defaults(data_low: any, data_high: any, cross_loc: any, desired_n_ticks: any): any;
}
