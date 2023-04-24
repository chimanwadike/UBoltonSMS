import unittest
import requests


class TestAPI(unittest.TestCase):
    URL = "http://127.0.0.1:5000/api/v1/semesters/"

    data = {
        "end_date": "2026-02-19",
        "name": "13th Semester",
        "start_date": "2025-03-19"
    }

    expected_results = {
        "end_date": "2023-08-19",
        "id": 1,
        "name": "1st Semester",
        "start_date": "2023-08-19"
    }

    updated_results = {
        "end_date": "2023-08-19",
        "name": "4th Term",
        "start_date": "2023-08-19"
    }

    def test_1_get_all_records(self):
        resp = requests.get(self.URL)
        self.assertEqual(resp.status_code, 200)
        print("Test 1 to get all semesters records completed")

    def test_2_post_records(self):
        resp = requests.post(self.URL, json=self.data)
        self.assertEqual(resp.status_code, 201)
        print("Test 2 to create semester completed")


    def test_3_get_specific_record(self):
        resp = requests.get(self.URL + '/2')
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), self.expected_results)
        print("Test 3 to get semester by id completed")

    def test_4_delete_specific_record(self):
        resp = requests.delete(self.URL + '/5')
        self.assertEqual(resp.status_code, 201)
        print("Test 4 to delete semester by id completed")

    def test_5_update_specific_record(self):
        resp = requests.put(self.URL + '/2', json=self.updated_results)
        self.assertEqual(resp.json()['name'], self.updated_results['name'])
        print("Test 5 to update semester completed")


if __name__ == "__main__":
    # tester = TestAPI()
    unittest.main()

    # tester.test_1_get_all_records()
    # tester.test_2_post_records()
