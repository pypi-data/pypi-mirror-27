export declare var UIEvents: {
    new (plot_view: any, toolbar: any, hit_area: any, plot: any): {
        _configure_hammerjs(): void;
        register_tool(tool_view: any): any;
        _hit_test_renderers(sx: any, sy: any): any;
        _hit_test_frame(sx: any, sy: any): any;
        _trigger(signal: any, e: any): any;
        trigger(signal: any, event: any, id?: null): any;
        _event_sxy(event: any): {
            sx: number;
            sy: number;
        };
        _bokify_hammer(e: any, extras?: {}): any;
        _bokify_point_event(e: any, extras?: {}): any;
        _tap(e: any): any;
        _doubletap(e: any): any;
        _press(e: any): any;
        _pan_start(e: any): any;
        _pan(e: any): any;
        _pan_end(e: any): any;
        _pinch_start(e: any): any;
        _pinch(e: any): any;
        _pinch_end(e: any): any;
        _rotate_start(e: any): any;
        _rotate(e: any): any;
        _rotate_end(e: any): any;
        _mouse_enter(e: any): any;
        _mouse_move(e: any): any;
        _mouse_exit(e: any): any;
        _mouse_wheel(e: any): any;
        _key_down(e: any): any;
        _key_up(e: any): any;
    };
};
