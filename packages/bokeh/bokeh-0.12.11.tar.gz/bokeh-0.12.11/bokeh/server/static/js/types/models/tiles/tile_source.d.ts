import { Model } from "../../model";
export declare class TileSource extends Model {
    initialize(attrs: any, options: any): any;
    string_lookup_replace(str: any, lookup: any): any;
    normalize_case(): any;
    update(): boolean[];
    tile_xyz_to_key(x: any, y: any, z: any): string;
    key_to_tile_xyz(key: any): number[];
    sort_tiles_from_center(tiles: any, tile_extent: any): any;
    prune_tiles(): (boolean | undefined)[];
    remove_tile(key: any): boolean | undefined;
    get_image_url(x: any, y: any, z: any): any;
    retain_neighbors(reference_tile: any): void;
    retain_parents(reference_tile: any): void;
    retain_children(reference_tile: any): void;
    tile_xyz_to_quadkey(x: any, y: any, z: any): void;
    quadkey_to_tile_xyz(quadkey: any): void;
}
