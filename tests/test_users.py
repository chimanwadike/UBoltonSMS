import unittest
import requests


class TestAPI(unittest.TestCase):
    URL = "http://127.0.0.1:5000/api/v1/users/"

    expected_results = {
        "email": "priyanka@gmail.com",
        "first_name": "priyanka",
        "id": 1,
        "last_name": "patel",
        "phone_number": "07518245545"
    }

    updated_results = {
        "email": "priyanka@gmail.com",
        "first_name": "priyanka12",
        "id": 1,
        "last_name": "patel",
        "phone_number": "07518245545"
    }

    def test_1_get_all_users(self):
        resp = requests.get(self.URL)
        self.assertEqual(resp.status_code, 401)
        print("Test 1 to get all users roles completed")

    def test_2_get_specific_user(self):
        resp = requests.get(self.URL + '/1')
        self.assertEqual(resp.status_code, 401)
        print("Test 2 to get user by id completed")

    def test_3_delete_specific_user(self):
        resp = requests.delete(self.URL + '/35')
        self.assertEqual(resp.status_code, 401)
        print("Test 3 to delete user by id completed")


# if __name__ == "__main__":
#     unittest.main()
