import arcgis
from arcgis.gis import GIS
from arcgis.features import FeatureLayer, FeatureLayerCollection, GeoAccessor
from arcgis.geocoding import geocode
from arcgis.geometry import buffer, Point
from arcgis.geometry.filters import intersects

import pandas as pd

import sys
sys.path.append('../../')
from utils import get_config


from ipywidgets.embed import embed_minimal_html

def get_block_group_map(region, radius):

    username = get_config("arcgis","username")
    password = get_config("arcgis","passkey")
    gis = GIS("https://ucsdonline.maps.arcgis.com/home", username=username, password=password)

    # Query the block group for respective variables and feature layer.
    #variables = "demographics"
    variables = "average_consumer_spending"
    if variables=="demographics":
        url = "https://services1.arcgis.com/eGSDp8lpKe5izqVc/arcgis/rest/services/aff1b6/FeatureServer/0"
    elif variables == "average_consumer_spending":
        url = "https://services1.arcgis.com/eGSDp8lpKe5izqVc/arcgis/rest/services/a2afc4/FeatureServer/0"
    ft_lyr = FeatureLayer(gis=gis,
                        url=url)

    # Picking up sample variables for just poc on rendering maps as per our need.
    out_fields = ["fips", "X1130_A", "X1132_A", "X1137_A", "X1147_A", "X1142_A"]  

    # Query the block group for respective variables and feature layer.
    #variables = "demographics"
    variables = "average_consumer_spending"
    if variables=="demographics":
        url = "https://services1.arcgis.com/eGSDp8lpKe5izqVc/arcgis/rest/services/aff1b6/FeatureServer/0"
    elif variables == "average_consumer_spending":
        url = "https://services1.arcgis.com/eGSDp8lpKe5izqVc/arcgis/rest/services/a2afc4/FeatureServer/0"
    ft_lyr = FeatureLayer(gis=gis,
                        url=url)

    # Picking up sample variables for just poc on rendering maps as per our need.
    out_fields = ["fips", "X1130_A", "X1132_A", "X1137_A", "X1147_A", "X1142_A"]  

    #region = "Bonita, San Diego"
    region_address = geocode(address=region,
                    max_locations = 1
                    )


    lat_long = [region_address[0]['location']['y'],region_address[0]['location']['x']]
    address_score = region_address[0]['score']
    address_identified = region_address[0]['address']
    print(f"Important Fields: \n Address Matched: {address_identified} \n Latitude,Longitude: {lat_long}\n Match SCore: {address_score}")


    point_location = region_address[0]['location']
    print(f"point_location: {point_location}")
    point_geom = Point({"x": point_location['x'], "y": point_location['y'], "spatialReference" : {'wkid': 4326, 'latestWkid': 4326}})

    ## This buffer query was failing because ESRI takes constant values instead of names for unit.
    # So here 9035 is Value for constant esriSRUnit_SurveyMile which is described as 'US Survey Mile'
    # Link for more constants: http://resources.arcgis.com/en/help/arcobjects-cpp/componenthelp/index.html#/esriSRUnitType_Constants/000w00000042000000/
    buffer_geom = buffer(geometries=[point_geom], distances=radius, unit='9035', in_sr={'wkid': 4326, 'latestWkid': 4326})

    target_geometry = buffer_geom[0]
    target_geometry


    buffer_filter = intersects(target_geometry,{'wkid': 4326, 'latestWkid': 4326})

    result_rows = ft_lyr.query(out_fields=out_fields,
                            return_geometry=True,
                            geometry_filter=buffer_filter,
                            as_df=True)
    print(f"Number of block groups identified: {result_rows.shape[0]}")
    result_rows.head(3)

    ## Getting the map center
    map_centre = [point_location['y'],point_location['x']]

    m3 = gis.map(map_centre, zoomlevel=12)
    result_rows.spatial.plot(renderer_type='c',
                            method='esriClassifyNaturalBreaks',
                            class_count=10,  # choose the number of classes
                            col='x1130_a',
                            cmap='hot',  # color map to pick colors from for each class
                            alpha=0.2 ,
                            map_widget= m3,)
    m3.draw(target_geometry)

    embed_minimal_html('static/block_level_map.html', views=[m3])

    return 'static/block_level_map.html'


if __name__ == '__main__':
    get_block_group_map('Bonita, San Diego',5.0)