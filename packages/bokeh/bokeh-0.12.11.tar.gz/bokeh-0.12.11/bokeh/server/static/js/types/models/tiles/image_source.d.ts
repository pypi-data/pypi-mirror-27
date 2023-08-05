import { Model } from "../../model";
export declare class ImageSource extends Model {
    initialize(attrs: any, options: any): any;
    normalize_case(): any;
    string_lookup_replace(str: any, lookup: any): any;
    add_image(image_obj: any): any;
    remove_image(image_obj: any): boolean;
    get_image_url(xmin: any, ymin: any, xmax: any, ymax: any, height: any, width: any): any;
}
