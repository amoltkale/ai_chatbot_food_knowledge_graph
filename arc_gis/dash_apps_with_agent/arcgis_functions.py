from arcgis.gis import GIS
from arcgis.features import Feature, FeatureLayer, FeatureSet
from arcgis.geometry import  project
from arcgis.geocoding import geocode
from arcgis.geometry import buffer, Point
from arcgis.geometry.filters import intersects
import arcgis.network as network


from langchain import OpenAI

from app_utils import get_bot_response

import pandas as pd

import sys
sys.path.append('../../')
from utils import get_config


from ipywidgets.embed import embed_minimal_html

def get_block_group_map(region, radius, gis):

    #openaikey = get_config("open_ai","key")
    #llm = OpenAI(temperature=0, openai_api_key=openaikey)

    # Query the block group for respective variables and feature layer.
    #variables = "demographics"
    variables = "average_consumer_spending"
    if variables=="demographics":
        url = "https://services1.arcgis.com/eGSDp8lpKe5izqVc/arcgis/rest/services/aff1b6/FeatureServer/0"
    elif variables == "average_consumer_spending":
        url = "https://services1.arcgis.com/eGSDp8lpKe5izqVc/arcgis/rest/services/a2afc4/FeatureServer/0"
    ft_lyr = FeatureLayer(gis=gis, url=url)

    # Picking up sample variables for just poc on rendering maps as per our need.
    out_fields = ["fips", "X1130_A", "X1132_A", "X1137_A", "X1147_A", "X1142_A"]  

    # Query the block group for respective variables and feature layer.
    #variables = "demographics"
    variables = "average_consumer_spending"
    if variables=="demographics":
        url = "https://services1.arcgis.com/eGSDp8lpKe5izqVc/arcgis/rest/services/aff1b6/FeatureServer/0"
    elif variables == "average_consumer_spending":
        url = "https://services1.arcgis.com/eGSDp8lpKe5izqVc/arcgis/rest/services/a2afc4/FeatureServer/0"
    ft_lyr = FeatureLayer(gis=gis, url=url)

    # Picking up sample variables for just poc on rendering maps as per our need.
    out_fields = ["fips", "X1130_A", "X1132_A", "X1137_A", "X1147_A", "X1142_A"]  

    #region = "Bonita, San Diego"
    region_address = geocode(address=region,
                    max_locations = 1
                    )


    lat_long = [region_address[0]['location']['y'],region_address[0]['location']['x']]
    address_score = region_address[0]['score']
    address_identified = region_address[0]['address']
    # print(f"Important Fields: \n Address Matched: {address_identified} \n Latitude,Longitude: {lat_long}\n Match SCore: {address_score}")


    point_location = region_address[0]['location']
    # print(f"point_location: {point_location}")
    point_geom = Point({"x": point_location['x'], "y": point_location['y'], "spatialReference" : {'wkid': 4326, 'latestWkid': 4326}})

    ## This buffer query was failing because ESRI takes constant values instead of names for unit.
    # So here 9035 is Value for constant esriSRUnit_SurveyMile which is described as 'US Survey Mile'
    # Link for more constants: http://resources.arcgis.com/en/help/arcobjects-cpp/componenthelp/index.html#/esriSRUnitType_Constants/000w00000042000000/
    buffer_geom = buffer(geometries=[point_geom], distances=radius, unit='9035', in_sr={'wkid': 4326, 'latestWkid': 4326})

    target_geometry = buffer_geom[0]
    # target_geometry


    buffer_filter = intersects(target_geometry,{'wkid': 4326, 'latestWkid': 4326})

    result_rows = ft_lyr.query(out_fields=out_fields,
                            return_geometry=True,
                            geometry_filter=buffer_filter,
                            as_df=True)
    #print(f"Number of block groups identified: {result_rows.shape[0]}")
    #result_rows.head(3)

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

    # template = """
    #         We are using hot cmap coloring argument given to function pandas df.spatial.plot(). Explain in human understandable 
    #         verbal description about the color representation in context of the col variable passed to it.
    #         Also elaborate and explain below parameters from our query result in a human friendly fasion: 
    #         Radius: {radius}, Number of block groups identified: {result_rows.shape[0]}
    # """

    tempt_dict = {"Radius": radius, "Total Block Groups": result_rows.shape[0]}
    # template = """
    #         Remember that you are directly talking to the person and should address them as if you are talking to them.
    #         Explain in a friendly manner the color map where dark red reprsents low opprotunity for their business and
    #         bright yellow resprsents high opprotunity for their business.
    #         Also format the following json text in a friendly and human digestable fashion.
    #         {temp_dict}
    # """
    template = f"""
            Darker colors represents low opportunity for your business, while brighter colors represents high opportunity.
            This is taking a total radius of {radius} miles and identified {result_rows.shape[0]} total blocks.
            """


    embed_minimal_html('static/block_level_map.html', views=[m3])
    return {'file_path':'static/block_level_map.html','verbal_desc':template}
    #return (f"Number of block groups identified: {result_rows.shape[0]}",'static/block_level_map.html')


def get_block_group_map_with_opp_comp_score(region, radius, gis):
    #openaikey = get_config("open_ai","key")
    #llm = OpenAI(temperature=0, openai_api_key=openaikey)

    ft_lyr = FeatureLayer(url="https://services1.arcgis.com/eGSDp8lpKe5izqVc/arcgis/rest/services/a3eb8f/FeatureServer/0")

    region_address = geocode(address=region,
                    max_locations = 1
                    )


    lat_long = [region_address[0]['location']['y'],region_address[0]['location']['x']]
    address_score = region_address[0]['score']
    address_identified = region_address[0]['address']
    # print(f"Important Fields: \n Address Matched: {address_identified} \n Latitude,Longitude: {lat_long}\n Match SCore: {address_score}")


    point_location = region_address[0]['location']
    # print(f"point_location: {point_location}")
    point_geom = Point({"x": point_location['x'], "y": point_location['y'], "spatialReference" : {'wkid': 4326, 'latestWkid': 4326}})

    ## This buffer query was failing because ESRI takes constant values instead of names for unit.
    # So here 9035 is Value for constant esriSRUnit_SurveyMile which is described as 'US Survey Mile'
    # Link for more constants: http://resources.arcgis.com/en/help/arcobjects-cpp/componenthelp/index.html#/esriSRUnitType_Constants/000w00000042000000/
    buffer_geom = buffer(geometries=[point_geom], distances=radius, unit='9035', in_sr={'wkid': 4326, 'latestWkid': 4326})

    target_geometry = buffer_geom[0]
    # target_geometry


    buffer_filter = intersects(target_geometry,{'wkid': 4326, 'latestWkid': 4326})
    out_fields = ["fips", "oc_score"]
    result_rows = ft_lyr.query(out_fields=out_fields,
                            return_geometry=True,
                            geometry_filter=buffer_filter,
                            as_df=True)
    #print(f"Number of block groups identified: {result_rows.shape[0]}")
    #result_rows.head(3)

    ## Getting the map center
    map_centre = [point_location['y'],point_location['x']]

    map = gis.map(map_centre, zoomlevel=12)
    result_rows.spatial.plot(renderer_type='c',                          
                            map_widget= map,)
    # Drawing a radius boundary for ease of demo.
    # map.draw(target_geometry)


    # template = f"""
    #         Darker colors represents high opportunity for your business, while brighter colors represents low opportunity.
    #         This is taking a total radius of {radius} miles and identified {result_rows.shape[0]} total block groups.
    #         """

    template = f"""
    We have generated a map for you around {region}, which shows areas with high business opportunities in darker colors and 
    areas with low opportunities in brighter colors. We use six factors to calculate the score, such as how many people live there, 
    how much they spend on food away from home, and how many restaurants are already there.
    This map has been created considering a radius of {radius} miles, and we have 
    identified a total of  {result_rows.shape[0]} block groups in the area.
    A block group here is a small geographic unit which contains between 600 and 3,000 people.
    """



    embed_minimal_html('static/block_level_map.html', views=[map])
    return {'file_path':'static/block_level_map.html','verbal_desc':template}
    #return (f"Number of block groups identified: {result_rows.shape[0]}",'static/block_level_map.html')


def nearest_facility(originating_address, facilities_feat_lyr, gis, as_df=False, return_all_facilities=False):
    '''
    This function identifies the nearest facility for a given originating address.
    '''
    
    analysis_url = gis.properties.helperServices.closestFacility.url
    cf_layer = network.ClosestFacilityLayer(analysis_url, gis=gis)
    facility_feat_list = []
    matched_facility_address = []
    contact_numbers = []
    org_names_list = []

    if facilities_feat_lyr is not None:
        fset = facilities_feat_lyr.query()
        all_geometries = [i['geometry'] for i in fset.to_dict()['features']]
        all_attributes = [i['attributes'] for i in fset.to_dict()['features']]
        all_geometries_sr4326 = project(all_geometries ,in_sr={'latestWkid': 3857}, out_sr={'latestWkid': 4326})

        for i in range(len(all_geometries_sr4326)):
            facility_feat = Feature(geometry=all_geometries_sr4326[i],attributes=all_attributes[i])
            matched_facility_address.append(facility_feat.attributes['Match_addr'])
            contact_numbers.append(facility_feat.attributes['cont_nmbr'])
            org_names_list.append(facility_feat.attributes['org_name'])

            facility_feat_list.append(facility_feat)

    facility_fset = FeatureSet(features=facility_feat_list, 
                                geometry_type='esriGeometryPoint', 
                                spatial_reference={'latestWkid': 4326})
    count_of_facilities = len(facility_fset)
        
    # originating_address = '581 Moss St, 91911, Chula Vista, CA'
    originating_matched_address = geocode(originating_address, max_locations=1)[0]
        
    originating_address_feature = Feature(geometry=originating_matched_address['location'], attributes=originating_matched_address['attributes'])
    originating_address_fset = FeatureSet([originating_address_feature], geometry_type='esriGeometryPoint',
                          spatial_reference={'latestWkid': 4326})
    
    result = cf_layer.solve_closest_facility(incidents=originating_address_fset,
                                        facilities=facility_fset,
                                        default_target_facility_count=count_of_facilities,
                                        return_facilities=True,
                                        impedance_attribute_name='TravelTime',
                                        accumulate_attribute_names=['Miles','TravelTime'])
    line_feat_list = []
    for line_dict in result['routes']['features']:
        f1 = Feature(line_dict['geometry'], line_dict['attributes'])
        line_feat_list.append(f1)
        
    routes_fset = FeatureSet(line_feat_list, 
                         geometry_type=result['routes']['geometryType'],
                         spatial_reference= result['routes']['spatialReference'])
    
    df1 = routes_fset.sdf
    
    df1['facility_address'] = matched_facility_address
    df1['originating_address'] = [originating_address_feature.attributes['Match_addr'] for i in range(count_of_facilities)]
    df1['contact_number'] = contact_numbers
    df1['organization_name'] = org_names_list

    df1 = df1[['facility_address','originating_address','contact_number','organization_name','Total_Miles']]

    if return_all_facilities:
        if as_df:
            return df1
        else:
            raise ValueError('as_df should be True if return_all_facilities is True')
    
    # select the row with the minimum Total_Miles
    min_miles_index = df1['Total_Miles'].idxmin()
    min_miles_row = df1.loc[min_miles_index]
    
    return min_miles_row.to_json()


if __name__ == '__main__':
    # print(get_block_group_map('Bonita, San Diego',2.0)["verbal_desc"])
    username = get_config("arcgis","username")
    password = get_config("arcgis","passkey")
    gis = GIS("https://ucsdonline.maps.arcgis.com/home", username=username, password=password)
    originating_address = '581 Moss St, 91911, Chula Vista, CA'
    sba_feat_layer = FeatureLayer(gis= gis, url = "https://services1.arcgis.com/eGSDp8lpKe5izqVc/arcgis/rest/services/a8d231/FeatureServer/0")
    nearest_facility_json = nearest_facility(originating_address, facilities_feat_lyr=sba_feat_layer, gis =gis, as_df=False, return_all_facilities=False)
    print(nearest_facility_json)
