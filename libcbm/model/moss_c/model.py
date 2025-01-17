# moss c model implementation
#
# based on referenced work:
#
# Bona, Kelly & Shaw, Cindy & Fyles, James & Kurz, Werner. (2016).
# Modelling moss-derived carbon in upland black spruce forests.
# Canadian Journal of Forest Research. 46. 10.1139/cjfr-2015-0512.
#

from types import SimpleNamespace
import numba
import numpy as np
import pandas as pd

from libcbm.model.moss_c.pools import Pool
from libcbm.model.moss_c.pools import ANNUAL_PROCESSES
from libcbm.model.moss_c.pools import DISTURBANCE_PROCESS
from libcbm.model.moss_c import model_functions
from libcbm.model.moss_c.model_functions import SpinupState
from libcbm.wrapper import libcbm_operation


def f1(merch_vol, a, b):
    """Returns Canopy openess, O(t) as a function of Merch. Volume

    10^(((a)*(Log(V(t))) + b)

    Args:
        merch_vol (float, np.ndarray): array of merch volumes
        a (float, np.ndarray): MossC a parameter
        b (float, np.ndarray): MossC b parameter

    Returns:
        np.ndarray: Canopy openess
    """

    return np.where(
        merch_vol == 0,
        60,
        np.power(
            10, a * np.log10(merch_vol, where=(merch_vol != 0)) + b,
            where=(merch_vol != 0)))


def f2(openness, stand_age, c, d):
    """ returns Feather moss ground cover, GCfm(t)

    (O(t)* c) + d

    Args:
        openness (float, np.ndarray): canopy openness
        stand_age (int, np.ndarray): stand age in years
        c (float, np.ndarray): MossC c parameter,
        d (float, np.ndarray): MossC d parameter

    Returns:
        np.ndarray: Feather moss ground cover
    """
    return np.where(
        stand_age < 10,
        0.0,
        np.where(
            openness > 70.0,
            100.0, openness * c + d))


def f3(openness, stand_age, e, f):
    """ returns Sphagnum moss ground cover, GCsp(t)

    (O(t)* e) + f

    Args:
        openness (float, np.ndarray): canopy openness
        stand_age (int, np.ndarray): stand age in years
        e (float, np.ndarray): MossC e parameter,
        f (float, np.ndarray): MossC f parameter

    Returns:
        np.ndarray: Sphagnum moss ground cover
    """
    return np.where(
        stand_age < 10,
        0.0,
        np.where(
            openness > 70.0,
            100.0, openness * e + f))


def f4(openness, g, h):
    """Feathermoss NPP (assuming 100% ground cover), NPPfm

    g*O(t)^h

    Args:
        openness (float, np.ndarray): canopy openness
        g (float, np.ndarray): MossC g parameter,
        h (float, np.ndarray): MossC h parameter,
    """
    return np.where(
        openness < 5.0, 0.6,
        g * np.power(openness, h))


def f5(openness, i, j, _l):
    """Sphagnum NPP (assuming 100% ground cover), NPPsp

    i*(O(t)^2) + j*(O(t) + l

    Args:
        openness (float, np.ndarray): canopy openness
        i (float, np.ndarray): MossC i parameter,
        j (float, np.ndarray): MossC j parameter,
        _l (float, np.ndarray): MossC l parameter,

    Returns:
        np.ndarray: Sphagnum moss NPP
    """
    return i * openness ** 2.0 + j * openness + _l


def f6(merch_vol, m, n):
    """

    Args:
        merch_vol (float, np.ndarray): merchantable volume.
        m (float, np.ndarray): MossC m parameter,
        n (float, np.ndarray): MossC n parameter,
    """
    return np.log(merch_vol) * m + n


def f7(mean_annual_temp, base_decay_rate, q10, t_ref):
    """Applied Decay rate, ak this applies to any of the moss DOM
    pools feather moss fast (kff), feather moss slow (kfs), sphagnum
    fast (ksf), and sphagnum slow (kss)

    Args:
        mean_annual_temp (float, np.ndarray): [description]
        base_decay_rate (float, np.ndarray): [description]
        q10 (float, np.ndarray): [description]
        t_ref (float, np.ndarray): [description]
    """
    return base_decay_rate * np.exp(
        (mean_annual_temp - t_ref) * np.log(q10) * 0.1)


def annual_process_dynamics(state, params):

    kss = f6(params.max_merch_vol, params.m, params.n)
    openness = f1(state.merch_vol, params.a, params.b)

    return SimpleNamespace(
        kss=kss,
        openness=openness,

        # applied feather moss fast pool decay rate
        akff=f7(
            params.mean_annual_temp, params.kff, params.q10,
            params.tref),

        # applied feather moss slow pool decay rate
        akfs=f7(
            params.mean_annual_temp, params.kfs, params.q10,
            params.tref),

        # applied sphagnum fast pool applied decay rate
        aksf=f7(
            params.mean_annual_temp, params.ksf, params.q10,
            params.tref),

        # applied sphagnum slow pool applied decay rate
        akss=f7(
            params.mean_annual_temp, kss, params.q10, params.tref),

        # Feather moss ground cover
        GCfm=f2(openness, state.age, params.c, params.d),

        # Sphagnum ground cover
        GCsp=f3(openness, state.age, params.e, params.f),

        # Feathermoss NPP (assuming 100% ground cover)
        NPPfm=f4(openness, params.g, params.h),

        # Sphagnum NPP (assuming 100% ground cover)
        NPPsp=f5(
            openness, params.i, params.j, params.l))


def get_annual_process_matrix(dynamics_param):
    mat = [
        [Pool.Input, Pool.FeatherMossLive,
         dynamics_param.NPPfm * dynamics_param.GCfm / 100.0],
        [Pool.Input, Pool.SphagnumMossLive,
         dynamics_param.NPPsp * dynamics_param.GCsp / 100.0],

        # turnovers
        [Pool.FeatherMossLive, Pool.FeatherMossFast, 1.0],
        [Pool.FeatherMossLive, Pool.FeatherMossLive, 0.0],

        [Pool.FeatherMossFast, Pool.FeatherMossSlow,
         dynamics_param.akff * 0.15],

        [Pool.SphagnumMossLive, Pool.SphagnumMossFast, 1.0],
        [Pool.SphagnumMossLive, Pool.SphagnumMossLive, 0.0],

        [Pool.SphagnumMossFast, Pool.SphagnumMossSlow,
         dynamics_param.aksf * 0.15],

        # fast losses
        [Pool.FeatherMossFast, Pool.FeatherMossFast,
         1.0 - dynamics_param.akff],
        [Pool.SphagnumMossFast, Pool.SphagnumMossFast,
         1.0 - dynamics_param.aksf],

        # decays
        [Pool.FeatherMossFast, Pool.CO2, dynamics_param.akff * 0.85],

        [Pool.SphagnumMossFast, Pool.CO2, dynamics_param.aksf * 0.85],

        [Pool.FeatherMossSlow, Pool.CO2, dynamics_param.akfs],
        [Pool.FeatherMossSlow, Pool.FeatherMossSlow,
         1.0 - dynamics_param.akfs],

        [Pool.SphagnumMossSlow, Pool.CO2, dynamics_param.akss],
        [Pool.SphagnumMossSlow, Pool.SphagnumMossSlow,
         1.0 - dynamics_param.akss]
    ]
    return mat


@numba.njit()
def update_spinup_variables(n_stands, spinup_state, dist_type, pools,
                            last_rotation_slow, this_rotation_slow,
                            rotation_num, historical_dist_type,
                            last_pass_dist_type, enabled):
    enabled_count = n_stands
    for i in range(n_stands):
        state = spinup_state[i]
        if state == SpinupState.LastPassEvent:
            dist_type[i] = last_pass_dist_type[i]
        elif state == SpinupState.HistoricalEvent:
            dist_type[i] = historical_dist_type[i]
            last_rotation_slow[i] = \
                pools[i, Pool.SphagnumMossSlow.value] + \
                pools[i, Pool.FeatherMossSlow.value]
            rotation_num[i] += 1
        else:
            if state == SpinupState.End:
                enabled[i] = 0
                enabled_count -= 1
            dist_type[i] = 0
            this_rotation_slow[i] = \
                pools[i, Pool.SphagnumMossSlow.value] + \
                pools[i, Pool.FeatherMossSlow.value]
    return enabled_count == 0


def _append_spinup_debug_record(spinup_debug, iteration, model_ctx,
                                spinup_vars):

    model_state_t = pd.DataFrame(
        {k: v for k, v in model_ctx.state.__dict__.items()})
    model_state_t.insert(0, "t", iteration)
    spinup_debug.model_state = spinup_debug.model_state.append(model_state_t)

    pools_t = model_ctx.get_pools_df()
    pools_t.insert(0, "t", iteration)
    spinup_debug.pools = spinup_debug.pools.append(pools_t)

    spinup_vars_t = pd.DataFrame(
        {k: v for k, v in spinup_vars.__dict__.items()})
    spinup_vars_t.insert(0, "t", iteration)
    spinup_debug.spinup_vars = spinup_debug.spinup_vars.append(spinup_vars_t)


def spinup(model_context, enable_debugging=False):

    if enable_debugging:
        spinup_debug = SimpleNamespace(
            model_state=pd.DataFrame(),
            pools=pd.DataFrame(),
            spinup_vars=pd.DataFrame()
        )
    else:
        spinup_debug = None

    spinup_vars = SimpleNamespace(
        spinup_state=np.full(
            model_context.n_stands, SpinupState.AnnualProcesses),
        rotation_num=np.full(model_context.n_stands, 0, dtype=int),
        last_rotation_slow=np.full(model_context.n_stands, 0.0, dtype=float),
        this_rotation_slow=np.full(model_context.n_stands, 0.0, dtype=float))
    iteration = 0
    while True:

        spinup_vars.spinup_state = model_functions.advance_spinup_state(
            spinup_state=spinup_vars.spinup_state,
            age=model_context.state.age,
            final_age=model_context.parameters.age,
            return_interval=model_context.parameters.return_interval,
            rotation_num=spinup_vars.rotation_num,
            max_rotations=model_context.parameters.max_rotations,
            last_rotation_slow=spinup_vars.last_rotation_slow,
            this_rotation_slow=spinup_vars.this_rotation_slow)
        all_finished = update_spinup_variables(
            n_stands=model_context.n_stands,
            spinup_state=spinup_vars.spinup_state,
            dist_type=model_context.state.disturbance_type,
            pools=model_context.pools,
            last_rotation_slow=spinup_vars.last_rotation_slow,
            this_rotation_slow=spinup_vars.this_rotation_slow,
            rotation_num=spinup_vars.rotation_num,
            historical_dist_type=model_context.historical_dm_index,
            last_pass_dist_type=model_context.last_pass_dm_index,
            enabled=model_context.state.enabled)
        if all_finished:
            # re-enable everything for subsequent processes
            model_context.state.enabled[:] = 1
            break
        step(
            model_context, disturbance_before_annual_process=False,
            include_flux=False)
        if enable_debugging:
            _append_spinup_debug_record(
                spinup_debug, iteration, model_context, spinup_vars)
        iteration += 1

    return spinup_debug


def step(model_context, disturbance_before_annual_process=True,
         include_flux=True):
    n_stands = len(model_context.state.age)
    model_context.state.merch_vol = \
        model_context.merch_vol_lookup.get_merch_vol(
            model_context.state.age,
            model_context.parameters.merch_volume_id)
    dynamics_param = annual_process_dynamics(
        model_context.state, model_context.parameters)
    annual_process_matrix = get_annual_process_matrix(dynamics_param)
    annual_process_matrices = libcbm_operation.Operation(
        model_context.dll,
        libcbm_operation.OperationFormat.RepeatingCoordinates,
        annual_process_matrix)
    annual_process_matrices.set_matrix_index(
        np.array(list(range(0, n_stands)), dtype=np.uintp))
    disturbance_matrices = libcbm_operation.Operation(
        model_context.dll,
        libcbm_operation.OperationFormat.MatrixList,
        model_context.disturbance_matrices.dm_list)
    disturbance_matrices.set_matrix_index(model_context.state.disturbance_type)

    flux = None
    if include_flux:
        model_context.initialize_flux()
        flux = model_context.flux

    if disturbance_before_annual_process:
        op_processes = [DISTURBANCE_PROCESS, ANNUAL_PROCESSES]
        ops = [disturbance_matrices, annual_process_matrices]
    else:
        op_processes = [ANNUAL_PROCESSES, DISTURBANCE_PROCESS]
        ops = [annual_process_matrices, disturbance_matrices]

    libcbm_operation.compute(
        dll=model_context.dll,
        pools=model_context.pools,
        operations=ops,
        op_processes=op_processes,
        flux=flux,
        enabled=model_context.state.enabled)

    for op in ops:
        op.dispose()

    model_context.state.age = \
        np.where(
            model_context.state.enabled == 0,
            model_context.state.age,
            np.where(
                model_context.state.disturbance_type != 0, 0,
                model_context.state.age + 1))
