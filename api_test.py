import unittest
import requests
import datetime

class FlaskTest(unittest.TestCase):

    #Defining URL'S
    API_URL = "http://127.0.0.1:5000/api"
    WEBHOOK_URL = "{}/webhook".format(API_URL)
    OCCUPANCY_URL = "{}/occupancy".format(API_URL)
    
    #Function to return the current date
    def current_datetime():
        x = datetime.datetime.now()
        return x.strftime("%Y-%m-%d %H:%M:%S")

    #Test request object with 0 into and 0 out to avoid affecting occupancy
    REQ_OBJ = {
        "sensor":"hij",
        "time": current_datetime(),
        "into":2,
        "out":0
    }

    #GET request to /api listing all sensor entries
    def test_1_get_all_requests(self):
        r = requests.get(FlaskTest.API_URL)
        self.assertEqual(r.status_code, 200)

    #POST request to /api/webhook adding a sensor entry
    def test_2_add_new_request(self):
        r = requests.post(FlaskTest.WEBHOOK_URL, json=FlaskTest.REQ_OBJ)
        self.assertEqual(r.status_code, 201)

    #GET request to /api/occupancy to get the occupancy on specific sensor and date
    def test_3_get_occupancy(self):
        r = requests.get(FlaskTest.OCCUPANCY_URL+"?sensor=hij&atInstant="+FlaskTest.current_datetime())
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(r.json()['inside'], 1)

        