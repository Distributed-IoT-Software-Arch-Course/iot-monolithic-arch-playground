from flask import Flask, request, render_template
import os
import yaml
import threading

from data.manager.data_manager import DataManager


class WebServer:

    def __init__(self, config_file:str, data_manager: DataManager):

        # Server Thread
        self.server_thread = None

        # Save the data manager
        self.data_manager = data_manager

        # Save the configuration file
        self.config_file = config_file

        # Get the main communication directory
        main_app_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Construct the file path
        template_dir = os.path.join(main_app_path, 'presentation')

        # Set a default configuration
        self.configuration_dict = {
            "web": {
                "host": "0.0.0.0",
                "port": 7071
            }
        }

        # Read Configuration from target Configuration File Path
        self.read_configuration_file()

        # Create the Flask app
        self.app = Flask(__name__, template_folder=template_dir)

        # Add URL rules to the Flask app mapping the URL to the function
        self.app.add_url_rule('/locations', 'locations', self.locations)
        self.app.add_url_rule('/location/<string:location_id>/devices', 'devices', self.devices)
        self.app.add_url_rule('/location/<string:location_id>/device/<string:device_id>/telemetry', 'telemetry', self.telemetry)

    def read_configuration_file(self):
        """ Read Configuration File for the Web Server
         :return:
        """

        # Get the main communication directory
        main_app_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Construct the file path
        file_path = os.path.join(main_app_path, self.config_file)

        with open(file_path, 'r') as file:
            self.configuration_dict = yaml.safe_load(file)

        print("Read Configuration from file ({}): {}".format(self.config_file, self.configuration_dict))

    def locations(self):
        """ Get all locations and render the locations.html template"""
        location_list = self.data_manager.get_all_locations()
        return render_template('locations.html', locations=location_list)

    def devices(self, location_id):
        """ Get all devices for a specific location and render the devices.html template"""
        device_list = self.data_manager.get_devices_by_location(location_id)
        return render_template('devices.html', devices=device_list, location_id=location_id)

    def telemetry(self, location_id, device_id):
        """ Get telemetry data for a specific device and render the telemetry.html template"""
        telemetry_data = self.data_manager.get_telemetry_data_by_device_id(device_id)
        return render_template('telemetry.html', telemetry_data=telemetry_data, location_id=location_id, device_id=device_id)

    def run_server(self):
        """ Run the Flask Web Server"""
        self.app.run(host=self.configuration_dict['web']['host'], port=self.configuration_dict['web']['port'])

    def start(self):
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.start()

    def stop(self):
        """ Stop the REST API Server (Flask Method)
        In this code, request.environ.get('werkzeug.server.shutdown')
        retrieves the shutdown function from the environment.
        If the function is not found, it raises a RuntimeError,
        indicating that the server is not running with Werkzeug.
        If the function is found, it is called to shut down the server."""

        # Shutdown the server
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')

        # Call the shutdown function
        func()

        # Wait for the server thread to join
        self.server_thread.join()