import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as ctx

point_data = gpd.read_file('data/combined_fire_extent_points.shp')
polygon_data = gpd.read_file('data/combined_fire_extent_polygons.shp')

polygon_data_wgs84 = polygon_data.to_crs(epsg=4326)
point_data_wgs84 = point_data.to_crs(epsg=4326)

fig, ax = plt.subplots(figsize=(10, 10))

polygon_data_wgs84.plot(ax=ax, color='red', alpha=0.5, edgecolor='black')

point_data_wgs84.plot(ax=ax, color='blue', markersize=5)

ctx.add_basemap(ax, crs=polygon_data_wgs84.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)

plt.title('Combined Fire Extent and Spread Points in California')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

plt.show()
