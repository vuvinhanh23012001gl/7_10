


import common_value
import common_object
import shared_queue
import func
import threading
import time

def fuc_main_process():
    from judget_product import Judget_Product
    judget_product = Judget_Product()
    flag_the_firts_connect = True
    while True:
        if common_object.obj_manager_serial.com_is_open:   #ham nay xoa
            while (common_value.the_first_connect == True):
                common_object.obj_manager_serial.send_data("200OK:")
                common_value.status_check_connect_arm = False
                time.sleep(1)   
                if common_object.obj_manager_serial.get_rx_queue_size() > 0:
                        data = common_object.obj_manager_serial.get_data_from_queue()
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
                                  common_value.the_first_connect = False
                                  common_object.obj_manager_serial.clear_rx_queue()  
                                  common_object.obj_manager_serial.clear_tx_queue()
                                  break
                            else:
                                 common_object.obj_manager_serial.send_data("cmd:0,0,0,0")
                                 time.sleep(1)   
            print("----------------- Bắt đầu điều khiển với ARM -------------------")
            common_value.status_check_connect_arm =  True
            match common_value.click_page_html:
                case 2|6:
                    if not shared_queue.queue_rx_web_api.empty():
                        data_web_rx = shared_queue.queue_rx_web_api.get()
                        if("cmd:" in data_web_rx):
                            common_object.obj_manager_serial.clear_tx_queue()
                            common_object.obj_manager_serial.send_data(data_web_rx)
                            result_send = func.wait_for_specific_data(common_object.obj_manager_serial,data_web_rx)                   
                            if result_send:
                                shared_queue.queue_tx_web_log.put(f"\n✔️Chạy {data_web_rx} thành công")
                            else :
                                shared_queue.queue_tx_web_log.put(f"\n❌Chạy {data_web_rx} thất bại")
                    if common_value.is_data_train == 1:
                                common_value.is_data_train = 0
                                print("Có sản phẩm cần Trainging")
                                func.read_file_training('name_product_train.json',shared_queue.queue_tx_arm,common_object.obj_manager_serial,data_web_rx) # Thuc hien doc tin hieu tra ve va thuc hien
                                time.sleep(0.5)         
                case 1:
                    print("--- Đang ở trang phán định----")
                    if flag_the_firts_connect :
                        flag_the_firts_connect = False
                    if(common_value.is_run == 1): 
                        common_value.is_run = 0 
                        common_object.obj_manager_serial.clear_rx_queue()
                        common_object.obj_manager_serial.clear_tx_queue()
                        print("Bắt đầu chạy các điểm")
                        func.create_choose_master(common_value.NAME_FILE_CHOOSE_MASTER) # tạo file choose_master nếu tạo rồi thì thôi
                        choose_master_index = func.read_data_from_file(common_value.NAME_FILE_CHOOSE_MASTER) # đọc lại file choose master cũ xem lần trước  người dùng chọn gì
                        choose_master_index =  choose_master_index.strip()
                        if "0" == choose_master_index:
                                shared_queue.queue_tx_web_log.put("❌Bạn chưa chọn loại sản phẩm. Cần \"Chọn loại sản phẩm\" trước khi nhấn \"Chạy\"!")
                                shared_queue.queue_tx_web_log.put("❌Hoặc sản phẩm chưa được tạo. Cần \"Thêm sản phẩm mới\"")
                                continue
                        arr_point = common_object.manage_product.get_list_point_find_id(choose_master_index)
                        # name_product       = common_object.manage_product.get_product_name_find_id(choose_master_index)
                        # print("name product",name_product)       
                        # print("shape_master",common_object.shape_master)
                        print("arr Point",arr_point)
                        if arr_point:
                                func.run_and_capture(choose_master_index,arr_point,judget_product,common_object.shape_master,common_object.obj_manager_serial)
                        elif isinstance(arr_point,list):
                             if len(arr_point)==0:
                                 shared_queue.queue_tx_web_log.put("❌Bạn chưa lấy Master cho điểm nào. Hãy vào \"Cấu hình master->Chỉnh sửa master->Thêm master\" để cấu hình cho sản phẩm")
                        else:
                            print("Hiên tại các điểm đang bị rỗng")
                            shared_queue.queue_tx_web_log.put("❌Sản phẩm không tồn tại. Hãy \"Thêm sản phẩm mới\"->\"Chọn loại sản phẩm\"->\"Cấu hình master\"")
            time.sleep(1)
        else:

            common_value.status_check_connect_arm = False
            common_value.the_first_connect = True
            func.clear_queue(shared_queue.queue_rx_web_main)
            time.sleep(1)
            print("❌ Không tìm thấy cổng Serial. Vui lòng kiểm tra kết nối.")
       
main_process = threading.Thread(target=fuc_main_process,name="main_pc",daemon=True)
main_process.start()     
    