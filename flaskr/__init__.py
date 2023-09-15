import os
import sys

from flask import Flask, url_for, redirect, request, Response

from wrappers.covid import Covid
from wrappers.carbonintensity import CarbonIntensity

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    covid = Covid()
    carbon_intensity = CarbonIntensity()
    
    @app.route('/regions')
    def regions():
        covid_regions = covid.get_regions()
        carbon_intensity_regions = carbon_intensity.get_regions()

        return {
            'regions': sorted(list(set(covid_regions.keys()) | set(carbon_intensity_regions.keys())))
        }

    @app.route('/data', methods=['GET', 'POST'])
    def data():

        if request.method == 'GET':
            return {
                'covid': covid.get_new_cases(),
                'carbon_intensity': carbon_intensity.get_carbon_intensity().get('data')
            }

        if request.method == 'POST':
            region = request.form.get('region')
            from_date = request.form.get('from')
            to_date = request.form.get('to')
            
            if not (region or from_date or to_date):
                return "Invalid parameters", 400, {'Content-Type': 'application/json'}

            covid_regions = covid.get_regions()

            if region in covid_regions:
                region_id = covid_regions.get(region)
                covid_data = covid.get_new_cases(from_date, region_id)
            
            carbon_intensity_regions = carbon_intensity.get_regions()

            if region in carbon_intensity_regions:
                region_id = carbon_intensity_regions.get(region)
                carbon_intensity_data = carbon_intensity.get_carbon_intensity(region_id, from_date, to_date)

            return {
                'covid': covid_data,
                'carbon_intensity': carbon_intensity_data
            }, 200, {'Content-Type': 'application/json'}      

    return app