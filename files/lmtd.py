import numpy as np
import pandas as pd
import math


# Logarithmic Mean Temperature Difference (LMTD) is used to determine the temperature driving force for heat transfer in flow systems.

def heat_capacity(mass_flow_rate, cp):
    """ Calculates the heat_capacity given a mass_flow_rate
        and a specif_heat of a material.

    Args:
        mass_flow_rate (float): the mass of a substance which
        passes per unit of time. Units: [kg/s]
        cp (float): Specif heat. The amount of energy that must be
        added, in the form of heat, to one unit of mass of the
        substance in order to cause an increase of one unit in
        temperature Units: [J/kg.K]

    Returns:
        [float]: The heat_capacity, which is the amount of
        heat to be supplied to a given mass of a material
        to produce a unit change in its temperature.
    """
    return mass_flow_rate * cp

def delta_temp(t_in, t_out):
    """ Calcutates the fluid temperature variation on the entrance
        and the exit point.
        Units: since this is a variation, the unit could be any.

    Args:
        t_in (float): Fluid temperature on the entrance.
        t_out (float): Fluid temperature on the exit.

    Returns:
        (float): temperature variation
    """
    return t_in - t_out

def log_mean_temp(t_hot_in, t_hot_out, t_cold_in, t_cold_out):
    """Calculates the Logarithmic Mean Temperature Difference of
    a concentric transfer heat with parallel flow

    Args:
        t_hot_in (float): Hot fluid temperature on the entrance.
        t_hot_out (float): Hot fluid temperature on the exit.
        t_cold_in (float): Cold fluid temperature on the entrance.
        t_cold_out (float): Cold fluid temperature on the exit.

    Returns:
        delta_tlm [float]: Logarithmic Mean Temperature Difference
    """
    delta_t1 =  t_hot_in - t_cold_in
    delta_t2 = t_hot_out - t_cold_out
    dif_delta = delta_t2 - delta_t1
    log_delta = np.log(delta_t2/delta_t1)
    delta_tlm = dif_delta / log_delta

    return delta_tlm

def cp(t):
    first = 6 * 10**(-9) * t**4
    second = 10**(-6) * t**3
    third = 7.0487 * 10**(-5) * t**2
    fourth = 2.4403 * 10**(-3) * t
    fifth = 4.2113

    cp = first - second + third - fourth + fifth

    return cp


def df_1(df):

    # Calculete temperature in and out mean in order no calculte specific heat 
    t_mean_hot= (df.iloc[:,2] + df.iloc[:,3])/2
    t_mean_cold = (df.iloc[:,4] + df.iloc[:,5])/2

    # Calculate specific heat
    cp_hot = cp(t_mean_hot)
    cp_cold = cp(t_mean_cold)

    # Calculate the temperature difference between entry and exit point
    t_delta_hot = delta_temp(df.iloc[:,2],df.iloc[:,3])
    t_delta_cold = delta_temp(df.iloc[:,4],df.iloc[:,5])

    # Calculate the transfer heat rate from both fluids
    q_hot = - 1 * (df.iloc[:,0] * cp_hot * t_delta_hot) * 1000
    q_cold = - 1 * (df.iloc[:,1] * cp_cold * t_delta_cold) * 1000

    # % heat lost
    heat_lost = q_cold / q_hot * 100

    # Creat dict
    d = {'Specific Heat Hot Fluid [kJ/kg.K]':cp_hot,
        'Specific Heat Cold Fluid [kJ/kg.K]': cp_cold,
        'Transfer Heat Rate Hot Fluid [W]': q_hot,
        'Transfer Heat Rate Cold Fluid [W]': q_cold,
        'Heat Lost [%]':heat_lost
        }

    df_new = pd.DataFrame(data=d)

    return df_new


def df_2(df):

    # Calculate log mean temperature difference
    delta_lmtd = log_mean_temp(df.iloc[:,2],df.iloc[:,3],df.iloc[:,4],df.iloc[:,5])

    # Calculate temperature in and out mean in order no calculte specific heat
    t_mean_hot= (df.iloc[:,2] + df.iloc[:,3])/2
    t_mean_cold = (df.iloc[:,4] + df.iloc[:,5])/2

    # Calculate specific heat
    cp_hot = cp(t_mean_hot)
    cp_cold = cp(t_mean_cold)

    # Calculate heat capacity
    heat_capacity_hot = heat_capacity(df.iloc[:,0],cp_hot)
    heat_capacity_cold = heat_capacity(df.iloc[:,1],cp_cold)

    # Find minimum heat capacity
    c_min = []
    for hot, cold in zip(heat_capacity_hot, heat_capacity_cold):
        if hot <= cold:
            c_min.append(hot)
        else:
            c_min.append(cold)

    # Calculate the maximum transfer heat rate
    q_max = c_min * (delta_temp(df.iloc[:,2],df.iloc[:,5]))

    # Calculate the transfer heat rate from cold fluid
    q_cold = - 1 * (df.iloc[:,1] * cp_cold * delta_temp(df.iloc[:,4],df.iloc[:,5]))

    # Calculate the effectiveness
    epsilon = q_cold/q_max

    # Calculate global heat coeficient and area
    ua = q_cold/delta_lmtd

    # Calculate NUT
    nut = ua/c_min

    # Create dict
    d = {'Log Mean Temperature Difference [°C]' : delta_lmtd,
        'Heat Capacity Hot [W/K]' : heat_capacity_hot,
        'Heat Capacity Cold [W/K]' : heat_capacity_cold,
        'Effectiveness' : epsilon,
        'NUT' : nut}

    # Create DataFrame
    df_new = pd.DataFrame(data=d)

    return df_new