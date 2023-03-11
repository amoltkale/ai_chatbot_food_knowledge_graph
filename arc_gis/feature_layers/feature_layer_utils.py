import arcgis
from arcgis.gis import GIS
from arcgis.features import *
import pandas as pd

def delete_existing_folder(folder_name):
    try:
        return gis.content.delete_folder(folder=folder_name)
    except:
        return False

def get_feature_layer(service_url,gis):
    '''Returns a feature layer from a feature layer service url.'''
    return FeatureLayer(url=service_url,gis=gis)


def explore_feature_layer(feature_layer):
    '''Prints few details about a feature layer.'''
    print(f'Layer Name: {feature_layer.properties.name}')
    print(f'\tCopyright Text: {feature_layer.properties.copyrightText}')
    
    # one of the properties to check serviceItemId
    print(f'\tserviceItemId: {feature_layer.properties.serviceItemId}')
    
    print(f'\tDescription: {feature_layer.properties.description}')
    
    # what operations are possible over this layer ?
    print(f'\tCapabalities: {feature_layer.properties.capabilities}')
    
    # How can we determine CRS of a layer (called "spatial_reference"). 

    # By converting it to a featureset - using query() without parameters -  and then retrieving its spatial reference
    # note that "spatial reference" is a property of a featureset, but not of a layer


    feature_set = feature_layer.query()
    print(f'\tType of feature set: {type(feature_set)}')
    print(f'\tSpatial Reference for the Feature Layer: {feature_set.spatial_reference}')
    print('\tSample Records from the layer:-')
    feature_layer_spatial_df = feature_set.sdf
    print(f'\tTotal Records: {len(feature_layer_spatial_df)}')
    display(feature_layer_spatial_df.head(4))
    
      
def get_enrichment_variables(nourish_enrichment_segment,exel_book='../resources/Variables to Use in Food Swamp and Opportunities Maps 2-2-23.xlsx'):
    '''Returns list of variables from noursish variable exel book for respective segment sheet.'''
    if nourish_enrichment_segment=='consumer_spending':
        sheet_name='Esri Consumer Spending Data '
    elif nourish_enrichment_segment=='business':
        sheet_name='Esri Business Data'
    elif nourish_enrichment_segment=='market_potential':
        sheet_name='Esri Market Potential Data'
    elif nourish_enrichment_segment=='demographics':
        sheet_name='Esri Demographics'
    else:
        raise KeyError(f"The sheet name for nourish_enrichment_segment={nourish_enrichment_segment} is not present in the workbook : {exel_book}")
    
    # Read excel file with sheet name
    dict_df = pd.read_excel(exel_book, sheet_name=[sheet_name])
    
    print(f"Parsing [{sheet_name}] for {nourish_enrichment_segment} segment!!")
    vars_df = dict_df.get(sheet_name)
    vars_df = vars_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    # drop Nan from the dataframe
    vars_df = vars_df.dropna(subset=['Variables to use'])
    var_list = list(vars_df['Variables to use'].unique())
    print(f"\tNumber of Variables: {len(var_list)}")
    return var_list


def find_non_common_columns(fl_sdf_1,fl_sdf_2):
    '''This function checks two spatially enabled dataframes for non-common columns'''
    
    fl_sdf_1_cols = list(fl_sdf_1.columns)
    
    fl_sdf_2_cols = list(fl_sdf_2.columns)
    
    print("Common columns between two layers: ")
    common_cols = set(fl_sdf_1_cols).intersection(set(fl_sdf_2_cols))
    print(common_cols)
    
    print("Non-common columns between two layers: ")
    non_common_cols = set(fl_sdf_1_cols) ^ (set(fl_sdf_2_cols))
    print(non_common_cols)
    return list(non_common_cols)