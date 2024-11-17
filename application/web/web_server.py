from flask import Flask, render_template
from data.data_manager import DataManager
import os

# Get the main application directory
main_app_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Construct the file path
template_dir = os.path.join(main_app_path, 'presentation')

# Create the Flask app
app = Flask(__name__, template_folder=template_dir)

# Initialize DataManager
data_manager = DataManager()
data_manager.init_demo_data()

@app.route('/locations')
def locations():
    location_list = data_manager.get_all_locations()
    return render_template('locations.html', locations=location_list)

@app.route('/location/<string:location_id>/devices')
def devices(location_id):
    device_list = data_manager.get_devices_by_location(location_id)
    return render_template('devices.html', devices=device_list, location_id=location_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7071)