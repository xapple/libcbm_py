# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import json
from types import SimpleNamespace
from contextlib import contextmanager
import pandas as pd
import numpy as np
from libcbm.model.cbm import cbm_factory
from libcbm.model.cbm import cbm_config
from libcbm.input.sit import sit_transition_rule_parser
from libcbm.input.sit import sit_disturbance_event_parser
from libcbm.input.sit import sit_format
from libcbm.input.sit.sit_mapping import SITMapping
from libcbm.input.sit import sit_reader
from libcbm.input.sit import sit_classifier_parser
from libcbm.input.sit.sit_cbm_defaults import SITCBMDefaults
from libcbm import resources
from libcbm.model.cbm.rule_based.sit import sit_rule_based_processor


def get_classifiers(classifiers, classifier_values):
    """Create classifier input for initializing the CBM class based on CBM
    Standard import tool formatted data.

    Args:
        classifiers (pandas.DataFrame): the parsed SIT classifiers output
            of :py:func:`libcbm.input.sit.sit_classifier_parser.parse`
        classifier_values (pandas.DataFrame): the parsed SIT classifier values
            output of :py:func:`libcbm.input.sit.sit_classifier_parser.parse`

    Returns:
        dict: configuration dictionary for CBM. See:
            :py:func:`libcbm.model.cbm.cbm_config.classifier_config`
    """
    classifiers_config = []
    for _, row in classifiers.iterrows():
        values = classifier_values[
            classifier_values.classifier_id == row.id].name
        classifiers_config.append(cbm_config.classifier(
            name=row["name"],
            values=[cbm_config.classifier_value(value=x) for x in list(values)]
        ))

    config = cbm_config.classifier_config(classifiers_config)
    return config


def _create_classifier_value_maps(sit):
    """Creates dictionaries for fetching internally defined identifiers
    and attaches them to the specified sit object instance. Values can
    then be fetched from the sit instance like the following examples::

        classifier_id = sit.classifier_ids["my_classifier_name"]
        classifier_name = sit.classifier_names[1]
        classifier_value_id = \
            sit.classifier_value_ids["classifier1"]["classifier1_value1"]

    The following fields will be assigned to the specified sit instance:

        * classifier_names - dictionary of id (int, key) to
            name (str, value) for each classifier
        * classifier_ids - dictionary of name (str, value)
            to id (int, key) for each classifier
        * classifier_value_ids - nested dictionary, with one entry per
            classifier name. Each nested dictionary contains classifier value
            name (str, key) to classifier value id (int, value)

            Example::

                {
                    "classifier_name_1": {
                        "classifier_1_value_name_1": 1,
                        "classifier_1_value_name_2": 2
                    },
                    "classifier_name_2": {
                        "classifier_2_value_name_1": 3,
                        "classifier_2_value_name_2": 4
                    },
                    ...
                }

        * classifier_value_names - nested dictionary, with one entry per
            classifier id. Each nested dictionary contains classifier value
            name (str, key) to classifier value id (int, value)

            Example::

                {
                    1: {
                        1: "classifier_1_value_name_1",
                        2: "classifier_1_value_name_2"
                    },
                    2: {
                        3: "classifier_2_value_name_1"
                        4: "classifier_2_value_name_2"
                    },
                    ...
                }

    Args:
        sit (object): sit instance as returned by :py:func:`load_sit`
    """
    classifiers_config = get_classifiers(
        sit.sit_data.classifiers, sit.sit_data.classifier_values)
    idx = cbm_config.get_classifier_indexes(classifiers_config)
    sit.classifier_names = idx["classifier_names"]
    sit.classifier_ids = idx["classifier_ids"]
    sit.classifier_value_ids = idx["classifier_value_ids"]
    sit.classifier_value_names = idx["classifier_value_names"]


def get_merch_volumes(yield_table, classifiers, classifier_values, age_classes,
                      sit_mapping):
    """Create merchantable volume input for initializing the CBM class
    based on CBM Standard import tool formatted data.

    Args:
        yield_table (pandas.DataFrame): the parsed SIT yield output
            of :py:func:`libcbm.input.sit.sit_yield_parser.parse`
        classifiers (pandas.DataFrame): the parsed SIT classifiers output
            of :py:func:`libcbm.input.sit.sit_classifier_parser.parse`
        age_classes (pandas.DataFrame): the parsed SIT age classes
            output of :py:func:`libcbm.input.sit.sit_age_class_parser.parse`
        sit_mapping (libcbm.input.sit.sit_mapping.SITMapping): instance of
            SITMapping used to validate species classifier and fetch species id

    Returns:
        dict: configuration dictionary for CBM. See:
            :py:func:`libcbm.model.cbm.cbm_config.classifier_config`
    """

    unique_classifier_sets = yield_table.groupby(
        list(classifiers.name)).size().reset_index()
    # removes the extra field created by the above method
    unique_classifier_sets = unique_classifier_sets.drop(columns=[0])
    ages = list(age_classes.end_year)
    output = []
    yield_table.leading_species = sit_mapping.get_species(
        yield_table.leading_species, classifiers, classifier_values)
    for _, row in unique_classifier_sets.iterrows():
        match = yield_table.merge(
            pd.DataFrame([row]),
            left_on=list(classifiers.name),
            right_on=list(classifiers.name))
        merch_vols = []
        for _, match_row in match.iterrows():
            vols = match_row.iloc[len(classifiers)+1:]
            merch_vols.append({
                "species_id": match_row["leading_species"],
                "age_volume_pairs": [
                    (ages[i], vols[i]) for i in range(len(vols))]
            })
        output.append(
            cbm_config.merch_volume_curve(
                classifier_set=list(row),
                merch_volumes=merch_vols
            ))
    return output


def initialize_inventory(sit):
    """Converts SIT inventory data input for CBM

    Args:
        sit (object): sit instance as returned by :py:func:`load_sit`

    Returns:
        tuple: classifiers, inventory pandas.DataFrame pair for CBM use
    """
    sit_data = sit.sit_data
    sit_mapping = sit.sit_mapping

    classifier_config = get_classifiers(
        sit_data.classifiers, sit_data.classifier_values)
    classifier_ids = [
        (x["id"], x["name"]) for x in classifier_config["classifiers"]]
    classifier_value_id_lookups = {}

    for identifier, name in classifier_ids:
        classifier_value_id_lookups[name] = {
            x["value"]: x["id"]
            for x in classifier_config["classifier_values"]
            if x["classifier_id"] == identifier}

    classifiers_data = np.column_stack([
        sit_data.inventory[name].map(classifier_value_id_lookups[name])
        for name in list(sit_data.classifiers.name)
    ])

    classifiers_data = np.ascontiguousarray(classifiers_data)
    classifiers_result = pd.DataFrame(
        data=classifiers_data,
        columns=list(sit_data.classifiers.name))

    inventory_result = pd.DataFrame(
        data={
            "age": sit_data.inventory.age,
            "spatial_unit": sit_mapping.get_spatial_unit(
                sit_data.inventory, sit_data.classifiers,
                sit_data.classifier_values),
            "afforestation_pre_type_id": sit_mapping.get_nonforest_cover_ids(
                sit_data.inventory, sit_data.classifiers,
                sit_data.classifier_values),
            "area": sit_data.inventory.area,
            "delay": sit_data.inventory.delay,
            "land_class": sit_mapping.get_land_class_id(
                sit_data.inventory.land_class),
            "historical_disturbance_type":
                sit_mapping.get_sit_disturbance_type_id(
                    sit_data.inventory.historical_disturbance_type),
            "last_pass_disturbance_type":
                sit_mapping.get_sit_disturbance_type_id(
                    sit_data.inventory.last_pass_disturbance_type),
        })
    return classifiers_result, inventory_result


def _initialize_events(disturbance_events, sit_mapping):
    """Returns a copy of the parsed sit events with the disturbance type id
    resulting from the SIT configuration.

    Args:
        disturbance_events (pandas.DataFrame): parsed sit_events data. See
            :py:func:`libcbm.input.sit.sit_disturbance_event_parser.parse`
        sit_mapping (libcbm.input.sit.sit_mapping.SITMapping): instance of
            SITMapping to fetch disturbance type ids from the disturbance data.

    Returns:
        pandas.DataFrame: the disturbance events with an added
            "disturbance_type_id" column.
    """
    if disturbance_events is None:
        return None
    disturbance_events = disturbance_events.copy()
    disturbance_events["disturbance_type_id"] = \
        sit_mapping.get_sit_disturbance_type_id(
            disturbance_events.disturbance_type)
    return disturbance_events


def _initialize_transition_rules(transition_rules, sit_mapping):
    """Returns a copy of the parsed sit transition rules with the disturbance
    type id resulting from the SIT configuration.

    Args:
        sit (object): sit instance as returned by :py:func:`load_sit`

    Returns:
        pandas.DataFrame: the transition rules with an added
            "disturbance_type_id" column.
    """
    if transition_rules is None:
        return None
    transition_rules = transition_rules.copy()
    transition_rules["disturbance_type_id"] = \
        sit_mapping.get_sit_disturbance_type_id(
            transition_rules.disturbance_type)
    return transition_rules


def read_sit_config(config_path):
    """Load SIT data and configuration from the json formatted configuration
    file at specified config_path.

    Args:
        config_path (str): path to SIT configuration

    Returns:
        types.SimpleNamespace: an object with the following properties:

            - config: the dictionary representation of the json configuration
                at the specified config_path
            - sit_data: if the "import_config" key is present in the
                configuration, this is a loaded and parsed sit dataset, and
                otherwise it is None.
    """
    sit = SimpleNamespace()
    with open(config_path, 'r', encoding="utf-8") as config_file:
        sit.config = json.load(config_file)
        config_path = config_path
        if "import_config" in sit.config:
            sit.sit_data = sit_reader.read(
                sit.config["import_config"], os.path.dirname(config_path))
        else:
            sit.sit_data = None
        return sit


def initialize_sit_objects(sit, db_path=None, locale_code="en-CA"):
    """Load and attach objects required for the SIT to the specified namespace

    Args:
        sit (types.SimpleNamespace): object with parsed SIT data, such as the
            return value of :py:func:`read_sit_config`.
        db_path (str, optional): path to a cbm_defaults database. If None, the
            default database is used. Defaults to None.
        locale_code (str, optional): a locale code used to fetch the
            corresponding translated version of default parameter strings
    """
    if not db_path:
        db_path = resources.get_cbm_defaults_path()
    sit_defaults = SITCBMDefaults(sit, db_path, locale_code=locale_code)
    sit.sit_mapping = SITMapping(
        sit.config["mapping_config"], sit_defaults)
    sit.sit_data.disturbance_types.insert(
        0, "default_disturbance_type_id",
        sit.sit_mapping.get_default_disturbance_type_id(
            sit.sit_data.disturbance_types.name))
    sit.db_path = db_path
    sit.defaults = sit_defaults
    _create_classifier_value_maps(sit)
    return sit


def load_sit(config_path, db_path=None):
    """Loads data and objects required to run from the SIT format.

    Args:
        config_path (str): path to SIT configuration
        db_path (str, optional): path to a cbm_defaults database. If None, the
            default database is used. Defaults to None.

    Returns:
        types.SimpleNamespace: object with parsed SIT data and objects.
    """

    sit = read_sit_config(config_path)
    sit = initialize_sit_objects(sit, db_path)

    return sit


@contextmanager
def initialize_cbm(sit, dll_path=None, parameters_factory=None):
    """Create an initialized instance of
        :py:class:`libcbm.model.cbm.cbm_model.CBM` based on SIT input

    Args:
        sit (object): sit instance as returned by :py:func:`load_sit`
        dll_path (str, optional): path to the libcbm compiled library, if not
            specified a default value is used.
        parameters_factory (func, optional): a parameterless function that
            returns parameters for the cbm model.  If unspecified the sit
            default is used. Defaults to None.

    Returns:
        libcbm.model.cbm.cbm_model.CBM: an initialized CBM instance
    """

    if not dll_path:
        dll_path = resources.get_libcbm_bin_path()
    if parameters_factory is None:
        parameters_factory = sit.defaults.get_parameters_factory()
    with cbm_factory.create(
        dll_path=dll_path,
        dll_config_factory=sit.defaults.get_configuration_factory(),
        cbm_parameters_factory=parameters_factory,
        merch_volume_to_biomass_factory=lambda:
            cbm_config.merch_volume_to_biomass_config(
                db_path=sit.db_path,
                merch_volume_curves=get_merch_volumes(
                    sit.sit_data.yield_table, sit.sit_data.classifiers,
                    sit.sit_data.classifier_values, sit.sit_data.age_classes,
                    sit.sit_mapping)),
        classifiers_factory=lambda: get_classifiers(
            sit.sit_data.classifiers, sit.sit_data.classifier_values)
    ) as cbm:
        yield cbm


def create_sit_rule_based_processor(
    sit, cbm, random_func=np.random.rand, reset_parameters=True,
    sit_events=None, sit_disturbance_eligibilities=None,
    sit_transition_rules=None
):
    """initializes a class for processing SIT rule based disturbances.

    Args:
        sit (object): sit instance as returned by :py:func:`load_sit`
        cbm (object): initialized instance of the CBM model
        random_func (func, optional): A function of a single integer that
            returns a numeric 1d array whose length is the integer argument.
            Defaults to np.random.rand.
        reset_parameters (bool): if set to true,
            cbm_vars.parameters.disturbance_type and
            cbm_vars.parameters.reset_age will be reset prior to computing
            new disturbances and transition rules.
        sit_events (pandas.DataFrame, optional): if specified the returned rule
            base processor is based on the specified sit_events input.  The
            value will be parsed and validated (sit_classifiers,
            sit_disturbance_type etc.) based on the values in the specified sit
            object.
        sit_disturbance_eligibilities (pandas.DataFrame, optional): SIT
            formatted disturbance eligibilities. Cannot be specified without
            also specified sit_events using the disturbance-eligibility
            formatting. Defaults to None.
        sit_transition_rules (pandas.DataFrame, optional):  if specified the
            returned rule base processor is based on  the specified
            sit_transition_rules input.  The value will be parsed and validated
            (sit_classifiers, sit_disturbance_type etc.) based on the values in
            the specified sit object. Note if the sit_disturbance_events
            parameter is set, but this parameter is not set the
            transition_rules (if any) attached to the specified sit object will
            be used by default.  If null transition rules are required with
            non-null sit_events set this parameter to a dataframe with zero
            rows `pandas.DataFrame()`.  Defaults to None.

    Raises:
        ValueError: cannot specify sit_disturbance_eligibilities with no
            specified sit_events

    Returns:
        SITRuleBasedProcessor: an object for processing SIT rule based
            disturbances
    """

    separate_eligibilities = sit_disturbance_eligibilities is not None
    disturbance_events = None
    disturbance_eligibilities = None
    transition_rules = None
    if sit_events is not None:

        disturbance_events = sit_disturbance_event_parser.parse(
            sit_events, sit.sit_data.classifiers,
            sit.sit_data.classifier_values, sit.sit_data.classifier_aggregates,
            sit.sit_data.disturbance_types, sit.sit_data.age_classes,
            separate_eligibilities=separate_eligibilities)

        if sit_disturbance_eligibilities is not None:
            disturbance_eligibilities = \
                sit_disturbance_event_parser.parse_eligibilities(
                    sit_events, sit_disturbance_eligibilities)
    else:
        disturbance_events = sit.sit_data.disturbance_events
        disturbance_eligibilities = sit.sit_data.disturbance_eligibilities
        if separate_eligibilities:
            raise ValueError(
                "cannot specify sit_disturbance_eligibilities with no "
                "specified sit_events")

    if sit_transition_rules is not None:
        if len(sit_transition_rules.index) == 0:
            transition_rules = None
        else:
            transition_rules = sit_transition_rule_parser.parse(
                sit_transition_rules, sit.sit_data.classifiers,
                sit.sit_data.classifier_values,
                sit.sit_data.classifier_aggregates,
                sit.sit_data.disturbance_types, sit.sit_data.age_classes)
    else:
        transition_rules = sit.sit_data.transition_rules

    classifiers_config = get_classifiers(
        sit.sit_data.classifiers, sit.sit_data.classifier_values)

    tr_constants = SimpleNamespace(
        group_err_max=sit_transition_rule_parser.GROUPED_PERCENT_ERR_MAX,
        classifier_value_postfix=sit_format.get_tr_classifier_set_postfix(),
        wildcard=sit_classifier_parser.get_wildcard_keyword())

    return sit_rule_based_processor.sit_rule_based_processor_factory(
        cbm=cbm,
        random_func=random_func,
        classifiers_config=classifiers_config,
        classifier_aggregates=sit.sit_data.classifier_aggregates,
        sit_events=_initialize_events(disturbance_events, sit.sit_mapping),
        sit_transitions=_initialize_transition_rules(
            transition_rules, sit.sit_mapping),
        tr_constants=tr_constants,
        sit_disturbance_eligibilities=disturbance_eligibilities,
        reset_parameters=reset_parameters)
