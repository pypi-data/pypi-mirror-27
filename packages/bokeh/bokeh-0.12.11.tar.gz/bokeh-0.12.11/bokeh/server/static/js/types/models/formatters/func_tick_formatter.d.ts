import { TickFormatter } from "./tick_formatter";
export declare class FuncTickFormatter extends TickFormatter {
    _make_func(): Function;
    doFormat(ticks: any, axis: any): any;
}
