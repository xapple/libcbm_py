# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from types import SimpleNamespace
from libcbm import data_helpers
from libcbm.model.cbm import cbm_variables


def create_in_memory_reporting_func(density=False, classifier_map=None,
                                    disturbance_type_map=None):
    """Create storage and a function for complete simulation results.  The
    function return value can be passed to :py:func:`simulate` to track
    simulation results.

    Args:
        density (bool, optional): if set to true pool and flux indicators will
            be computed as area densities (tonnes C/ha). By default, pool and
            flux outputs are computed as mass (tonnes C) based on the area of
            each stand. Defaults to False.
        classifier_map (dict, optional): a classifier map for subsituting the
            internal classifier id values with classifier value names.
            If specified, the names associated with each id in the map are the
            values in the  the classifiers result DataFrame  If set to None the
            id values will be returned.
        disturbance_type_map (dict, optional): a disturbance type map for
            subsituting the internally defined disturbance type id with names
            or other ids in the parameters and state tables.  If set to none no
            substitution will occur.

    Returns:
            tuple: a pair of values:

                1. types.SimpleNameSpace: an object with properties:

                    - pool (pandas.DataFrame) pool results storage
                    - flux (pandas.DataFrame) flux results storage
                    - state (pandas.DataFrame) state results storage
                    - classifiers (pandas.DataFrame) classifiers results
                        storage
                    - parameters (pandas.DataFrame) cbm params storage
                    - area (pandas.DataFrame) area storage

                2. func: a function for appending to the above results
                    DataFrames for each timestep
    """

    results = SimpleNamespace()
    results.pools = None
    results.flux = None
    results.state = None
    results.classifiers = None
    results.parameters = None
    results.area = None

    def append_simulation_result(timestep, cbm_vars):
        timestep_pools = cbm_vars.pools if density else \
            cbm_vars.pools.multiply(cbm_vars.inventory.area, axis=0)
        results.pools = data_helpers.append_simulation_result(
            results.pools, timestep_pools, timestep)
        if (
            cbm_vars.flux is not None and
            len(cbm_vars.flux.index) > 0
        ):
            timestep_flux = cbm_vars.flux \
                if density else cbm_vars.flux.multiply(
                    cbm_vars.inventory.area, axis=0)
            results.flux = data_helpers.append_simulation_result(
                results.flux, timestep_flux, timestep)

        def disturbance_type_map_func(dist_id):
            if dist_id <= 0:
                return dist_id
            else:
                return disturbance_type_map[dist_id]

        state = cbm_vars.state.copy()
        params = cbm_vars.parameters.copy()
        if disturbance_type_map:
            state.last_disturbance_type = \
                cbm_vars.state.last_disturbance_type.apply(
                    disturbance_type_map_func)

            params.disturbance_type = \
                cbm_vars.parameters.disturbance_type.apply(
                    disturbance_type_map_func)

        results.state = data_helpers.append_simulation_result(
            results.state, state, timestep)

        if classifier_map is None:
            results.classifiers = data_helpers.append_simulation_result(
                results.classifiers, cbm_vars.classifiers, timestep)
        else:
            results.classifiers = data_helpers.append_simulation_result(
                results.classifiers,
                cbm_vars.classifiers.applymap(
                    classifier_map.__getitem__),
                timestep)
        results.area = data_helpers.append_simulation_result(
            results.area, cbm_vars.inventory.loc[:, ["area"]], timestep)
        results.parameters = data_helpers.append_simulation_result(
            results.parameters, params, timestep)
    return results, append_simulation_result


def simulate(cbm, n_steps, classifiers, inventory, reporting_func,
             pre_dynamics_func=None, spinup_params=None,
             spinup_reporting_func=None):
    """Runs the specified number of timesteps of the CBM model.  Model output
    is processed by the provided reporting_func. The provided
    pre_dynamics_func is called prior to each CBM dynamics step.

    Args:
        cbm (libcbm.model.cbm.cbm_model.CBM): Instance of the CBM model
        n_steps (int): The number of CBM timesteps to run
        classifiers (pandas.DataFrame): CBM classifiers for each of the rows
            in the inventory
        inventory (pandas.DataFrame): CBM inventory which defines the initial
            state of the simulation
        reporting_func (function): a function which accepts the simulation
            timestep and all CBM variables for reporting results by timestep.
            An example compatible function factory is
            :py:func:`create_in_memory_reporting_func` which stores the
            results in memory.
        pre_dynamics_func (function, optional): A function which accepts the
            simulation timestep and all CBM variables, and which is called
            prior to computing C dynamics  The layout of the CBM variables is
            the same as the return value of:
            :py:func:`libcbm.model.cbm.cbm_variables.initialize_simulation_variables`
            The function returns all CBM variables which will then be passed
            into the current CBM timestep.
        spinup_params (object): collection of spinup specific parameters. See
            :py:func:`libcbm.model.cbm.cbm_variables.initialize_spinup_parameters`
            for object format
        spinup_reporting_func (function, optional): a function which accepts
            the spinup iteration, and all spinup variables.  Specifying this
            function will result in a performance penalty as the per-iteration
            spinup results are computed and tracked. An example compatible
            function factory is :py:func:`create_in_memory_reporting_func`
            which stores the results in memory.  If unspecified spinup results
            are not tracked. Defaults to None.
    """

    cbm_vars = cbm_variables.initialize_simulation_variables(
        classifiers, inventory, cbm.pool_codes, cbm.flux_indicator_codes)

    spinup_vars = cbm_variables.initialize_spinup_variables(
        cbm_vars, spinup_params,
        include_flux=spinup_reporting_func is not None)

    cbm.spinup(spinup_vars, reporting_func=spinup_reporting_func)
    cbm_vars = cbm.init(cbm_vars)
    reporting_func(0, cbm_vars)

    for time_step in range(1, int(n_steps) + 1):

        if pre_dynamics_func:
            cbm_vars = pre_dynamics_func(time_step, cbm_vars)
            # make memory contiguous in case pre_dynamics_func messed things up
            cbm_vars = cbm_variables.prepare(cbm_vars)

        cbm_vars = cbm.step(cbm_vars)
        reporting_func(time_step, cbm_vars)
