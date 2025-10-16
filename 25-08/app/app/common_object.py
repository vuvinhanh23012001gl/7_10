
from producttypemanager import ProductTypeManager
from process_master import Proces_Shape_Master
from shared_queue import queue_tx_arm,queue_rx_arm 
from manager_serial import ManagerSerial
from folder_create import Create
from log import Log
from common_value import NAME_FOLDER_LOG

folder =  Create()
NAME_FILE_LOG = "log_data.txt"
NAME_CLASS_LOG = "app"
file_path = folder.create_file_in_folder_two(NAME_FILE_LOG,NAME_FOLDER_LOG) 
obj_log = Log(NAME_CLASS_LOG,NAME_FILE_LOG)
obj_log.enable_console()

obj_manager_serial = ManagerSerial(queue_rx_arm=queue_rx_arm,queue_tx_arm=queue_tx_arm)
manage_product = ProductTypeManager()
shape_master = Proces_Shape_Master()
