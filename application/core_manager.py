from communication.api.dto.location_creation_request import LocationCreationRequest
from communication.mqtt.dto.telemetry_message import TelemetryMessage
from data.manager.data_manager import DataManager


class CoreManager:

    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager

    def handle_mqtt_device_telemetry_data(self, device_id, device_telemetry_data):
        """ Handle telemetry data from device """

        # Check request not None and instance of TelemetryMessage
        if device_telemetry_data is None or not isinstance(device_telemetry_data, TelemetryMessage):
            raise ValueError("Invalid TelemetryMessage")
        else:

            # If the device is registered, update the telemetry data
            if self.data_manager.get_device_by_id(device_id) is not None:
                self.data_manager.add_device_telemetry_data(device_id, device_telemetry_data)
                print(f'Telemetry data received from device {device_id}')
            else:
                raise ValueError("Device not registered")

    def get_telemetry_data_by_device_id(self, device_id):
        """
        Get telemetry data by device id from data manager
        :param device_id: Device id associated with telemetry data
        :return: List of telemetry data
        """
        return self.data_manager.get_telemetry_data_by_device_id(device_id)
