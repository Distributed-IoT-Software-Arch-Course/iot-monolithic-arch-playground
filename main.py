from data.data_manager import DataManager
from logic.model.location_model import LocationModel
from logic.model.device_model import DeviceModel
from application.api.rest_api_server import RestApiServer

API_CONFIG_FILE = "config/api_conf.yaml"

if __name__ == '__main__':

    # Data Manager
    data_manager = DataManager()

    # Init some demo data on the Data Manager


    # Create RESTful API Server
    rest_api_server = RestApiServer(API_CONFIG_FILE, data_manager)

    # Run RESTful API Server
    rest_api_server.start()