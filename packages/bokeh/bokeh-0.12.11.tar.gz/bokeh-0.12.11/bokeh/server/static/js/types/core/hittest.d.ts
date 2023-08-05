export declare var point_in_poly: (x: any, y: any, px: any, py: any) => boolean;
export declare class HitTestResult {
    constructor();
    is_empty(): boolean;
    update_through_union(other: any): {
        [key: string]: {}[];
    };
}
export declare var create_hit_test_result: () => HitTestResult;
export declare var create_1d_hit_test_result: (hits: any) => HitTestResult;
export declare var validate_bbox_coords: ([x0, x1]: [any, any], [y0, y1]: [any, any]) => {
    minX: any;
    minY: any;
    maxX: any;
    maxY: any;
};
export declare var dist_2_pts: (x0: any, y0: any, x1: any, y1: any) => any;
export declare var dist_to_segment_squared: (p: any, v: any, w: any) => any;
export declare var dist_to_segment: (p: any, v: any, w: any) => number;
export declare var check_2_segments_intersect: (l0_x0: any, l0_y0: any, l0_x1: any, l0_y1: any, l1_x0: any, l1_y0: any, l1_x1: any, l1_y1: any) => {
    hit: boolean;
    x: any;
    y: any;
};
