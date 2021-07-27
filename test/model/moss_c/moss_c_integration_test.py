import os
import unittest
import numpy as np
import pandas as pd

from libcbm.model.moss_c import model_context
from libcbm.model.moss_c import model
from libcbm.model.moss_c.pools import ECOSYSTEM_POOLS
from libcbm import resources


class MossCIntegrationTest(unittest.TestCase):

    def test_integration(self):
        test_data_dir = os.path.join(
            resources.get_test_resources_dir(),
            "moss_c_test_case")

        expected_output = pd.read_csv(
            os.path.join(test_data_dir, "expected_output.csv"))
        ctx = model_context.create_from_csv(test_data_dir)
        pool_results = pd.DataFrame()
        flux_results = pd.DataFrame()

        pools = ctx.get_pools_df()
        pools.insert(0, "t", 0)
        pool_results = pool_results.append(pools)

        for i in range(1, 125):

            model.step(ctx)

            pools = ctx.get_pools_df()
            pools.insert(0, "t", i)
            pool_results = pool_results.append(pools)

            flux = ctx.flux.copy()
            flux.insert(0, "t", i)
            flux_results = flux_results.append(flux)

        for p in ECOSYSTEM_POOLS:
            np.allclose(pool_results[p.name], expected_output[p.name])
