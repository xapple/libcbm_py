import unittest
import pandas as pd
from libcbm.model.cbm.rule_based.classifier_filter import ClassifierFilter


def get_mock_classifiers_config():
    return {
            "classifiers": [
                {"id": 1, "name": "c1"},
                {"id": 2, "name": "c2"},
                {"id": 3, "name": "c3"}
            ],
            "classifier_values": [
                {"id": 1, "classifier_id": 1, "value": "c1_v1"},
                {"id": 2, "classifier_id": 1, "value": "c1_v2"},
                {"id": 3, "classifier_id": 2, "value": "c2_v1"},
                {"id": 4, "classifier_id": 2, "value": "c2_v2"},
                {"id": 5, "classifier_id": 3, "value": "c3_v1"},
                {"id": 6, "classifier_id": 3, "value": "c3_v2"},
                {"id": 7, "classifier_id": 3, "value": "c3_v3"}
            ]
        }


class ClassifierFilterTest(unittest.TestCase):

    def test_create_classifiers_filter_expected_value(self):

        classifier_set = ["c1_v1", "?", "agg1"]
        classifiers_config = get_mock_classifiers_config()
        classifier_aggregates = [
            {'classifier_id': 3,
             'name': 'agg1',
             'description': 'agg1',
             'classifier_values': ['c3_v1', 'c3_v3']}]

        rule_filter = ClassifierFilter(
            classifiers_config, classifier_aggregates)

        def get_classifier_value_index(classifier_id):
            return {
                x["value"]: x["id"] for x
                in classifiers_config["classifier_values"]
                if x["classifier_id"] == classifier_id}

        c1 = get_classifier_value_index(1)
        c2 = get_classifier_value_index(2)
        c3 = get_classifier_value_index(3)

        classifier_values = pd.DataFrame(
            [
                (c1[x[0]], c2[x[1]], c3[x[2]])
                for x in [
                    ("c1_v1", "c2_v1", "c3_v3"),  # match
                    ("c1_v2", "c2_v1", "c3_v3"),  # non-match (c1_v2)
                    ("c1_v1", "c2_v2", "c3_v3"),  # match
                    ("c1_v1", "c2_v2", "c3_v1"),  # match
                    ("c1_v1", "c2_v2", "c3_v2")]  # non-match (aggregate)
            ],
            columns=["c1", "c2", "c3"])

        result = rule_filter.create_classifiers_filter(
            classifier_set, classifier_values)
        self.assertTrue(
            result.expression == "(c_0 == 1) & ((c_2 == 5) | (c_2 == 7))")
        self.assertTrue(list(result.local_dict["c_0"]) == [1, 2, 1, 1, 1])
        self.assertTrue(list(result.local_dict["c_1"]) == [3, 3, 4, 4, 4])
        self.assertTrue(list(result.local_dict["c_2"]) == [7, 7, 7, 5, 6])

    def test_create_classifiers_filter_expected_value_all_wildcards(self):

        classifier_set = ["?", "?", "?"]
        classifiers_config = get_mock_classifiers_config()
        classifier_aggregates = [
            {'classifier_id': 3,
             'name': 'agg1',
             'description': 'agg1',
             'classifier_values': ['c3_v1', 'c3_v3']}]

        rule_filter = ClassifierFilter(
            classifiers_config, classifier_aggregates)

        def get_classifier_value_index(classifier_id):
            return {
                x["value"]: x["id"] for x
                in classifiers_config["classifier_values"]
                if x["classifier_id"] == classifier_id}

        c1 = get_classifier_value_index(1)
        c2 = get_classifier_value_index(2)
        c3 = get_classifier_value_index(3)

        classifier_values = pd.DataFrame(
            [
                (c1[x[0]], c2[x[1]], c3[x[2]])
                for x in [
                    ("c1_v1", "c2_v1", "c3_v3"),  # match
                    ("c1_v2", "c2_v1", "c3_v3"),  # non-match (c1_v2)
                    ("c1_v1", "c2_v2", "c3_v3"),  # match
                    ("c1_v1", "c2_v2", "c3_v1"),  # match
                    ("c1_v1", "c2_v2", "c3_v2")]  # non-match (aggregate)
            ],
            columns=["c1", "c2", "c3"])

        result = rule_filter.create_classifiers_filter(
            classifier_set, classifier_values)
        self.assertTrue(result.expression == "")
        self.assertTrue(result.local_dict == {})

    def test_error_on_mismatching_classifiers(self):
        """check that an error is raised on mismatch in the number of
        classifiers
        """
        classifiers_config = get_mock_classifiers_config()

        rule_filter = ClassifierFilter(
            classifiers_config, [])

        with self.assertRaises(ValueError):
            rule_filter.create_classifiers_filter(
                ["c1_v1", "?", "agg1", "extra"],
                pd.DataFrame([[1, 3, 5]]))

        with self.assertRaises(ValueError):
            rule_filter.create_classifiers_filter(
                ["c1_v1", "?"],  # one too few
                pd.DataFrame([[1, 3, 5]]))

        with self.assertRaises(ValueError):
            rule_filter.create_classifiers_filter(
                ["c1_v1", "?", "agg1"],
                pd.DataFrame([[1, 3]]))  # not enough columns in dataframe

        with self.assertRaises(ValueError):
            rule_filter.create_classifiers_filter(
                ["c1_v1", "?", "agg1"],
                pd.DataFrame([[1, 3, 5, 1]]))  # too many columns in dataframe

    def test_error_on_undefined_value_in_classifier_set(self):
        """check that an error is raised on when classifier value in
        the specified classifier set is not defined
        """
        classifiers_config = get_mock_classifiers_config()

        rule_filter = ClassifierFilter(
            classifiers_config, [])

        with self.assertRaises(ValueError):
            rule_filter.create_classifiers_filter(
                ["undefined", "?", "agg1"],
                pd.DataFrame([[1, 3, 5]]))
