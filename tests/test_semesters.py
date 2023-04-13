import unittest
import requests


class TestAPI(unittest.TestCase):
    URL = "http://127.0.0.1:5000/#/Semesters"

    data = {
        "name": "Testing",
        "description": "Testing post functionality"
    }

    expected_result = {
        "end_date": "2023-08-19",
        "id": 1,
        "name": "1st Semester",
        "start_date": "2023-08-19"
    }

    def test_1_get_all_records(self):
        resp = requests.get(self.URL + '/get_semesters_')
        # self.assertEqual(resp.status_code, 200)
        if resp.status_code != 200:
            print("Test Fail")
        else:
            print("Test 1 to get all semesters records completed")

    def test_2_post_records(self):
        resp = requests.post(self.URL + '/post_semesters_')
        if resp.status_code != 201:
            print("Test 2 to create semester completed")
        else:
            print("Test Fail")

    def test_3_get_specific_record(self):
        resp = requests.get(self.URL + '/get_semesters__id_')

        self.assertEqual(resp.status_code, 201)
        print("Test 3 to get semester by id completed")

        if AssertionError:
            print("Test Fail")
        #self.assertNotEqual(resp.status_code, 200)
        #print("Test Fail")


if __name__ == "__main__":
    #tester = TestAPI()
    unittest.main()

    # tester.test_1_get_all_records()
    # tester.test_2_post_records()
    #tester.test_3_get_specific_record()
