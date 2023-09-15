import requests

class Covid:

    def __init__(self):
        self.base_url = 'https://api.coronavirus.data.gov.uk/generic'

    def get_regions(self):
        url = self.base_url + '/area/region'
        headers = {
            'Accept': 'application/json'
        }
        response = requests.get(url, params={}, headers = headers)

        regions = dict()
        for data in response.json():
            regions[data['areaName']] = data['areaCode']

        return regions
    
    def get_new_cases(self, date=None, region_id=None):

        if region_id is None:
            default_id = "E02004402"
            url = self.base_url + '/soa/msoa/{region_id}/newCasesBySpecimenDate'.format(region_id=default_id)
        else:
            url = self.base_url + '/soa/msoa/{region_id}/newCasesBySpecimenDate'.format(region_id=region_id)

        params = {}
        if date is not None:
            params = {
                'date': date
            }

        headers = {
            'Accept': 'application/json'
        }
        response = requests.get(url, params=params, headers = headers)

        if response.status_code == 204:
            return "No data found for this date and region"

        return response.json()