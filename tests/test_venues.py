import unittest
import requests


class TestAPI(unittest.TestCase):
    URL = "http://127.0.0.1:5000/api/v1/venues/"

    data = {
        "building": "Block E",
        "name": "E01"
    }

    expected_results = {
        "building": "Senate House",
        "id": 1,
        "name": "B01"
    }

    updated_results = {
        "name": "C0001",
        "building": "Senate House"
    }

    def test_1_get_all_venues(self):
        resp = requests.get(self.URL)
        self.assertEqual(resp.status_code, 401)
        print("Test 1 to get all venues records completed")

    def test_2_post_venue(self):
        resp = requests.post(self.URL, json=self.data)
        self.assertEqual(resp.status_code, 401)
        print("Test 2 to create venue completed")

    def test_3_get_specific_venue(self):
        resp = requests.get(self.URL + '/1')
        self.assertEqual(resp.status_code, 401)
        print("Test 3 to get venue by id completed")

    def test_4_delete_specific_venue(self):
        resp = requests.delete(self.URL + '/4')
        self.assertEqual(resp.status_code, 401)
        print("Test 4 to delete venue by id completed")


# if __name__ == "__main__":
#     unittest.main()
