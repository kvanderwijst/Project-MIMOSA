import numpy as np
import pandas as pd

import importlib.resources as pkg_resources

from . import data as package_data

##################
## RICE/AD-RICE:
##################

AD_RICE_coeffs = pd.read_csv(
    pkg_resources.open_text(package_data, 'rice_damages_adapt.csv'),
    index_col=0
)

SSP_to_RICE2010_regions = {
    'R5.2OECD': ['USA', 'JAPAN', 'EUROPE'],
    'R5.2ASIA': ['CHINA', 'INDIA', 'LI'],
    'R5.2LAM': ['LMI'],
    'R5.2MAF': ['AFRICA', 'HIO'],
    'R5.2REF': [],
}

SSP_to_RICE2012_regions = {
    'R5.2OECD': ['USA', 'JAPAN', 'EUROPE'],
    'R5.2ASIA': ['CHINA', 'INDIA', 'LI'],
    'R5.2LAM': ['MI'],
    'R5.2MAF': ['AFRICA', 'OHI'],
    'R5.2REF': ['RUSSIA', 'EE'],
}

def get_damage_adapt_coeffs_RICE2010(region, param_name):
    regions = SSP_to_RICE2010_regions[region]
    if len(regions) == 0:
        return 0.0 if param_name not in ['a3', 'g2'] else 1
    # TODO: current aggregation is "mean". Maybe population/GDP weighted is better
    coeffs = AD_RICE_coeffs.loc[regions].mean()
    return float(coeffs[param_name+'_2010'])

def get_damage_adapt_coeffs_RICE2012(region, param_name):
    regions = SSP_to_RICE2012_regions[region]
    # TODO: current aggregation is "mean". Maybe population/GDP weighted is better
    coeffs = AD_RICE_coeffs.loc[regions].mean()
    return float(coeffs[param_name])
    

##################
## AD-WITCH:
##################

AD_WITCH_coeffs = pd.read_csv(
    pkg_resources.open_text(package_data, 'witch_damages_adapt.csv'),
    index_col=0
)

SSP_to_WITCH_regions = { # KOSAU not used?
    'R5.2OECD': ['USA', 'Western EU', 'CAJAZ'],
    'R5.2ASIA': ['CHINA', 'INDIA', 'SASIA', 'EASIA'],
    'R5.2LAM': ['LACA'],
    'R5.2MAF': ['SSA', 'MENA'],
    'R5.2REF': ['TE']
}

def get_damage_coeffs_witch(region, param_name):
    WITCH_regions = SSP_to_WITCH_regions[region]
    # TODO: current aggregation is "mean". Maybe population/GDP weighted is better
    coeffs = AD_WITCH_coeffs.loc[WITCH_regions].mean()
    return float(coeffs[param_name])



def get_param_value(region, params, all_params):
    if params[0] in ['damages', 'adaptation']:
        damage_module = all_params['model']['damage module']
        if damage_module == 'RICE2010':
            return get_damage_adapt_coeffs_RICE2010(region, params[1])
        if damage_module == 'RICE2012':
            return get_damage_adapt_coeffs_RICE2012(region, params[1])
        if damage_module == 'WITCH':
            return get_damage_coeffs_witch(region, params[1])
        raise Exception('{} not found for region {}'.format(region, params))
    raise NotImplementedError()




# %%
# damage_coeffs = {
#     'DICE': [0, 0.267],
#     'Global': np.array([0.0018, 0.0023]) * 100,
#     'US': [0.0, 0.1414],
#     'EU': [0.0, 0.1591],
#     'Japan': [0.0, 0.1617],
#     'Russia': [0.0, 0.1151],
#     'Eurasia': [0.0, 0.1305],
#     'China': [0.0785, 0.1259],
#     'India': [0.4385, 0.1689],
#     'Middle East': [0.277989, 0.1586],
#     'Africa': [0.340974, 0.1983],
#     'Latin America': [0.0609, 0.1345],
#     'OHI': [0.0, 0.1564],
#     'Other non-OECD Asia': [0.1755, 0.1734]
# }