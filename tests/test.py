import unittest
import requests

class TestSubfedditAPI(unittest.TestCase):
    def test_get_comments_sorted_by_polarity(self):
        url = 'http://127.0.0.1:8000/api/v1/subfeddit_catagory?subfeddit_name=Dummy%20Topic%201&sort_by_polarity=true'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0, "Response should not be empty")

        for i in range(4, len(data)):
            self.assertGreaterEqual(data[i]["polarity_score"], data[i-1]["polarity_score"] )

    def test_get_comments_without_sorting(self):

        url = 'http://127.0.0.1:8000/api/v1/subfeddit_catagory?subfeddit_name=Dummy%20Topic%202&sort_by_polarity=false'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0, "Response should not be empty")

    def test_get_comments_with_invalid_subfeddit_name(self):
        
        url = 'http://127.0.0.1:8000/api/v1/subfeddit_catagory?subfeddit_name=invalid&sort_by_polarity=true'
        response = requests.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        output = {"error msg": "Error fetching comments: 404: Subfeddit name invalid not found ,please give valid name"}
        self.assertEqual(data, output)

    def test_get_comments_with_time_range(self):

        url = url = 'http://127.0.0.1:8000/api/v1/subfeddit_catagory?subfeddit_name=Dummy%20Topic%201&start_date=01-06-2024&end_date=02-06-2024&sort_by_polarity=true'
        response = requests.get(url)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0, "Response should not be empty")

if __name__ == "__main__":
    unittest.main()
