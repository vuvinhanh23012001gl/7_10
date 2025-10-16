
from producttypemanager import ProductTypeManager
from process_master import Proces_Shape_Master
from shared_queue import queue_tx_arm,queue_rx_arm 
from manager_serial import ManagerSerial

obj_manager_serial = ManagerSerial(queue_rx_arm=queue_rx_arm,queue_tx_arm=queue_tx_arm)
manage_product = ProductTypeManager()
shape_master = Proces_Shape_Master()
