import logging
import threading
import os

class Log:
    def __init__(self, name=__name__, log_file="app.log"):
        self.name = name
        self.log_file = log_file
        self.console_enabled = False
        self.file_enabled = False
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # Cho phép tất cả mức log
        self.formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(threadName)s] (%(name)s:%(lineno)d): %(message)s"
        )

        # Dùng Lock để đảm bảo việc thêm/bỏ handler thread-safe
        self._lock = threading.Lock()

    # ===============================
    # Cấu hình
    # ===============================
    def log_and_print(self, msg, value=None, level="info"):
        # Ghép message nếu có value
        full_msg = f"{msg}: {value}" if value is not None else msg
        if level == "debug":
            self.logger.debug(full_msg)
        elif level == "warning":
            self.logger.warning(full_msg)
        elif level == "error":
            self.logger.error(full_msg)
        elif level == "critical":
            self.logger.critical(full_msg)
        else:
            self.logger.info(full_msg)
            
    def enable_console(self):
        with self._lock:
            if not self.console_enabled:
                ch = logging.StreamHandler()
                ch.setLevel(logging.DEBUG)
                ch.setFormatter(self.formatter)
                self.logger.addHandler(ch)
                self.console_enabled = True

    def disable_console(self):
        with self._lock:
            for h in list(self.logger.handlers):
                if isinstance(h, logging.StreamHandler):
                    self.logger.removeHandler(h)
            self.console_enabled = False

    def enable_file(self):
        with self._lock:
            if not self.file_enabled:
                os.makedirs(os.path.dirname(self.log_file) or ".", exist_ok=True)
                fh = logging.FileHandler(self.log_file, encoding="utf-8")
                fh.setLevel(logging.DEBUG)
                fh.setFormatter(self.formatter)
                self.logger.addHandler(fh)
                self.file_enabled = True

    def disable_file(self):
        with self._lock:
            for h in list(self.logger.handlers):
                if isinstance(h, logging.FileHandler):
                    self.logger.removeHandler(h)
            self.file_enabled = False

    # ===============================
    # Các hàm log tiện dụng
    # ===============================
    def debug(self, msg):
        self.logger.debug(msg)
        

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

# import time
# logger = Log(__name__)
# logger.enable_console()
# logger.enable_file()
# def worker(n):
#     for i in range(3):
#         logger.info(f"Luồng {n}: chạy lần {i}")
#         time.sleep(0.3)

# threads = []
# for i in range(3):
#     t = threading.Thread(target=worker, args=(i+1,), name=f"Thread-{i+1}")
#     threads.append(t)
#     t.start()

# for t in threads:
#     t.join()
# class log_excell:
#     def __init__(self,path_save_log_excell):
#         self.data = None
#         self.path_save = path_save_log_excell
#     def 

from config_software import OilDetectionSystem
obj_infor_config = OilDetectionSystem()
from openpyxl import load_workbook
class log_excell:
    from folder_create import Create
    obj_folder = Create()

    def __init__(self,obj_config_software:OilDetectionSystem):
        self.wb = None
        self.ws = None
        #obj_config_software chi duoc doc thoi khong duoc cau hinh log
        self.obj_config_software = obj_config_software

        self.path_file_save_log_excell = self.create_file_excell()  #self.path_file_save_log_excell  se cho co the bang none neu khong duoc phep tao file
        if self.path_file_save_log_excell:
            self.write_file_excel(["Thời gian","Mã sản phẩm","Tên sản phẩm","Tên người thao tác","Trạng thái nhận diện"])

    def get_path_file_save_log_excell(self):
        """Tra ve path File luu log hien tai"""
        return self.path_file_save_log_excell
    def get_time(self):
        """Lấy thời gian cho phép log được lưu nếu được bật"""
        return self.obj_config_software.GetTimeSaveLogExcell()

    def get_open_log_excell(self):
        """lấy quyền lưu log"""
        return self.obj_config_software.get_log_product()

    def get_path_save_log_excell(self):
        return self.obj_config_software.get_path_log_product()
    

    def get_list_file_in_folder_log_excell(self)->list:
        """Hàm này trả về danh sách file hiện có trong folder excell"""
        return log_excell.obj_folder.get_list_file_in_folder(self.get_path_save_log_excell())
    
    def create_file_excell(self):
        """name_file la duong dan toi file"""
        self.delete_file_old()
        if self.get_open_log_excell():
            file_path = log_excell.obj_folder.create_file_excell_in_folder_log(self.get_path_save_log_excell())
            return file_path
        else:
            print("Không tạo File Log sản phẩm vì không bật log")
            return None
    
    def get_list_find_old(self,days_threshold):
        """Trả về đường danh sách tên file có days_threshold không thỏa mãn để xóa """
        list_file = self.get_list_file_in_folder_log_excell()
        print("Danh sach file excell hiện có trong thư mục là:",list_file)
        if  list_file:
            arr_old_file  = log_excell.obj_folder.get_old_files_by_threshold(list_file,days_threshold)
            print(f"Danh sách file cũ hơn {days_threshold} ngày để xóa",arr_old_file)
            return arr_old_file
        else :
            print("Danh sách trong folder excell rỗng")
            return None
    def delete_file_old(self):
        arr_file_old = self.get_list_find_old(self.get_time())
        if arr_file_old:
            print("---Xóa File quá hạn \n Bắt đầu xóa --")
            for file_delete in arr_file_old:
                path_file_delete = log_excell.obj_folder.find_file(self.get_path_save_log_excell(),file_delete)
                print(path_file_delete)
                if path_file_delete:
                    log_excell.obj_folder.delete_file(path_file_delete)
            print("--Xóa thành công file--")

    def write_file_excel(self, row: list):
        """
        Ghi 1 dòng dữ liệu vào file Excel hiện tại.
        Nếu file chưa tồn tại -> tạo mới.
        :param row: list chứa dữ liệu tương ứng 1 dòng
        """
        if not self.get_open_log_excell():
            print("⚠️ Chức năng log chưa được bật, không lưu Excel")
            return None

        file_path = self.get_path_file_save_log_excell()
        if os.path.exists(file_path):
            self.wb = load_workbook(file_path)
            self.ws = self.wb.active
        self.ws.append(row)
        self.wb.save(file_path)
        print(f"✅ Đã lưu dòng dữ liệu vào: {file_path}")
        return file_path
    





        
        


# test_obj_log_excell = log_excell(obj_infor_config)
# test_obj_log_excell.write_file_excel([1,3,4,5])
# # test_obj_log_excell.delete_file_old()
# # test_obj_log_excell.create_file_excell()
# # test_obj_log_excell.get_list_find_old(1)

        