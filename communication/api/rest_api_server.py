from flask import Flask, request
from flask_restful import Api
from communication.api.resources.device_resource import DeviceResource
from communication.api.resources.devices_resource import DevicesResource
from communication.api.resources.locations_resource import LocationsResource
from communication.api.resources.location_resource import LocationResource
import threading
import yaml
import os

class RestApiServer:

    # Default Endpoint Prefix
    DEFAULT_ENDPOINT_PREFIX = "/api/iot/inventory"

    def __init__(self, config_file, data_manager):

        # Initialize REST API Server and Flask Application to None
        # They will be initialized in the init_rest_api method
        self.api = None
        self.app = None

        # Server Thread
        self.server_thread = None

        # Configuration File Path
        self.config_file = config_file

        # Data Manager
        self.data_manager = data_manager

        # Set a default configuration
        self.configuration_dict = {
            "rest":{
                "api_prefix": self.DEFAULT_ENDPOINT_PREFIX,
                "host": "0.0.0.0",
                "port": 7070
            }
        }

        # Read Configuration from target Configuration File Path
        self.read_configuration_file()

        # Initialize REST API
        self.init_rest_api()

    def read_configuration_file(self):
        """ Read Configuration File for the REST API Server
         :return:
        """

        # Get the main communication directory
        main_app_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Construct the file path
        file_path = os.path.join(main_app_path, self.config_file)

        with open(file_path, 'r') as file:
            self.configuration_dict = yaml.safe_load(file)

        print("Read Configuration from file ({}): {}".format(self.config_file, self.configuration_dict))

    def init_rest_api(self):
        """ Initialize REST API with resources and endpoints
        :return:
        """

        # Create a new Flask Application and the REST API from Flask Restful
        self.app = Flask(__name__)
        self.api = Api(self.app)

        # Add Resources and Endpoints
        self.api.add_resource(LocationsResource, self.configuration_dict['rest']['api_prefix'] + '/location',
                         resource_class_kwargs={'data_manager': self.data_manager},
                         endpoint="locations",
                         methods=['GET', 'POST'])

        self.api.add_resource(LocationResource, self.configuration_dict['rest']['api_prefix'] + '/location/<string:location_id>',
                         resource_class_kwargs={'data_manager': self.data_manager},
                         endpoint='location',
                         methods=['GET', 'PUT', 'DELETE'])

        self.api.add_resource(DevicesResource,
                         self.configuration_dict['rest']['api_prefix'] + '/location/<string:location_id>/device',
                         resource_class_kwargs={'data_manager': self.data_manager},
                         endpoint="devices",
                         methods=['GET', 'POST'])

        self.api.add_resource(DeviceResource, self.configuration_dict['rest'][
            'api_prefix'] + '/location/<string:location_id>/device/<string:device_id>',
                         resource_class_kwargs={'data_manager': self.data_manager},
                         endpoint='device',
                         methods=['GET', 'PUT', 'DELETE'])

    def run_server(self):
        """ Start the REST API Server """
        self.app.run(host=self.configuration_dict['rest']['host'], port=self.configuration_dict['rest']['port'])

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