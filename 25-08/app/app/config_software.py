
from folder_create import Create
from common_value import NAME_FILE_IMG_RETRAINING,NAME_FOLDER_CONFIG
import func
class OilDetectionSystem:
    SET_TIME_SAVE_LOG_IMG = 30
    SET_TIME_SAVE_LOG_SOFTWARE = 30
    SET_TIME_SAVE_LOG_EXCELL =  30
    
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
                 author="Nhóm phần mềm RD-PE công ty Brother" ):
        
        self.name = name
        self.version = version
        self.author = author
        self.path_log_img_oil = OilDetectionSystem.PATH_FOLDER_LOG_IMG
        self.path_log_product = OilDetectionSystem.PATH_FOLDER_LOG_PRODUCT
        self.path_log_software = OilDetectionSystem.PATH_FOLDER_LOG_SOFWARE

        data_config = self.read_serial_config()
        name_data_in_file = data_config.get("name",None)
        version_data_in_file = data_config.get("version",None)
        author_data_in_file  = data_config.get("author",None)
        
        self.time_save_log_img = data_config.get("set_time_save_log_img",OilDetectionSystem.SET_TIME_SAVE_LOG_IMG)
        self.time_save_log_software = data_config.get("set_time_save_log_software",OilDetectionSystem.SET_TIME_SAVE_LOG_SOFTWARE)
        self.time_save_log_excell = data_config.get("set_time_save_log_excell",OilDetectionSystem.SET_TIME_SAVE_LOG_EXCELL)
  
        if all([name_data_in_file,version_data_in_file,author_data_in_file]):
            self.name = name_data_in_file
            self.version = version_data_in_file
            self.author = author_data_in_file
        self.open_log_img_oil = data_config.get("open_log_img_oil",False)
        self.open_log_product =data_config.get("open_log_product",False)
        self.open_log_software =data_config.get("open_log_software",False)
    def get_path_log_img_oil(self):   
        return self.path_log_img_oil     

    def get_path_log_product(self): #log excell
        return self.path_log_product

    def get_path_log_software(self):
          return self.path_log_software
    def get_log_img_oil(self):
        return self.open_log_img_oil

    def get_log_product(self):  #log excell
        return self.open_log_product

    def get_log_software(self):
        return self.open_log_software
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
        
        print(f"Thời gian lưu log hình ảnh {self.time_save_log_img}")
        print(f"Thời gian lưu log software {self.time_save_log_software}")
        print(f"Thời gian lưu log File excell {self.time_save_log_excell}")
        
    def to_dict_btn_status(self):
        """Chuyển thông tin phần mềm sang dict"""
        return {
            "open_log_img_oil": self.open_log_img_oil,
            "open_log_product": self.open_log_product,
            "open_log_software": self.open_log_software,
            
            "set_time_save_log_img":self.time_save_log_img,
            "set_time_save_log_software":self.time_save_log_software,
            "set_time_save_log_file_excell":self.time_save_log_excell,
        }
    def to_dict_infor_software(self):
        """Chuyển thông tin phần mềm sang dict"""
        return {
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "path_log_img_oil": self.path_log_img_oil,
            "path_log_product": self.path_log_product,
            "path_log_software": self.path_log_software
        }
    def update_open_btn(self,open_log_img_oil,open_log_product,open_log_software,time_save_software=None,time_save_img=None,time_save_excell=None):
        """Cập nhật lại toàn bộ đường dẫn log theo cấu hình hệ thống"""
        self.open_log_img_oil = open_log_img_oil
        self.open_log_product = open_log_product
        self.open_log_software = open_log_software
    
        if all(isinstance(v, (int, float)) and v >= 0 for v in [time_save_software, time_save_img, time_save_excell]):
            self.time_save_log_software = time_save_software
            self.time_save_log_img = time_save_img
            self.time_save_log_excell = time_save_excell
            self.wirte_data_config()
        else:
            print("❌ Một hoặc nhiều giá trị thời gian không hợp lệ (phải >= 0).")

            
        self.wirte_data_config()
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
            "open_log_software": self.open_log_software,
            "set_time_save_log_software": self.time_save_log_software,
            "set_time_save_log_img":self.time_save_log_img,
            "set_time_save_log_excell":self.time_save_log_excell,
        }
    def SetTimeSaveLogSoftware(self, days_software: int):
        """Cập nhật thời gian lưu log phần mềm (đơn vị: ngày)"""
        if isinstance(days_software, int) and days_software > 0:
            self.time_save_log_software = days_software
            self.wirte_data_config()
            print(f"✅ Cập nhật thời gian lưu log phần mềm: {days_software} ngày")
        else:
            print("❌ Giá trị không hợp lệ. Vui lòng nhập số nguyên dương.")

    def SetTimeSaveLogImg(self, days_img: int):
        """Cập nhật thời gian lưu log hình ảnh (đơn vị: ngày)"""
        if isinstance(days_img, int) and days_img > 0:
            self.time_save_log_img = days_img
            self.wirte_data_config()
            print(f"✅ Cập nhật thời gian lưu log hình ảnh: {days_img} ngày")
        else:
            print("❌ Giá trị không hợp lệ. Vui lòng nhập số nguyên dương.")

    def SetTimeSaveLogExcell(self, days_excel: int):
        """Cập nhật thời gian lưu log file Excel (đơn vị: ngày)"""
        if isinstance(days_excel, int) and days_excel > 0:
            self.time_save_log_excell = days_excel
            self.wirte_data_config()
            print(f"✅ Cập nhật thời gian lưu log Excel: {days_excel} ngày")
        else:
            print("❌ Giá trị không hợp lệ. Vui lòng nhập số nguyên dương.")

    def SetTimeSaveAllLog(self, days_software: int, days_img: int, days_excel: int):
        """Cập nhật đồng thời 3 loại thời gian lưu log"""
        if all(isinstance(x, int) and x > 0 for x in [days_software, days_img, days_excel]):
            self.time_save_log_software = days_software
            self.time_save_log_img = days_img
            self.time_save_log_excell = days_excel
            self.wirte_data_config()
            print("✅ Đã cập nhật toàn bộ thời gian lưu log:")
            print(f"   • Phần mềm : {days_software} ngày")
            print(f"   • Hình ảnh : {days_img} ngày")
            print(f"   • File Excel: {days_excel} ngày")
        else:
            print("❌ Tất cả giá trị phải là số nguyên dương.")
    def GetTimeSaveLogSoftware(self) -> int:
        """Lấy thời gian lưu log phần mềm (đơn vị: ngày)"""
        print(f"📄 Thời gian lưu log phần mềm hiện tại: {self.time_save_log_software} ngày")
        return self.time_save_log_software

    def GetTimeSaveLogImg(self) -> int:
        """Lấy thời gian lưu log hình ảnh (đơn vị: ngày)"""
        return self.time_save_log_img

    def GetTimeSaveLogExcell(self) -> int:
        """Lấy thời gian lưu log file Excel (đơn vị: ngày)"""
        print(f"📄 Thời gian lưu log Excel hiện tại: {self.time_save_log_excell} ngày")
        return self.time_save_log_excell

    def GetTimeSaveAllLog (self) -> dict:
        """Lấy đồng thời toàn bộ thời gian lưu log"""
        info_log_time = {
            "software": self.time_save_log_software,
            "image": self.time_save_log_img,
            "excel": self.time_save_log_excell
        }
        print("📄 Thông tin toàn bộ thời gian lưu log hiện tại:")
        print(f"   • Phần mềm : {info_log_time['software']} ngày")
        print(f"   • Hình ảnh : {info_log_time['image']} ngày")
        print(f"   • File Excel: {info_log_time['excel']} ngày")
        return info_log_time
    
# ==== Ví dụ sử dụng ====
# object_infor_software = OilDetectionSystem()
# object_infor_software.show_info()

# #kiem tra update oke chua 
# object_infor_software.update_open_btn(True,True,True,50,50,50)

# object_infor_software.show_info()
# object_infor_software.set_open_log_software(True)



