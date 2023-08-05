import { Model } from "../../model";
export declare class Ticker extends Model {
    get_ticks(data_low: any, data_high: any, range: any, cross_loc: any, {desired_n_ticks}: {
        desired_n_ticks: any;
    }): {
        "major": number[];
        "minor": number[];
    };
    get_ticks_no_defaults(data_low: any, data_high: any, cross_loc: any, desired_n_ticks: any): {
        "major": number[];
        "minor": number[];
    };
}
