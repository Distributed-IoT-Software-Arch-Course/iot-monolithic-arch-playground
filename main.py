from data.data_manager import DataManager
from application.api.rest_api_server import RestApiServer
from application.web.web_server import WebServer

API_CONFIG_FILE = "config/api_conf.yaml"
WEB_CONFIG_FILE = "config/web_conf.yaml"

if __name__ == '__main__':

    # Data Manager
    data_manager = DataManager()

    # Init some demo data on the Data Manager
    data_manager.init_demo_data()

    # Create RESTful API Server
    rest_api_server = RestApiServer(API_CONFIG_FILE, data_manager)

    # Run RESTful API Server
    rest_api_server.start()

    # Create Web Server
    web_server = WebServer(WEB_CONFIG_FILE, data_manager)

    # Run Web Server
    web_server.start()