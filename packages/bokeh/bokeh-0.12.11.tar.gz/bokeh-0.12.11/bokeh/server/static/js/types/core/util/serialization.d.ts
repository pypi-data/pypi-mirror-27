export declare var ARRAY_TYPES: {
    float32: Float32ArrayConstructor;
    float64: Float64ArrayConstructor;
    uint8: Uint8ArrayConstructor;
    int8: Int8ArrayConstructor;
    uint16: Uint16ArrayConstructor;
    int16: Int16ArrayConstructor;
    uint32: Uint32ArrayConstructor;
    int32: Int32ArrayConstructor;
};
export declare var DTYPES: {};
export declare var BYTE_ORDER: string;
export declare var swap16: (a: any) => null;
export declare var swap32: (a: any) => null;
export declare var swap64: (a: any) => null;
export declare var process_buffer: (spec: any, buffers: any) => any[];
export declare var process_array: (obj: any, buffers: any) => any[] | undefined;
export declare var arrayBufferToBase64: (buffer: any) => string;
export declare var base64ToArrayBuffer: (base64: any) => ArrayBuffer;
export declare var decode_base64: (input: any) => any[];
export declare var encode_base64: (array: any, shape: any) => {
    __ndarray__: string;
    shape: any;
    dtype: any;
};
export declare var decode_column_data: (data: any, buffers: any) => {}[];
export declare var encode_column_data: (data: any, shapes: any) => {};
