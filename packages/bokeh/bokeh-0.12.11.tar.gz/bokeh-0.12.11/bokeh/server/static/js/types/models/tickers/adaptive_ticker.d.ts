import { ContinuousTicker } from "./continuous_ticker";
export declare class AdaptiveTicker extends ContinuousTicker {
    initialize(attrs: any, options: any): any;
    get_interval(data_low: any, data_high: any, desired_n_ticks: any): any;
}
