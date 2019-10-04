from libcbm.model.cbm.rule_based import rule_filter
from libcbm.model.cbm.rule_based.classifier_filter import ClassifierFilter


def get_pool_variable_filter_mappings():
    return [
        ("MinTotBiomassC", "", ""),
        ("MaxTotBiomassC", "", ""),
        ("MinSWMerchBiomassC", "", ""),
        ("MaxSWMerchBiomassC", "", ""),
        ("MinHWMerchBiomassC", "", ""),
        ("MaxHWMerchBiomassC", "", ""),
        ("MinTotalStemSnagC", "", ""),
        ("MaxTotalStemSnagC", "", ""),
        ("MinSWStemSnagC", "", ""),
        ("MaxSWStemSnagC", "", ""),
        ("MinHWStemSnagC", "", ""),
        ("MaxHWStemSnagC", "", ""),
        ("MinTotalStemSnagMerchC", "", ""),
        ("MaxTotalStemSnagMerchC", "", ""),
        ("MinSWMerchStemSnagC", "", ""),
        ("MaxSWMerchStemSnagC", "", ""),
        ("MinHWMerchStemSnagC", "", ""),
        ("MaxHWMerchStemSnagC", "", "")]


def get_state_variable_age_filter_mappings():
    """get mappings between SIT events or transitions age criteria columns,
    and state variable columns, along with a boolean operator to compare age
    values.

    Returns:
        list: a list of (str, str, str) tuples in format

             - SIT_Event column name
             - state variable column name
             - operator string
    """
    return [
        ("min_age", "age", ">="),
        ("max_age", "age", "<=")]


def get_state_variable_filter_mappings():
    """get mappings between SIT events criteria columns, and state variable
    columns, along with a boolean operator to compare values.

    Returns:
        list: a list of (str, str, str) tuples in format

             - SIT_Event column name
             - state variable column name
             - operator string

    """
    return get_state_variable_age_filter_mappings() + [
        ("MinYearsSinceDist", "time_since_last_disturbance", ">="),
        ("MaxYearsSinceDist", "time_since_last_disturbance", "<="),
        ("LastDistTypeID", "last_disturbance_type", "==")]


def create_state_variable_filter(create_filter, sit_data, state_variables,
                                 filter_mappings):
    """Create a filter against simulation state variables based on a single
    row of SIT disturbance event, or transition rule data.

    Args:
        create_filter (func): a function to create a filter.
            :py:func:`libcbm.model.cbm.rule_based.rule_filter.create_filter`
        sit_data (dict): a row dictionary from an SIT events, or SIT
            transition rules table
        state_variables (pandas.DataFrame): simulation state variables
        filter_mappings (list): the return value of either:

            - :py:func:`get_state_variable_filter_mappings`
              (for use with sit events)
            - :py:func:`get_state_variable_age_filter_mappings`
              (for use with sit transition rules)

    Returns:
        object: a filter object for use with :py:mod:`libcbm.model.cbm`
    """

    columns = []
    expression_tokens = []
    for sit_column, state_variable_column, operator in filter_mappings:

        if sit_data[sit_column] < 0:
            # by convention, SIT criteria less than 0 are considered null criteria
            continue
        columns.append(sit_column)
        expression_tokens.append(
            "({state_variable} {operator} {value})".format(
                state_variable=state_variable_column,
                operator=operator,
                value=sit_data[sit_column]
            ))

    expression = " & ".join(expression_tokens)
    return create_filter(
        expression, state_variables, columns=columns)


def create_classifier_filter(sit_data, classifier_values,
                             classifier_filter_builder):
    classifier_set = [
        sit_data[x] for x in classifier_values.columns.values.tolist()]
    return classifier_filter_builder.create_classifiers_filter(
        classifier_set, classifier_values)