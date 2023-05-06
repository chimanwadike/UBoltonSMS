import unittest
import requests


class TestAPI(unittest.TestCase):
    URL = "http://127.0.0.1:5000/api/v1/courses/"

    data = {
        "description": "This course explores advance software concepts",
        "name": "Advance Software Development"
    }

    expected_results = {
        "description": "This course explores advance software concepts",
        "id": 1,
        "name": "Advance Software Development"
    }

    updated_results = {
        "description": "This course explores advance software concepts",
        "id": 1,
        "name": "Advance Software Development"
    }

    def test_1_get_all_courses(self):
        resp = requests.get(self.URL)
        self.assertEqual(resp.status_code, 401)
        print("Test 1 to get all courses records completed")

    def test_2_post_course(self):
        resp = requests.post(self.URL, json=self.data)
        self.assertEqual(resp.status_code, 401)
        print("Test 2 to create course completed")

    def test_3_get_specific_course(self):
        resp = requests.get(self.URL + '/1')
        self.assertEqual(resp.status_code, 401)
        print("Test 3 to get course by id completed")

    def test_4_delete_specific_course(self):
        resp = requests.delete(self.URL + '/4')
        self.assertEqual(resp.status_code, 401)
        print("Test 4 to delete course by id completed")

#if __name__ == "__main__":
    #unittest.main()
