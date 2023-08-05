export interface Ref {
    id: string;
    type: string;
    subtype?: string;
}
export declare function create_ref(obj: any): Ref;
export declare function is_ref(arg: any): boolean;
