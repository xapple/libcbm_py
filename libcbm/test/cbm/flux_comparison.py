# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pandas as pd
import collections
from libcbm.test.cbm import result_comparison


def get_libcbm_flux_disturbance_cols():
    """Returns the ordered set of names for LibCBM columns involved in
    disturbance fluxes.

    Returns:
        list: a list of strings which are the ordered LibCBM flux indicator
        columns involved in disturbance fluxes.
    """
    return [
        'DisturbanceCO2Production',
        'DisturbanceCH4Production',
        'DisturbanceCOProduction',
        'DisturbanceBioCO2Emission',
        'DisturbanceBioCH4Emission',
        'DisturbanceBioCOEmission',
        'DisturbanceSoftProduction',
        'DisturbanceHardProduction',
        'DisturbanceDOMProduction',
        'DisturbanceMerchToAir',
        'DisturbanceFolToAir',
        'DisturbanceOthToAir',
        'DisturbanceCoarseToAir',
        'DisturbanceFineToAir',
        'DisturbanceDOMCO2Emission',
        'DisturbanceDOMCH4Emission',
        'DisturbanceDOMCOEmission',
        'DisturbanceMerchLitterInput',
        'DisturbanceFolLitterInput',
        'DisturbanceOthLitterInput',
        'DisturbanceCoarseLitterInput',
        'DisturbanceFineLitterInput',
        'DisturbanceVFastAGToAir',
        'DisturbanceVFastBGToAir',
        'DisturbanceFastAGToAir',
        'DisturbanceFastBGToAir',
        'DisturbanceMediumToAir',
        'DisturbanceSlowAGToAir',
        'DisturbanceSlowBGToAir',
        'DisturbanceSWStemSnagToAir',
        'DisturbanceSWBranchSnagToAir',
        'DisturbanceHWStemSnagToAir',
        'DisturbanceHWBranchSnagToAir'
    ]


def get_libcbm_flux_annual_process_cols():
    """Returns the ordered set of names for LibCBM columns involved in
    annual process fluxes.

    Returns:
        list: a list of strings which are the ordered LibCBM flux indicator
        columns involved in annual process fluxes.
    """
    return [
        'DecayDOMCO2Emission',
        'DeltaBiomass_AG',
        'DeltaBiomass_BG',
        'TurnoverMerchLitterInput',
        'TurnoverFolLitterInput',
        'TurnoverOthLitterInput',
        'TurnoverCoarseLitterInput',
        'TurnoverFineLitterInput',
        'DecayVFastAGToAir',
        'DecayVFastBGToAir',
        'DecayFastAGToAir',
        'DecayFastBGToAir',
        'DecayMediumToAir',
        'DecaySlowAGToAir',
        'DecaySlowBGToAir',
        'DecaySWStemSnagToAir',
        'DecaySWBranchSnagToAir',
        'DecayHWStemSnagToAir',
        'DecayHWBranchSnagToAir'
    ]


def get_cbm3_flux_disturbance_cols():
    """Returns the ordered set of names for CBM3 columns involved in
    disturbance fluxes.

    Returns:
        list: a list of strings which are the ordered CBM3 columns involved in
        disturbance fluxes.
    """
    return[
        'CO2Production',
        'CH4Production',
        'COProduction',
        'BioCO2Emission',
        'BioCH4Emission',
        'BioCOEmission',
        'SoftProduction',
        'HardProduction',
        'DOMProduction',
        'MerchToAir',
        'FolToAir',
        'OthToAir',
        'CoarseToAir',
        'FineToAir',
        'DOMCO2Emission',
        'DOMCH4Emssion',
        'DOMCOEmission',
        'MerchLitterInput',
        'FolLitterInput',
        'OthLitterInput',
        'CoarseLitterInput',
        'FineLitterInput',
        'VFastAGToAir',
        'VFastBGToAir',
        'FastAGToAir',
        'FastBGToAir',
        'MediumToAir',
        'SlowAGToAir',
        'SlowBGToAir',
        'SWStemSnagToAir',
        'SWBranchSnagToAir',
        'HWStemSnagToAir',
        'HWBranchSnagToAir',
    ]


def get_cbm3_flux_annual_process_cols():
    """Returns the ordered set of names for CBM3 columns involved in annual
    process fluxes.

    Returns:
        list: a list of strings which are the ordered CBM3 columns involved
        in annual process fluxes.
    """
    return [
        'DOMCO2Emission',
        'DeltaBiomass_AG',
        'DeltaBiomass_BG',
        'MerchLitterInput',
        'FolLitterInput',
        'OthLitterInput',
        'CoarseLitterInput',
        'FineLitterInput',
        'VFastAGToAir',
        'VFastBGToAir',
        'FastAGToAir',
        'FastBGToAir',
        'MediumToAir',
        'SlowAGToAir',
        'SlowBGToAir',
        'SWStemSnagToAir',
        'SWBranchSnagToAir',
        'HWStemSnagToAir',
        'HWBranchSnagToAir'
    ]


def get_cbm3_disturbance_flux(cbm3_flux):
    """Returns disturbance flux from a query result of CBM3 flux indicators.

    Also performs the following table changes to make it easy to join and
    compare with to the libcbm result:

        - rename "TimeStep" to "timestep"
        - convert the "identifier" column to numeric from string
        - rename the columns according to the :py:func:`zip` of
            :py:func:`get_cbm3_flux_disturbance_cols` to
            :py:func:`get_libcbm_flux_disturbance_cols`
        - negate the values for the following columns due to a quirk in
            CBM-CFS3 flux indicator results:
            - 'MerchToAir'
            - 'FolToAir'
            - 'OthToAir'
            - 'CoarseToAir'
            - 'FineToAir'

    Args:
        cbm3_flux (pandas.DataFrame): The CBM-CFS3 disturbance flux

    Returns:
        pandas.DataFrame: a filtered and altered copy of the input containing
            only disturbance fluxes.
    """

    # in CBM3 a default disturbance type of 0 indicates annual process
    # in tblFluxIndicators rows by convention.
    flux = cbm3_flux.loc[cbm3_flux["DefaultDistTypeID"] != 0].copy()
    flux = flux.rename(columns={'TimeStep': 'timestep'})
    flux["identifier"] = pd.to_numeric(flux["identifier"])

    # get the timesteps that do not have any disturbance fluxes
    missing_timesteps = set(cbm3_flux.TimeStep) - set(flux.timestep)

    # account for a CBM-CFS3 quirk where the following fluxes are negated
    # in the tblFluxIndicators results.
    biomass_to_air_cols = [
        'MerchToAir', 'FolToAir', 'OthToAir', 'CoarseToAir', 'FineToAir']
    for b in biomass_to_air_cols:
        flux[b] = flux[b] * -1.0
    libcbm_flux_cols = get_libcbm_flux_disturbance_cols()
    disturbance_flux_mapping = collections.OrderedDict(
        zip(get_cbm3_flux_disturbance_cols(), libcbm_flux_cols))

    flux = flux.rename(columns=disturbance_flux_mapping)
    zero_flux_timesteps = {"timestep": list(missing_timesteps)}
    zero_flux_timesteps.update(
        dict(
            zip(
                libcbm_flux_cols,
                [0.0]*len(libcbm_flux_cols))))

    for identifier in cbm3_flux.identifier.unique():
        zero_flux_timesteps_copy = zero_flux_timesteps.copy()
        zero_flux_timesteps_copy["identifier"] = identifier
        # add rows for timesteps that have zero disturbance flux
        # for each identifier
        flux = flux.append(pd.DataFrame(zero_flux_timesteps_copy))

    return flux


def get_cbm3_annual_process_flux(cbm3_flux):
    """Returns annual process flux from a query result of CBM3 flux
    indicators.

    Also performs the following table changes to make it easy to join and
    compare with to the libcbm result:

        - rename "TimeStep" to "timestep"
        - convert the "identifier" column to numeric from string
        - rename the columns according to the :py:func:`zip` of
            :py:func:`get_cbm3_flux_disturbance_cols` to
            :py:func:`get_libcbm_flux_annual_process_cols`

    Args:
        cbm3_flux (pandas.DataFrame): The CBM-CFS3 flux indicator result

    Returns:
        pandas.DataFrame: a filtered and altered copy of the input containing
            only annual process fluxes.
    """

    # in CBM3 a default disturbance type of 0 indicates annual process
    # in tblFluxIndicators rows by convention.
    flux = cbm3_flux.loc[cbm3_flux["DefaultDistTypeID"] == 0].copy()
    flux = flux.rename(columns={'TimeStep': 'timestep'})
    flux["identifier"] = pd.to_numeric(flux["identifier"])

    disturbance_flux_mapping = collections.OrderedDict(
        zip(
            get_cbm3_flux_annual_process_cols(),
            get_libcbm_flux_annual_process_cols()))

    flux = flux.rename(columns=disturbance_flux_mapping)
    return flux


def get_merged_annual_process_flux(cbm3_flux, libcbm_flux, col_filter=None):
    """Produces a merge of the annual process cbm3 and libcbm flux results

    Args:
        cbm3_flux (pandas.DataFrame): cbm3 pool results as produced by:
            :py:func:`libcbm.test.cbm.cbm3_support.cbm3_simulator.get_cbm3_results`
        libcbm_flux (pandas.DataFrame): libcbm pool results as produced by:
            :py:func:`libcbm.test.cbm.test_case_simulator.run_test_cases`
        col_filter (func): a function for filtering the returned columns
            (accepts an string element of the list and returns true to include
             and false to exclude the column from the result)

    Returns:
        pandas.DataFrame: merged comparison of CBM3 versus libcbm for analysis
    """
    cols = get_libcbm_flux_annual_process_cols()
    if col_filter:
        cols = [x for x in cols if col_filter(x)]
    merged_flux = result_comparison.merge_result(
        get_cbm3_annual_process_flux(cbm3_flux), libcbm_flux, cols)

    return merged_flux


def get_merged_disturbance_flux(cbm3_flux, libcbm_flux, col_filter=None):
    """Produces a merge of the cbm3 and libcbm disturbance flux results

    Args:
        cbm3_flux (pandas.DataFrame): cbm3 pool results as produced by:
            :py:func:`libcbm.test.cbm.cbm3_support.cbm3_simulator.get_cbm3_results`
        libcbm_flux (pandas.DataFrame): libcbm pool results as produced by:
            :py:func:`libcbm.test.cbm.test_case_simulator.run_test_cases`
        col_filter (func): a function for filtering the returned columns
            (accepts an string element of the list and returns true to include
             and false to exclude the column from the result)

    Returns:
        pandas.DataFrame: merged comparison of CBM3 versus libcbm for analysis
    """
    cols = get_libcbm_flux_disturbance_cols()
    if col_filter:
        cols = [x for x in cols if col_filter(x)]
    merged_flux = result_comparison.merge_result(
        get_cbm3_disturbance_flux(cbm3_flux), libcbm_flux, cols)
    return merged_flux
