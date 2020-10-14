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
    first = 6 * 10**(-6) * t**4
    second = 10**(-6) * t**3
    third = 10**(-5) * t**2
    fourth = 2.4403 * 10**(-3) * t
    fifth = 4.2113

    cp = first - second + third - fourth + fifth

    return cp

"""
def df_one(df):

    t_hot_mean= (df.loc[:,'T1 Hot In'] + df.loc[:,'T2 Hot Out'])/2
    t_cold_mean = (df.loc[:,'T3 Cold In'] + df.loc[:,'T4 Cold Out'])/2

    """