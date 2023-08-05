export declare var OnOffButtonView: {
    new (options?: {}): {
        render(): any;
        _clicked(): boolean;
        initialize(options: any): any;
        remove(): any;
        layout(): void;
        renderTo(element: any, replace?: boolean): void;
        has_finished(): any;
        notify_finished(): any;
        _createElement(): HTMLElement;
        toString(): string;
        connect_signals(): void;
        disconnect_signals(): void;
    };
    getters(specs: any): any[];
};
