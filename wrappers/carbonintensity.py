import requests

class CarbonIntensity:

    def __init__(self):
        self.base_url = 'https://api.carbonintensity.org.uk'

    def get_regions(self):
        region_name_to_id = {
            'North Scotland': 1,
            'South Scotland': 2,
            'North West England': 3,
            'North East England': 4,
            'Yorkshire': 5,
            'North Wales': 6,
            'South Wales': 7,
            'West Midlands': 8,
            'East Midlands': 9,
            'East England': 10,
            'South West England': 11,
            'South England': 12,
            'London': 13,
            'South East England': 14,
            'England': 15,
            'Scotland': 16,
            'Wales': 17
        }

        return region_name_to_id
    
    def get_carbon_intensity(self, region_id=None, from_date=None, to_date=None):
        headers = {
            'Accept': 'application/json'
        }

        url = None

        if region_id is None and from_date is None and to_date is None:
            url = self.base_url + '/regional'

        elif region_id is not None and from_date is None and to_date is None:
            url = self.base_url + '/regional/regionid/{regionid}'.format(regionid=region_id)
        
        elif from_date is not None and to_date is None and region_id is None:
            url = self.base_url + '/regional/intensity/{from_date}/fw24h'.format(from_date=from_date)

        elif to_date is None and from_date is not None and region_id is not None:
            url = self.base_url + '/regional/intensity/{from_date}/fw24h/regionid/{regionid}'.format(from_date=from_date, regionid=region_id)
            

        if url is None:
            return "Invalid parameters"

        response = requests.get(url, params={}, headers = headers)
 
        return response.json()
    


