
from producttypemanager import ProductTypeManager
from process_master import Proces_Shape_Master
from shared_queue import queue_tx_arm,queue_rx_arm
from manager_serial import ManagerSerial
from folder_create import Create
import log
from config_software import OilDetectionSystem
from user import Manage_User

obj_manager_serial = ManagerSerial(queue_rx_arm=queue_rx_arm,queue_tx_arm=queue_tx_arm)
manage_product = ProductTypeManager()
shape_master = Proces_Shape_Master()
folder =  Create()
obj_manage_user = Manage_User()
obj_config_software = OilDetectionSystem()

obj_log = log.Log(obj_config_software)
# obj_log_excell  = log_excell(obj_config_software)
obj_log_img = log.log_img(obj_config_software)



