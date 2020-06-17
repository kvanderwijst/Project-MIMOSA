import numpy as np


def get_TFP(region, data_store):
    params = data_store.params
    quant = data_store.quant
    time = data_store.data_years
    TFP = []
    dt = time[1] - time[0]

    # Parameters
    alpha = params['economics']['GDP']['alpha']
    dk = params['economics']['GDP']['depreciation of capital']
    sr = params['economics']['GDP']['savings rate']

    # Initialise capital
    K0_data = quant(params['regions'][region]['initial capital'], 'currency_unit', only_magnitude=False)
    K = K0_data.magnitude
    
    # Get data
    GDP_data = data_store.data_values['GDP'][region]
    population_data = data_store.data_values['population'][region]

    for t, GDP, L in zip(time, GDP_data, population_data):
        TFP.append(GDP / calc_GDP(1, L, K, alpha))
        dKdt = calc_dKdt(K, dk, sr * GDP, dt)
        K = dKdt * dt + K

    return np.array(TFP)


def calc_dKdt(K, dk, I, dt):
    return np.log(1-dk) * K + I
    # return ( (1-dk)**dt - 1)/dt * K + I

def calc_GDP(TFP, L, K, alpha):
    return TFP * L**(1-alpha) * K**alpha



def MAC(a, factor, gamma, beta):
    return gamma * factor * a**beta

def AC(a, factor, gamma, beta):
    return gamma * factor * a**(beta+1) / (beta+1)



def damage_fct(T, a1, a2, a3, T0=None):
    """Quadratic damage function

    T: temperature
    T0 [None]: if specified, substracts damage at T0
    """
    fct = lambda temp: a1 * temp + a2 * temp**a3
    dmg = fct(T)
    if T0 is not None:
        dmg -= fct(T0)
    return dmg

def damage_fct_dot(T, a1, a2, a3):
    return a1 + a2 * a3 * T ** (a3 - 1)



def adaptation_costs(P, gamma1, gamma2):
    return gamma1 * P**gamma2