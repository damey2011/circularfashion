import json

from django.urls import reverse

from materials.tests.test_funcs import TestSetup
from materials.tests.utils import recursively_assert_values


class TestCFAPI(TestSetup):
    def test_that_recycler_endpoint_returns_valid_data(self):
        self.create_quality()
        response = self.client.get(reverse('materials:recyclers'))
        self.assertEqual(response.status_code, 200)
        expected_data = json.loads("""[
            {
                "id": 1,
                "name": "Recycler 1",
                "qualities": [
                    {
                        "id": 1,
                        "title": "Quality Best",
                        "min_count": 1,
                        "material": {
                            "id": 1,
                            "name": "Material 1",
                            "attributes": "http://testserver/api/materials/1/attributes/",
                            "attributes_count": 18
                        },
                        "condition": "(4 and (8 * 8 * 8) and ATTR_POLYESTER)",
                        "operations": [
                            {
                                "operands": [
                                    4,
                                    {
                                        "operands": [
                                            8,
                                            8,
                                            8
                                        ],
                                        "operator": "*"
                                    },
                                    "ATTR_POLYESTER"
                                ],
                                "operator": "and"
                            }
                        ],
                        "passed": true
                    }
                ]
            }
        ]""")
        recursively_assert_values(expected_data, response.json(), 0, 'data')
