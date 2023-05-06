import unittest
import requests


class TestAPI(unittest.TestCase):
    URL = "http://127.0.0.1:5000/api/v1/roles/"

    data = {
        "display_name": "Student",
        "name": "Student"
    }

    expected_results = {
        "display_name": "User",
        "id": 2,
        "name": "User"
    }

    updated_results = {
        "name": "User1",
        "display_name": "User"
    }

    def test_1_get_all_roles(self):
        resp = requests.get(self.URL)
        self.assertEqual(resp.status_code, 401)
        print("Test 1 to get all roles roles completed")

    def test_2_post_role(self):
        resp = requests.post(self.URL, json=self.data)
        self.assertEqual(resp.status_code, 401)
        print("Test 2 to create role completed")

    def test_3_get_specific_role(self):
        resp = requests.get(self.URL + '/2')
        self.assertEqual(resp.status_code, 401)
        print("Test 3 to get role by id completed")

    def test_4_delete_specific_role(self):
        resp = requests.delete(self.URL + '/5')
        self.assertEqual(resp.status_code, 401)
        print("Test 4 to delete role by id completed")
#
# if __name__ == "__main__":
#     unittest.main()
