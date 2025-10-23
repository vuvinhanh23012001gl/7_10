
from producttypemanager import ProductTypeManager
from process_master import Proces_Shape_Master
from shared_queue import queue_tx_arm,queue_rx_arm,queue_accept_capture
from manager_serial import ManagerSerial
from folder_create import Create
import log
from config_software import OilDetectionSystem
from user import Manage_User
from flask_socketio import SocketIO
from flask import Flask
from connect_camera import BaslerCamera

obj_manage_user = Manage_User()
obj_config_software = OilDetectionSystem()
obj_log = log.Log(obj_config_software)
obj_log_img = log.log_img(obj_config_software)
# obj_log_excell  = log_excell(obj_config_software)


folder =  Create()
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
cam_basler = BaslerCamera(queue_accept_capture,socketio,config_file="Camera_25129678.pfs")
obj_manager_serial = ManagerSerial(queue_rx_arm=queue_rx_arm,queue_tx_arm=queue_tx_arm)
manage_product = ProductTypeManager()
shape_master = Proces_Shape_Master()








