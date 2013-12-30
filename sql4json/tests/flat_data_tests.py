import unittest

from sql4json.flat_data import FlatData


class FlatDataTests(unittest.TestCase):
    def test_flatten_simple_data(self):
        data = {"a": 1, "b": "string", "c": True}
        flat_data = FlatData(data)

        self.assertEqual(["a", "b", "c"], flat_data.get_headers())
        self.assertEqual([[1, "string", True]], flat_data.get_rows())

    def test_multiple_rows(self):
        data = [{"a": 1, "b": "string", "c": True}, {"a": 2, "b": "other", "c": False}]
        flat_data = FlatData(data)

        self.assertEqual(["a", "b", "c"], flat_data.get_headers())
        self.assertEqual([[1, "string", True], [2, "other", False]], flat_data.get_rows())

    def test_objects_with_different_fields(self):
        data = [{"a": 1, "b": "string"}, {"a": 2, "c": False}]
        flat_data = FlatData(data)

        self.assertEqual(["a", "b", "c"], flat_data.get_headers())
        self.assertEqual([[1, "string", None], [2, None, False]], flat_data.get_rows())

    def test_flatten_complex_hierarchy(self):
        data = [
            {
                "id": 1,
                "first_name": "Brian",
                "employer": {
                    "id": 1,
                    "name": "Some Company",
                    "addresses": [
                        {"address1": "123 Fake Street", "city": "Venice", "state": "CA"},
                        {"address1": "456 Real Ave", "address2": "Suite 13", "city": "San Francisco", "state": "CA"}
                    ]
                }
            },
            {
                "id": 2,
                "first_name": "David",
                "employer": {
                    "id": 2,
                    "name": "Other Company",
                }
            },
            {
                "id": 3,
                "first_name": "Logan"
            }
        ]

        flat_data = FlatData(data)

        expected_headers = [
            "employer/addresses[0]/address1",
            "employer/addresses[0]/city",
            "employer/addresses[0]/state",
            "employer/addresses[1]/address1",
            "employer/addresses[1]/address2",
            "employer/addresses[1]/city",
            "employer/addresses[1]/state",
            "employer/id",
            "employer/name",
            "first_name",
            "id"
        ]

        self.assertEqual(expected_headers, flat_data.get_headers())

        expected_rows = [
            ["123 Fake Street", "Venice", "CA", "456 Real Ave", "Suite 13", "San Francisco", "CA", 1, "Some Company",
             "Brian", 1],
            [None, None, None, None, None, None, None, 2, "Other Company", "David", 2],
            [None, None, None, None, None, None, None, None, None, "Logan", 3]
        ]

        self.assertEqual(expected_rows, flat_data.get_rows())

    def test_flatten_complex_hierarchy_with_ordered_output(self):
        data = [
            {
                "id": 1,
                "first_name": "Brian",
                "employer": {
                    "id": 1,
                    "name": "Some Company",
                    "addresses": [
                        {"address1": "123 Fake Street", "city": "Venice", "state": "CA"},
                        {"address1": "456 Real Ave", "address2": "Suite 13", "city": "San Francisco", "state": "CA"}
                    ]
                }
            },
            {
                "id": 2,
                "first_name": "David",
                "employer": {
                    "id": 2,
                    "name": "Other Company",
                }
            },
            {
                "id": 3,
                "first_name": "Logan"
            }
        ]

        flat_data = FlatData(data, ("id", "first_name", "employer/id", "employer/name"))

        expected_headers = [
            "id",
            "first_name",
            "employer/id",
            "employer/name",
            "employer/addresses[0]/address1",
            "employer/addresses[0]/city",
            "employer/addresses[0]/state",
            "employer/addresses[1]/address1",
            "employer/addresses[1]/address2",
            "employer/addresses[1]/city",
            "employer/addresses[1]/state",

        ]

        self.assertEqual(expected_headers, flat_data.get_headers())

        expected_rows = [
            [1, "Brian", 1, "Some Company", "123 Fake Street", "Venice", "CA", "456 Real Ave", "Suite 13", "San Francisco", "CA"],
            [2, "David", 2, "Other Company", None, None, None, None, None, None, None],
            [3, "Logan", None, None, None, None, None, None, None, None, None]
        ]

        self.assertEqual(expected_rows, flat_data.get_rows())
