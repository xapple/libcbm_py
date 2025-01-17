# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import numpy as np
from libcbm.input.sit import sit_format
from libcbm.input.sit import sit_parser


def parse(disturbance_types_table):
    """Parse and validate a SIT formatted disturbance type table

    Args:
        disturbance_types_table (pandas.DataFrame): a table in SIT
            disturbance type format

    Example:

        Input:

            ========  =========
              0         1
            ========  =========
            distid1   fire
            distid2   clearcut
            distid3   clearcut
            ========  =========

        Output:

            ========  =========
             id         name
            ========  =========
            distid1   fire
            distid2   clearcut
            distid3   clearcut
            ========  =========


    Raises:
        ValueError: duplicate ids detected in disturbance data.

    Returns:
        pandas.DataFrame: a validated copy of the input table with
            standardized colmun names
    """
    result = sit_parser.unpack_table(
        disturbance_types_table,
        sit_format.get_disturbance_type_format(
            len(disturbance_types_table.columns)),
        "disturbance types")

    duplicates = result.groupby("id").size()
    duplicates = list(duplicates[duplicates > 1].index)
    if len(duplicates) > 0:
        raise ValueError(
            f"duplicate ids detected in disturbance types {duplicates}")

    # establish a numeric identifier for each row of the SIT disturbances
    result.insert(
        0, "sit_disturbance_type_id",
        np.arange(len(result)) + 1)
    return result
