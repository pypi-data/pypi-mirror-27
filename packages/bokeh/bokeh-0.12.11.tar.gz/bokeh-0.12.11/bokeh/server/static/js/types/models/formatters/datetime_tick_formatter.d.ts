import { TickFormatter } from "./tick_formatter";
export declare class DatetimeTickFormatter extends TickFormatter {
    initialize(attrs: any, options: any): {
        microseconds: [any[], {}[]];
        milliseconds: [any[], {}[]];
        seconds: [any[], {}[]];
        minsec: [any[], {}[]];
        minutes: [any[], {}[]];
        hourmin: [any[], {}[]];
        hours: [any[], {}[]];
        days: [any[], {}[]];
        months: [any[], {}[]];
        years: [any[], {}[]];
    };
    _update_width_formats(): {
        microseconds: [any[], {}[]];
        milliseconds: [any[], {}[]];
        seconds: [any[], {}[]];
        minsec: [any[], {}[]];
        minutes: [any[], {}[]];
        hourmin: [any[], {}[]];
        hours: [any[], {}[]];
        days: [any[], {}[]];
        months: [any[], {}[]];
        years: [any[], {}[]];
    };
    _get_resolution_str(resolution_secs: any, span_secs: any): "microseconds" | "milliseconds" | "minsec" | "seconds" | "hourmin" | "minutes" | "hours" | "days" | "months" | "years";
    doFormat(ticks: any, axis: any, num_labels?: null, char_width?: null, fill_ratio?: number, ticker?: null): any[];
}
