import { Ticker } from "./ticker";
export declare class ContinuousTicker extends Ticker {
    get_min_interval(): any;
    get_max_interval(): any;
    get_ideal_interval(data_low: any, data_high: any, desired_n_ticks: any): number;
}
