import pandas as pd
from libcbm.model.cbm import cbm_defaults
from libcbm.model.cbm import cbm_factory
from libcbm.model.cbm import cbm_config
from libcbm.model.cbm.cbm_defaults_reference import CBMDefaultsReference
from libcbm import resources


def _safe_map(series, map):
    """Helper method to ensure an error is thrown if any value in a
    mapped series is null

    Args:
        series (pandas.Series): the series to map
        map (function, collections.abc.Mapping subclass or Series): the
            `Series.map` map parameter

    Raises:
        ValueError: at least one value in the mapped series was null

    Returns:
        pd.Series: The mapped series (see :py:func:`pandas.Series.map`)
    """
    out_series = series.map(map)
    null_values = pd.isnull(out_series)
    if null_values.any():
        missing_entries = list(
            series[null_values].unique())
        raise ValueError(
            f"undefined values detected {missing_entries[:10]}")
    return out_series


class StandCBMFactory:
    """StandCBMFactory encompasses a method to create a working CBM instance
    with minimal inputs: stand merchantable volumes and classifiers.

    The resulting CBM instance can easily be used for stand level simulations
    with explicit relationships between stands and disturbances.
    """
    def __init__(self, classifiers, merch_volumes, db_path=None,
                 locale="en-CA", dll_path=None):
        """Initialize an instance of CBMStandFactory using classifiers and
        merch volumes.

        Example classifiers::

            {
                "c1": ["c1_v1", "c1_v2", ...],
                "c1": ["c1_v1", "c1_v2", ...],
                ...
                "cN": ["cN_v1", "cN_v2", ...],
            }

        Example merch_volumes::

                [
                    {
                        "classifier_set": ["c1_v1", "c2_v1", ..., "cN_vK"],
                        "merch_volumes": [
                            "species_name": "Spruce",
                            "age_volume_pairs": [
                                [0, 0],
                                [50, 100],
                                [100, 150],
                                [150, 200],
                            ]
                        ]
                    }
                ]


        Args:
            classifiers (dict): dictionary describing classifiers and
                classifier values
            merch_volumes (list): list of dictionaries describing merchantable
                volume components. See example.
            db_path (str, optional): path to a cbm_defaults database. If None,
                the default database is used. Defaults to None.
            locale_code (str, optional): a locale code used to fetch the
                corresponding translated version of default parameter strings
            dll_path (str, optional): path to the libcbm compiled library, if
                not specified a default value is used.
        """
        if not db_path:
            self._db_path = resources.get_cbm_defaults_path()
        else:
            self._db_path = db_path

        if not dll_path:
            self._dll_path = resources.get_libcbm_bin_path()
        else:
            self._dll_path = dll_path

        self._classifiers = classifiers
        self._merch_volumes = merch_volumes
        self._locale = locale
        self.defaults_ref = CBMDefaultsReference(self._db_path, self._locale)
        self.merch_vol_factory = self.merch_volumes_factory()
        self._classifier_config = self._get_classifier_config()
        self._classifier_idx = cbm_config.get_classifier_indexes(
            self._classifier_config)

    def merch_volumes_factory(self):
        merch_volume_list = []
        for c in self._merch_volumes:
            merch_volume_list.append(
                cbm_config.merch_volume_curve(
                    classifier_set=c["classifier_set"],
                    merch_volumes=[
                        {
                            "species_id": self.defaults_ref.get_species_id(
                                m["species"]),
                            "age_volume_pairs": [
                                list(age_vol)
                                for age_vol in m["age_volume_pairs"]
                            ],
                        }
                        for m in c["merch_volumes"]
                    ],
                )
            )
        return cbm_config.merch_volume_to_biomass_config(
            db_path=self._db_path, merch_volume_curves=merch_volume_list
        )

    def get_disturbance_type_map(self):
        return {
            r["disturbance_type_id"]: r["disturbance_type_name"]
            for r in self.defaults_ref.disturbance_type_ref}

    def get_classifier_map(self):
        return self._classifier_idx[
            "classifier_value_names"].copy()

    def _get_classifier_value_ids(self, classifier_name,
                                  classifier_value_name_series):
        classifier_value_name_map = self._classifier_idx[
            "classifier_value_ids"][classifier_name]
        return _safe_map(
            classifier_value_name_series, classifier_value_name_map)

    def _get_classifier_config(self):
        classifiers_list = []
        for classifier_name, values in self._classifiers.items():
            classifiers_list.append(
                cbm_config.classifier(classifier_name, values=[
                    cbm_config.classifier_value(value) for value in values
                ]))

        return cbm_config.classifier_config(classifiers_list)

    def classifiers_factory(self):
        return self._classifier_config

    def prepare_inventory(self, inventory_df):
        """Prepare inventory, classifiers pd.DataFrames compatible with
        :py:func:`libcbm.model.cbm.cbm_simulator.simulate` using the provided
        inventory dataframe.

        Args:
            inventory_df (pd.DataFrame): dataframe with the following columns::

                * c1 .. cN: one column for each classifier, each containing
                  classifier values
                * admin_boundary: the admin boundary name for drawing CBM
                  parameters (defined in db)
                * eco_boundary: the eco boundary name for drawing CBM
                  parameters (defined in db)
                * age: inventory age [years]
                * area: inventory area [hectares]
                * delay: inventory spinup delay [years]
                * land_class: unfccc land class name (defined in db.landclass)
                * afforestation_pre_type: afforestation pre-type name (defined
                  in db)
                * historic_disturbance_type: historic disturbance type name
                  (defined in db)
                * last_pass_disturbance_type: last pass disturbance type name
                  (defined in db)

        Returns:
            Tuple:
                0: classifiers pd.DataFrame
                1: inventory pd.DataFrame
        """

        classifiers = pd.DataFrame(
            columns=self._classifiers.keys(),
            data={
                k: self._get_classifier_value_ids(k, inventory_df[k])
                for k in self._classifiers.keys()
            }
        )
        inventory = pd.DataFrame(
            columns=[
                "age", "area", "spatial_unit", "afforestation_pre_type_id",
                "land_class", "historical_disturbance_type",
                "last_pass_disturbance_type", "delay"],
            data={
                "age": inventory_df.age,
                "area": inventory_df.area,
                "spatial_unit": _safe_map(
                    inventory_df.index,
                    lambda x: self.defaults_ref.get_spatial_unit_id(
                        str(inventory_df.admin_boundary.iloc[x]),
                        str(inventory_df.eco_boundary.iloc[x]))
                ),
                "afforestation_pre_type_id": _safe_map(
                    inventory_df.afforestation_pre_type,
                    lambda x: (
                        -1 if pd.isnull(x) else
                        self.defaults_ref.get_afforestation_pre_type_id(x))
                    ),
                "land_class": _safe_map(
                    inventory_df.land_class,
                    self.defaults_ref.get_land_class_id),
                "historical_disturbance_type": _safe_map(
                    inventory_df.historic_disturbance_type,
                    lambda x: (
                        -1 if pd.isnull(x) else
                        self.defaults_ref.get_disturbance_type_id(x))
                    ),
                "last_pass_disturbance_type": _safe_map(
                    inventory_df.last_pass_disturbance_type,
                    lambda x: (
                        -1 if pd.isnull(x) else
                        self.defaults_ref.get_disturbance_type_id(x))
                    ),
                "delay": inventory_df.delay
            })
        return classifiers, inventory

    def initialize_cbm(self):
        return cbm_factory.create(
            dll_path=self._dll_path,
            dll_config_factory=cbm_defaults.get_libcbm_configuration_factory(
                self._db_path
            ),
            cbm_parameters_factory=cbm_defaults.get_cbm_parameters_factory(
                self._db_path
            ),
            merch_volume_to_biomass_factory=self.merch_volumes_factory,
            classifiers_factory=self.classifiers_factory)
