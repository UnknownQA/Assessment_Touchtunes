import unittest
import requests
import requests_api_pagination


class TestDiscogs(unittest.TestCase):
    key = "yVkSPQlrfEVJkSHeSIOJ"
    secret = "NNHMrjqXNSzDYCnaXyesWGogwYfOSNmh"
    discog_url = "https://api.discogs.com/database"
    discog_pagination_url = "https://api.discogs.com/artists/1/releases?page=2&"
    invalid_key = "abcd"

    @classmethod
    def setUpClass(self):
        auth1 = "Discogs key={}, secret={}".format(self.key, self.secret)
        auth2 = "Discogs key={}, secret={}".format(self.invalid_key, self.secret)
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": auth1
        }
        self.headers2 ={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": auth2
        }


    def test_basic_response(self):
        res = requests.get("{}/search".format(self.discog_url), headers=self.headers)

        print(res.request)
        print(res.json())

    def test_authorized_search(self):
        res = requests.get("{}/search".format(self.discog_url), headers=self.headers)
        print('Current status code is {}'.format(res.status_code))
        statuscode = res.status_code
        if statuscode == 200:
            print('User has authorized search access')
        else:
            print('user Invalid/is unauthorized')

    def test_invalid_credential(self):
        res = requests.get("{}/search".format(self.discog_url), headers=self.headers2)
        print('Current status code is {} '.format(res.status_code))
        statuscode = res.status_code
        if statuscode == 401:
            print('User is Invalid/unauthorized for accessing data')

    def test_no_limits_pagination(self):
        default_items = 50
        max_items = 100

        limit = input('Do you want to specify any limits for records per page? Enter Y/N : ')

        if any(limit.lower()== a for a in ['n','no',0]):
            print('No Limit is specified, Printing default number of items');
            res = requests.get("{}per_page={}".format(self.discog_pagination_url,default_items), headers=self.headers)
            print(res.json())

        elif any(limit.lower()== a for a in ['y','yes',1]):
            records_per_page = input("Enter the number of records you want to display per page : ")
            limits_per_page = int(records_per_page)
            print(limits_per_page)
            if (limits_per_page < 1):
                print('Entered limits per page is invalid');
            elif(limits_per_page <= 100):
                res = requests.get("{}per_page={}".format(self.discog_pagination_url, limits_per_page), headers=self.headers)
                print(res.json())
            else:
                print('Entered limits per page exceeds maximum count per page(100), Printing maximum number of items');
                res = requests.get("{}per_page={}".format(self.discog_pagination_url, max_items),
                                   headers=self.headers)
                print(res.json())

        else:
            Print('Entered record is invalid, Please enter any values from list, No-[n,no,0] and Yes-[y,yes,1]')


if __name__ == '__main__':
    unittest.main()