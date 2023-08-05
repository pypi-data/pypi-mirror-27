export declare type Model = any;
export declare type View = any;
export declare const overrides: {
    [key: string]: Model;
};
export interface Models {
    (name: string): Model;
    register(name: string, model: Model): void;
    unregister(name: string): void;
    register_models(models: {
        [key: string]: Model;
    } | null | undefined, force?: boolean, errorFn?: (name: string) => void): void;
    registered_names(): string[];
}
export declare const Models: Models;
export declare const register_models: (models: {
    [key: string]: any;
} | null | undefined, force?: boolean | undefined, errorFn?: ((name: string) => void) | undefined) => void;
export declare const index: {
    [key: string]: View;
};
