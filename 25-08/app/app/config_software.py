from folder_create import Create
from common_value import NAME_FILE_IMG_RETRAINING, NAME_FOLDER_CONFIG
import func


class OilDetectionSystem:
    SET_TIME_SAVE_LOG_IMG = 30
    SET_TIME_SAVE_LOG_SOFTWARE = 30
    SET_TIME_SAVE_LOG_EXCELL = 30

    folder = Create()
    NAME_FOLDER_INFOR_SOFTWARE = "information_product.json"
    path_folder_config = folder.get_or_create_json(NAME_FOLDER_INFOR_SOFTWARE, NAME_FOLDER_CONFIG)

    NAME_FOLDER_LOG = "log"
    NAME_FILE_LOG_PRODUCT = "log_product"
    NAME_FILE_LOG_SOFWARE = "log_software"

    PATH_FOLDER_LOG = func.create_folder_in_static(NAME_FOLDER_LOG)
    PATH_FOLDER_LOG_IMG = func.create_folder_in_static(NAME_FILE_IMG_RETRAINING)
    PATH_FOLDER_LOG_PRODUCT = folder.create_subfolder(PATH_FOLDER_LOG, NAME_FILE_LOG_PRODUCT)
    PATH_FOLDER_LOG_SOFWARE = folder.create_subfolder(PATH_FOLDER_LOG, NAME_FILE_LOG_SOFWARE)

    def __init__(self,
                 name="Hệ thống nhận diện điểm dầu",
                 version="v1.0",
                 author="Nhóm phần mềm RD-PE công ty Brother"):

        self.name = name
        self.version = version
        self.author = author

        self.path_log_img_oil = OilDetectionSystem.PATH_FOLDER_LOG_IMG
        self.path_log_product = OilDetectionSystem.PATH_FOLDER_LOG_PRODUCT
        self.path_log_software = OilDetectionSystem.PATH_FOLDER_LOG_SOFWARE

        data_config = self.read_serial_config()

        # Đọc thông tin phần mềm
        self.name = data_config.get("name", self.name)
        self.version = data_config.get("version", self.version)
        self.author = data_config.get("author", self.author)

        # Đọc cấu hình log
        self.time_save_log_img = data_config.get("set_time_save_log_img", OilDetectionSystem.SET_TIME_SAVE_LOG_IMG)
        self.time_save_log_software = data_config.get("set_time_save_log_software", OilDetectionSystem.SET_TIME_SAVE_LOG_SOFTWARE)
        self.time_save_log_excell = data_config.get("set_time_save_log_excell", OilDetectionSystem.SET_TIME_SAVE_LOG_EXCELL)

        # Trạng thái log
        self.open_log_img_oil = data_config.get("open_log_img_oil", False)
        self.open_log_product = data_config.get("open_log_product", False)
        self.open_log_software = data_config.get("open_log_software", False)
        self.open_log_console = data_config.get("open_log_console", False)  # 🆕 Thêm log console

    # ========================= GETTERS =========================
    def get_path_log_img_oil(self):
        return self.path_log_img_oil

    def get_path_log_product(self):
        return self.path_log_product

    def get_path_log_software(self):
        return self.path_log_software

    def get_log_img_oil(self):
        return self.open_log_img_oil

    def get_log_product(self):
        return self.open_log_product

    def get_log_software(self):
        return self.open_log_software

    def get_log_console(self):
        return self.open_log_console

    # ========================= SETTERS =========================
    def set_open_log_img_oil(self, status: bool):
        self.open_log_img_oil = status
        self.wirte_data_config()

    def set_open_log_product(self, status: bool):
        self.open_log_product = status
        self.wirte_data_config()

    def set_open_log_software(self, status: bool):
        self.open_log_software = status
        self.wirte_data_config()

    def set_open_log_console(self, status: bool):
        """🆕 Bật / Tắt log console"""
        self.open_log_console = status
        self.wirte_data_config()

    # ========================= CONFIG FILE =========================
    def wirte_data_config(self):
        data_update = self.to_dict()
        OilDetectionSystem.folder.write_json_to_file(OilDetectionSystem.path_folder_config, data_update)

    def read_serial_config(self):
        return OilDetectionSystem.folder.read_json_from_file(OilDetectionSystem.path_folder_config)

    # ========================= HIỂN THỊ =========================
    def show_info(self):
        print(f"=== THÔNG TIN PHẦN MỀM ===")
        print(f"Tên phần mềm : {self.name}")
        print(f"Phiên bản     : {self.version}")
        print(f"Tác giả       : {self.author}")
        print("\n=== Trạng thái log và đường dẫn ===")
        print(f"• Log ảnh dầu : {'Mở' if self.open_log_img_oil else 'Đóng'} | Path: {self.path_log_img_oil}")
        print(f"• Log sản phẩm: {'Mở' if self.open_log_product else 'Đóng'} | Path: {self.path_log_product}")
        print(f"• Log phần mềm: {'Mở' if self.open_log_software else 'Đóng'} | Path: {self.path_log_software}")
        print(f"• Log console  : {'Mở' if self.open_log_console else 'Đóng'}")
        print("\n=== Thời gian lưu log (ngày) ===")
        print(f"Hình ảnh : {self.time_save_log_img}")
        print(f"Software : {self.time_save_log_software}")
        print(f"Excel    : {self.time_save_log_excell}")

    # ========================= DICT CONVERT =========================
    def to_dict_btn_status(self):
        return {
            "open_log_img_oil": self.open_log_img_oil,
            "open_log_product": self.open_log_product,
            "open_log_software": self.open_log_software,
            "open_log_console": self.open_log_console,
            "set_time_save_log_img": self.time_save_log_img,
            "set_time_save_log_software": self.time_save_log_software,
            "set_time_save_log_file_excell": self.time_save_log_excell,
        }

    def to_dict_infor_software(self):
        return {
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "path_log_img_oil": self.path_log_img_oil,
            "path_log_product": self.path_log_product,
            "path_log_software": self.path_log_software
        }

    def to_dict(self):
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
            "open_log_console": self.open_log_console,
            "set_time_save_log_software": self.time_save_log_software,
            "set_time_save_log_img": self.time_save_log_img,
            "set_time_save_log_excell": self.time_save_log_excell,
        }

    # ========================= CẬP NHẬT THỜI GIAN =========================
    def update_open_btn(self, open_log_img_oil, open_log_product, open_log_software, open_log_console,
                        time_save_software=None, time_save_img=None, time_save_excell=None):
        """Cập nhật toàn bộ trạng thái và thời gian log"""
        self.open_log_img_oil = open_log_img_oil
        self.open_log_product = open_log_product
        self.open_log_software = open_log_software
        self.open_log_console = open_log_console
        print(time_save_software,time_save_img,time_save_excell)
        if all(isinstance(v, (int, float)) and v >= 0 for v in [time_save_software, time_save_img, time_save_excell]):
            
            self.time_save_log_software = time_save_software
            self.time_save_log_img = time_save_img
            self.time_save_log_excell = time_save_excell
        else:
            print("❌ Một hoặc nhiều giá trị thời gian không hợp lệ (phải >= 0).")

        self.wirte_data_config()

    # ========================= SET TIME METHODS =========================
    def SetTimeSaveLogSoftware(self, days_software: int):
        if isinstance(days_software, int) and days_software > 0:
            self.time_save_log_software = days_software
            self.wirte_data_config()
            print(f"✅ Cập nhật thời gian lưu log phần mềm: {days_software} ngày")
        else:
            print("❌ Giá trị không hợp lệ. Vui lòng nhập số nguyên dương.")

    def SetTimeSaveLogImg(self, days_img: int):
        if isinstance(days_img, int) and days_img > 0:
            self.time_save_log_img = days_img
            self.wirte_data_config()
            print(f"✅ Cập nhật thời gian lưu log hình ảnh: {days_img} ngày")
        else:
            print("❌ Giá trị không hợp lệ. Vui lòng nhập số nguyên dương.")

    def SetTimeSaveLogExcell(self, days_excel: int):
        if isinstance(days_excel, int) and days_excel > 0:
            self.time_save_log_excell = days_excel
            self.wirte_data_config()
            print(f"✅ Cập nhật thời gian lưu log Excel: {days_excel} ngày")
        else:
            print("❌ Giá trị không hợp lệ. Vui lòng nhập số nguyên dương.")

    def SetTimeSaveAllLog(self, days_software: int, days_img: int, days_excel: int):
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

    # ========================= GET TIME METHODS =========================
    def GetTimeSaveLogSoftware(self) -> int:
        print(f"📄 Thời gian lưu log phần mềm hiện tại: {self.time_save_log_software} ngày")
        return self.time_save_log_software

    def GetTimeSaveLogImg(self) -> int:
        return self.time_save_log_img

    def GetTimeSaveLogExcell(self) -> int:
        print(f"📄 Thời gian lưu log Excel hiện tại: {self.time_save_log_excell} ngày")
        return self.time_save_log_excell

    def GetTimeSaveAllLog(self) -> dict:
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
# object_infor_software.update_open_btn(1,1,1,1,1,1,1)
# object_infor_software.show_info()

# #kiem tra update oke chua 
# object_infor_software.update_open_btn(True,True,True,50,50,50)

# object_infor_software.show_info()
# object_infor_software.set_open_log_software(True)



