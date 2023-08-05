import { InputWidget, InputWidgetView } from "./input_widget";
export declare class DatePickerView extends InputWidgetView {
    constructor();
    render(): this;
    _on_select(date: any): any;
}
export declare class DatePicker extends InputWidget {
}
