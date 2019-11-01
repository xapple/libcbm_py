"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import os
import json
import shutil
from types import SimpleNamespace
import pandas as pd


def get_version_number(filename):
    """
    Gets the version number for the specified filename,
    If that filename corresponds to a .net assembly
    https://stackoverflow.com/questions/6470032/extract-assembly-version-from-dll-using-python

    Args:
        filename (str): path to a compiled .net executable or dll for which to
            fetch the version

    Returns:
        str: a string representation of the version
    """
    import win32api
    info = win32api.GetFileVersionInfo(filename, "\\")
    ms = info['FileVersionMS']
    ls = info['FileVersionLS']
    return ".".join([str(x) for x in [
        win32api.HIWORD(ms), win32api.LOWORD(ms),
        win32api.HIWORD(ls), win32api.LOWORD(ls)]])


def save_cbm_cfs3_test(name, output_dir, start, end, runtime,
                       cbm3_project_path, cbm3_results_path, age_interval,
                       num_age_classes, n_steps, cases, toolbox_install_path,
                       cbm_exe_dir, aidb_path, cbm3_result):
    """Saves metadata, the CBM-CFS3 databases, configuration and CSV results
    for a run.

    Args:
        name (str): the name of the CBM test run
        output_dir ([type]): The directory where the output created by this
            function will be copied.
        start (str): a string representation of simulation start time and date
        end (str):  a string representation of simulation end time and date
        runtime (float): The run time (in seconds)
        cbm3_project_path (str): path to the cbm-cfs3 project being simulated
        cbm3_results_path (str): path to the cbm-cfs3 results db being
            simulated
        age_interval (int): the number of years between age points in yield
            curves
        num_age_classes (int): the number of age points in yield curves
        n_steps (int): the number of time steps being simulated
        cases (list): test cases as generated by the test case generator.
            See: libcbm.test.cbm.casegeneration
        toolbox_install_path (str): path to the installation of CBM-CFS3
        cbm_exe_dir (str): directory containing the CBM-CFS3 model
            executables "cbm.exe" and "makelist.exe".
        aidb_path (str): path to a copy of a CBM-CFS3 archive
            index access database.
        cbm3_result (dict): formatted like:
            :py:func:`libcbm.test.cbm.cbm3_support.cbm3_simulator.get_cbm3_results`

    Returns:
        dict: the metadata for the simulation
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cbm3_project_save_path = os.path.join(
        output_dir, os.path.basename(cbm3_project_path))
    shutil.copyfile(cbm3_project_path, cbm3_project_save_path)

    cbm3_results_save_path = os.path.join(
        output_dir, os.path.basename(cbm3_results_path)
    )
    shutil.copyfile(cbm3_results_path, cbm3_results_save_path)

    metadata = {
        "name": name,
        "start": start,
        "end": end,
        "runtime": runtime,
        "cbm3_project_path": cbm3_project_save_path,
        "cbm3_results_path": cbm3_results_save_path,
        "age_interval": age_interval,
        "num_age_classes": num_age_classes,
        "n_steps": n_steps,
        "toolbox_install_path": toolbox_install_path,
        "toolbox_version": get_version_number(
            os.path.join(toolbox_install_path, "Toolbox.exe")),
        "cbm_exe_dir": cbm_exe_dir,
        "aidb_path": aidb_path
    }

    with open(os.path.join(output_dir, 'metadata.json'), 'w') as metadata_fp:
        json.dump(metadata, metadata_fp, indent=4)
    with open(os.path.join(output_dir, 'cases.json'), 'w') as cases_fp:
        json.dump(cases, cases_fp, indent=4)

    cbm3_result["pools"].to_csv(
        os.path.join(output_dir, "pools.csv"), index=False)
    cbm3_result["flux"].to_csv(
        os.path.join(output_dir, "flux.csv"), index=False)
    cbm3_result["state"].to_csv(
        os.path.join(output_dir, "state.csv"), index=False)
    return metadata


def load_cbm_cfs3_test(test_dir):
    """Loads an existing test output created by :py:func:`save_cbm_cfs3_test`

    Args:
        test_dir (str): the directory containing the test

    Returns:
        types.SimpleNamespace: an object with properties:

            - metadata : test metadata
            - cases : the test cases config
            - pools : pandas.DataFrame containing pool results
            - flux : pandas.DataFrame containing flux results
            - state : pandas.DataFrame containing state results
    """
    test = SimpleNamespace()
    with open(os.path.join(test_dir, 'metadata.json')) as metadata_fp:
        test.metadata = json.load(metadata_fp)
    with open(os.path.join(test_dir, 'cases.json')) as cases_fp:
        test.cases = json.load(cases_fp)
    test.pools = pd.read_csv(os.path.join(test_dir, "pools.csv"))
    test.flux = pd.read_csv(os.path.join(test_dir, "flux.csv"))
    test.state = pd.read_csv(os.path.join(test_dir, "state.csv"))
    return test
