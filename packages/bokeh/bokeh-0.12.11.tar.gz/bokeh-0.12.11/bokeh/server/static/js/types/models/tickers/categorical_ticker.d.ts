import { Ticker } from "./ticker";
export declare class CategoricalTicker extends Ticker {
    get_ticks(start: any, end: any, range: any, cross_loc: any, {desired_n_ticks}: {
        desired_n_ticks: any;
    }): {
        major: any[];
        tops: any[];
        mids: any[];
        minor: never[];
    };
    _collect(factors: any, range: any, start: any, end: any): any[];
}
