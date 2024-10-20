import os
import geopandas as gpd
import pandas as pd
from pyogrio.errors import DataSourceError
from shapely.geometry import Polygon, MultiPolygon

root_dir = "California_spread_2012_2021"
output_dir = "data" 

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

point_data = []
polygon_data = []

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".shp"):
            shapefile_path = os.path.join(root, file)
            
            try:
                fire_extent = gpd.read_file(shapefile_path)
                
                if fire_extent.geom_type.iloc[0] == 'Point':
                    point_data.append(fire_extent)
                elif fire_extent.geom_type.iloc[0] == 'Polygon':
                    polygon_data.append(fire_extent)
                elif fire_extent.geom_type.iloc[0] == 'MultiPolygon':
                    # Handle MultiPolygon by extracting individual polygons
                    polygons = []
                    repeated_data = []
                    
                    for idx, geom in enumerate(fire_extent.geometry):
                        if isinstance(geom, MultiPolygon):
                            # Append each individual polygon and repeat the corresponding data row
                            for poly in geom.geoms:
                                polygons.append(poly)
                                repeated_data.append(fire_extent.iloc[idx])
                        else:
                            polygons.append(geom)
                            repeated_data.append(fire_extent.iloc[idx])

                    # Create a new GeoDataFrame with repeated non-geometry data and corresponding polygons
                    repeated_data_df = pd.DataFrame(repeated_data).reset_index(drop=True)
                    multi_polygon_df = gpd.GeoDataFrame(repeated_data_df, geometry=polygons)
                    
                    polygon_data.append(multi_polygon_df)
                else:
                    print(f"Skipping {file} due to unhandled geometry type: {fire_extent.geom_type.iloc[0]}")
            
            except DataSourceError as e:
                print(f"Skipping {file}: {e}")

if point_data:
    combined_point_data = pd.concat(point_data, ignore_index=True)
    point_output_path = os.path.join(output_dir, "combined_fire_extent_points.shp")
    combined_point_data.to_file(point_output_path)

if polygon_data:
    combined_polygon_data = pd.concat(polygon_data, ignore_index=True)
    polygon_output_path = os.path.join(output_dir, "combined_fire_extent_polygons.shp")
    combined_polygon_data.to_file(polygon_output_path)
