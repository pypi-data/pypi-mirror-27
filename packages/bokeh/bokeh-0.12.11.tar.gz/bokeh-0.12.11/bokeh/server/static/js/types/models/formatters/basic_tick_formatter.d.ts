import { TickFormatter } from "./tick_formatter";
export declare class BasicTickFormatter extends TickFormatter {
    initialize(attrs: any, options: any): number;
    doFormat(ticks: any, axis: any): any[] | undefined;
}
