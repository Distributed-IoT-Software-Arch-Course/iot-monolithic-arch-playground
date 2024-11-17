from logic.model.device_model import DeviceModel
from logic.model.location_model import LocationModel


class DataManager:

    location_dictionary = {}

    def init_demo_data(self):
        """Initialize the DataManager with some demo data"""

        # Demo Location
        demo_location = LocationModel("l0001",
                                      "TestBuilding",
                                      48.312321,
                                      10.433423211)

        # Add New Location
        self.add_location(demo_location)

        # Demo Device for the previous location
        demo_device = DeviceModel("d0001",
                                  "demo-device",
                                  demo_location.uuid,
                                  DeviceModel.DEVICE_TYPE_DEFAULT,
                                  "ACME Inc",
                                  "0.0.1beta",
                                  48.312321,
                                  10.433423211)

        # Add New Device
        self.add_device(demo_location.uuid, demo_device)

    # LOCATION MANAGEMENT
    def add_location(self, new_location):

        # Check the correct instance for the variable new_location
        if isinstance(new_location, LocationModel):
            self.location_dictionary[new_location.uuid] = new_location
        else:
            raise TypeError("Error adding new Location ! Only LocationModel are allowed !")

    def update_location(self, updated_location):

        # Check the correct instance for the variable updated_location
        if isinstance(updated_location, LocationModel):
            self.location_dictionary[updated_location.uuid] = updated_location
        else:
            raise TypeError("Error updating the Location ! Only LocationModel are allowed !")

    def remove_location(self, location_uuid):
        if location_uuid in self.location_dictionary.keys():
            del self.location_dictionary[location_uuid]

    # DEVICE MANAGEMENT

    def add_device(self, location_id, new_device):

        # Check the correct instance for the variable new_device
        if isinstance(new_device, DeviceModel):
            # Check if the required Location Id is correct
            if location_id in self.location_dictionary:
                self.location_dictionary[location_id].device_dictionary[new_device.uuid] = new_device
            else:
                raise IndexError("Error Location Id is not correct !")
        else:
            raise TypeError("Error adding new device ! Only DeviceModel are allowed !")

    def update_device(self, location_id, updated_device):
        # Check the correct instance for the variable new_device
        if isinstance(updated_device, DeviceModel):
            # Check if the required Location Id is correct
            if location_id in self.location_dictionary:
                self.location_dictionary[location_id].device_dictionary[updated_device.uuid] = updated_device
            else:
                raise IndexError("Error Location Id is not correct !")
        else:
            raise TypeError("Error adding new device ! Only DeviceModel are allowed !")

    def remove_device(self, location_id, device_uuid):

        # Check if the required Location Id is correct
        if location_id in self.location_dictionary:
            # Retrieve the target location object
            target_location = self.location_dictionary[location_id]

            if device_uuid in target_location.device_dictionary.keys():
                del target_location.device_dictionary[device_uuid]
        else:
            raise IndexError("Error Location Id is not correct !")

    def get_all_locations(self):
        """Return a list of all locations"""
        return self.location_dictionary.values()

    def get_devices_by_location(self, location_id):
        """Return a list of all devices for a given location"""
        if location_id in self.location_dictionary:
            return list(self.location_dictionary[location_id].device_dictionary.values())
        else:
            raise IndexError("Error Location Id is not correct !")