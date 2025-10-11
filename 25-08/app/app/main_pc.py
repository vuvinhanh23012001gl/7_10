

from manager_serial import ManagerSerial
from producttypemanager import ProductTypeManager
from process_master import Proces_Shape_Master
from common_value import NAME_FILE_CHOOSE_MASTER
from shared_queue import queue_rx_web_api,queue_rx_web_main,queue_tx_web_log,queue_tx_arm,queue_rx_arm
import func
import threading
import time

 
#---lock doi tuong-----
manage_product_type = ProductTypeManager()
object_shape_master = Proces_Shape_Master()

click_page_html = threading.Lock()              
click_page_html = 0

the_first_connect = True    
is_data_train = 0
is_run = 0
status_check_connect_arm =  0
mumber_total_product = 0
mumber_product_oke = 0

obj_manager_serial = ManagerSerial(queue_rx_arm=queue_rx_arm,queue_tx_arm=queue_tx_arm) 
def fuc_main_process():
    from judget_product import Judget_Product
    judget_product = Judget_Product()
    global status_check_connect_arm
    global is_data_train 
    global click_page_html
    global is_run
    global the_first_connect
    flag_the_firts_connect = True
    while True:
        if obj_manager_serial.com_is_open:   #ham nay xoa
            while (the_first_connect == True):
                obj_manager_serial.send_data("200OK:")
                status_check_connect_arm = 0
                time.sleep(1)   
                if obj_manager_serial.get_rx_queue_size() > 0:
                        data = obj_manager_serial.get_data_from_queue()
                        print("Data nhận được từ Queue ARM:", data)
                        if("200OK," in data ):
                            if(len(data) <= 6):
                                print("❌Độ dài dữ liệu gửi về ngắn....PC Gửi lại 200OK") 
                                continue
                            cut_data = data[6:].split(",")
                            print("Mảng ",cut_data)
                            if cut_data == data[6:]:
                                print("❌Dữ liệu không có dấu phẩy....PC Gửi lại 200OK")
                                continue
                            if (func.is_all_int_strings(cut_data) == False or len(cut_data) != 4):
                                print("Dữ liệu tọa độ ban đầu không hợp lệ. Vui lòng kiểm tra lại.")
                                continue
                            if "200OK,000,000,000" in data:
                                  print("........Nhan dung tin hieu dieu khien .....")
                                  the_first_connect = False
                                  obj_manager_serial.clear_rx_queue()  
                                  obj_manager_serial.clear_tx_queue()
                                  break
                            else:
                                 obj_manager_serial.send_data("cmd:0,0,0,0")
                                 time.sleep(1)   
            print("----------------- Bắt đầu điều khiển với ARM -------------------")
            
            # click_page_html  ==  2 vao che do trainning san pham
            # click_page_html  ==  1 Vào Chế độ main  show
            status_check_connect_arm = 1
            match click_page_html:
                case 2|6:
                    if not queue_rx_web_api.empty():
                        data_web_rx = queue_rx_web_api.get()
                        if("cmd:" in data_web_rx):
                            obj_manager_serial.clear_tx_queue()
                            obj_manager_serial.send_data(data_web_rx)
                            result_send = func.wait_for_specific_data(obj_manager_serial,data_web_rx)                   
                            if result_send:
                                queue_tx_web_log.put(f"\n✔️Chạy {data_web_rx} thành công")
                            else :
                                queue_tx_web_log.put(f"\n❌Chạy {data_web_rx} thất bại")
                    if is_data_train == 1:
                                is_data_train = 0
                                print("Có sản phẩm cần Trainging")
                                func.read_file_training('name_product_train.json',queue_tx_arm,obj_manager_serial,data_web_rx) # Thuc hien doc tin hieu tra ve va thuc hien
                                time.sleep(0.5)
                              
                case 1:
         
                    print("Đang Xử Lý Trang Main")
                    if flag_the_firts_connect :
                        flag_the_firts_connect = False
                    
                    # else:
                    #     #  print("Cam đã kết nối")
                    if(is_run == 1): 
                        is_run = 0  #tat de khong vao lai
                        obj_manager_serial.clear_rx_queue()
                        obj_manager_serial.clear_tx_queue()
                        print("Bắt đầu chạy các điểm")
                        func.create_choose_master(NAME_FILE_CHOOSE_MASTER) # tạo file choose_master nếu tạo rồi thì thôi
                        choose_master_index = func.read_data_from_file(NAME_FILE_CHOOSE_MASTER) # đọc lại file choose master cũ xem lần trước  người dùng chọn gì
                        choose_master_index =  choose_master_index.strip()
                        print("Chạy với ID là :",)
                        arr_point = manage_product_type.get_list_point_find_id(choose_master_index)
                        # name_product       = manage_product_type.get_product_name_find_id(choose_master_index)
                        # print("name product",name_product)    
                        # shape_master =  object_shape_master.get_data_is_id(choose_master_index)        
                        # print("shape_master",shape_master)
                        print("arr Point",arr_point)
                        if arr_point is not None:
                                func.run_and_capture(choose_master_index,arr_point,judget_product,object_shape_master,obj_manager_serial)

                        else:
                                print("Không tìm thấy ID danh sách điểm để chạy")
                                
                                
      

               

                    time.sleep(0.5)         
            time.sleep(1)
         
        else:
            the_first_connect = True
            func.clear_queue(queue_rx_web_main)
            print("❌ Không tìm thấy cổng Serial. Vui lòng kiểm tra kết nối.")
            time.sleep(1)
       
main_process = threading.Thread(target=fuc_main_process,daemon=True)
main_process.start()     
    