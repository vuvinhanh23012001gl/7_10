
from folder_create import Create
from common_value import NAME_FILE_IMG_RETRAINING,NAME_FOLDER_CONFIG
import func
class OilDetectionSystem:
    folder = Create()
    
    NAME_FOLDER_INFOR_SOFTWARE = "information_product.json"
    path_folder_config = folder.get_or_create_json(NAME_FOLDER_INFOR_SOFTWARE,NAME_FOLDER_CONFIG)

    NAME_FOLDER_LOG = "log"
    NAME_FILE_LOG_PRODUCT = "log_product"
    NAME_FILE_LOG_SOFWARE = "log_software"

    PATH_FOLDER_LOG =func.create_folder_in_static(NAME_FOLDER_LOG)
    PATH_FOLDER_LOG_IMG = func.create_folder_in_static(NAME_FILE_IMG_RETRAINING)
    PATH_FOLDER_LOG_PRODUCT = folder.create_subfolder(PATH_FOLDER_LOG,NAME_FILE_LOG_PRODUCT)
    PATH_FOLDER_LOG_SOFWARE = folder.create_subfolder(PATH_FOLDER_LOG,NAME_FILE_LOG_SOFWARE)
    

    def __init__(self,
                 name="Hệ thống nhận diện điểm dầu",
                 version="v1.0",
                 author="Nhóm phần mềm công ty Brother" ):
        
        self.name = name
        self.version = version
        self.author = author
        self.path_log_img_oil = OilDetectionSystem.PATH_FOLDER_LOG_IMG
        self.path_log_product = OilDetectionSystem.PATH_FOLDER_LOG_PRODUCT
        self.path_log_software = OilDetectionSystem.PATH_FOLDER_LOG_SOFWARE

        data_config = self.read_serial_config()
        self.open_log_img_oil = data_config.get("open_log_img_oil",False)
        self.open_log_product =data_config.get("open_log_product",False)
        self.open_log_software =data_config.get("open_log_software",False)
    def set_open_log_img_oil(self, status: bool):
        self.open_log_img_oil = status
        self.wirte_data_config()
    # Set trạng thái log sản phẩm
    def set_open_log_product(self, status: bool):
        self.open_log_product = status
        self.wirte_data_config()

    # Set trạng thái log phần mềm
    def set_open_log_software(self, status: bool):
        self.open_log_software = status
        self.wirte_data_config()

    def wirte_data_config(self):
        data_update = self.to_dict()
        OilDetectionSystem.folder.write_json_to_file(OilDetectionSystem.path_folder_config,data_update)
    def read_serial_config(self):
        return OilDetectionSystem.folder.read_json_from_file(OilDetectionSystem.path_folder_config)
    
    def show_info(self):
        """Hiển thị thông tin phần mềm và trạng thái log"""
        print(f"=== THÔNG TIN PHẦN MỀM ===")
        print(f"Tên phần mềm: {self.name}")
        print(f"Phiên bản: {self.version}")
        print(f"Tác giả: {self.author}")
        print("\n=== Trạng thái log và đường dẫn ===")
        print(f"Log ảnh dầu:      {'Mở' if self.open_log_img_oil else 'Đóng'} | Path: {self.path_log_img_oil}")
        print(f"Log sản phẩm:     {'Mở' if self.open_log_product else 'Đóng'} | Path: {self.path_log_product}")
        print(f"Log phần mềm:     {'Mở' if self.open_log_software else 'Đóng'} | Path: {self.path_log_software}")
    def to_dict(self):
        """Chuyển thông tin phần mềm sang dict"""
        return {
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "path_log_img_oil": self.path_log_img_oil,
            "path_log_product": self.path_log_product,
            "path_log_software": self.path_log_software,
            "open_log_img_oil": self.open_log_img_oil,
            "open_log_product": self.open_log_product,
            "open_log_software": self.open_log_software
        }
    def update_open_btn(self,open_log_img_oil,open_log_product,open_log_software):
        """Cập nhật lại toàn bộ đường dẫn log theo cấu hình hệ thống"""
        self.open_log_img_oil = open_log_img_oil
        self.open_log_product = open_log_product
        self.open_log_software = open_log_software
        self.wirte_data_config()

    
# ==== Ví dụ sử dụng ====
# object_infor_software = OilDetectionSystem()
# object_infor_software.show_info()
# object_infor_software.set_open_log_software(True)

