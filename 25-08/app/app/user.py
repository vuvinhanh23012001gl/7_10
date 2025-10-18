from folder_create import Create
import common_value
import common_object   

USER_ADMIN = "BIVNRDP"
PASSWORD_ADMIN = "BIVNRDP"

class acc_use():
    def __init__(self,user_name ="None",use_password="None",first_name="None",last_name="None",line="None",usine="None"):
        self.id = None
        self.first_name = first_name
        self.last_name = last_name
        self.line = line
        self.usine = usine
        self.user_name = user_name
        self.use_password = use_password

    def show_infor_user(self):
        """Hiển thị toàn bộ thông tin của user."""
        common_object.obj_log.log_and_print("===== USER INFORMATION =====")
        common_object.obj_log.log_and_print("First Name:", self.first_name)
        common_object.obj_log.log_and_print("Last Name:", self.last_name)
        common_object.obj_log.log_and_print("Username:", self.user_name)
        common_object.obj_log.log_and_print("Password:", self.use_password)
        common_object.obj_log.log_and_print("Line:", self.line)
        common_object.obj_log.log_and_print("Usine:", self.usine)
        common_object.obj_log.log_and_print("============================")
    def to_dict(self):
        """Chuyển thông tin user thành dictionary."""
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "user_name": self.user_name,
            "use_password": self.use_password,
            "line": self.line,
            "usine": self.usine
        }

# user = acc_use()
# user.show_infor_user()

class acc_admmin():
    def __init__(self,admin_name = USER_ADMIN,admin_password=PASSWORD_ADMIN):
        self.admin_name = admin_name
        self.admin_password = admin_password
    def show_infor_use(self):
        """In thong tin tai khoan mat khau cua user """
        common_object.obj_log.log_and_print("User:",self.admin_name)
        common_object.obj_log.log_and_print("Password:",self.admin_password)
    def to_dict(self):
        """Chuyển thông tin admin thành dictionary."""
        return {
            "admin_name": self.admin_name,
            "admin_password": self.admin_password
        }

class Manage_User():
    object_folder =  Create()
    NAME_FILE_JSON_USER  = "acc_user.json"
    NAME_FILE_JSON_ADMIN =  "acc_admin.json"
    path_admin = object_folder.get_path_grandaugter(NAME_FILE_JSON_ADMIN,common_value.NAME_FOLDER_USER,common_value.NAME_FILE_STATIC)
    path_user = object_folder.get_path_grandaugter(NAME_FILE_JSON_USER,common_value.NAME_FOLDER_USER,common_value.NAME_FILE_STATIC)
    def __init__(self):
        self.data_use = [] 
        self.data_admin = {}
    def create_user(self, user_name:str=None, use_password:str=None, first_name:str=None, last_name:str=None, line:str=None, usine:str=None):
        if not all([user_name, use_password, first_name, last_name, line, usine]):
            common_object.obj_log.error("Thiếu dữ liệu khi tạo tài khoản User")
            return False,"Thiếu dữ liệu khi tạo tài khoản"
        arr_user = []
        object_user = acc_use(user_name,use_password,first_name, last_name,line,usine)
        self.data_use = Manage_User.object_folder.get_data_grandaugter(Manage_User.NAME_FILE_JSON_USER,common_value.NAME_FOLDER_USER,common_value.NAME_FILE_STATIC)  # cap nhat truoc khi thay
        if self.data_use:
            for acc in self.data_use:
                user_name_file = acc.get("user_name",None)
                if user_name_file:
                    if user_name_file.strip() == user_name.strip():
                        return False,"Tài khoản này đã tồn tại"
            self.data_use.append(object_user.to_dict())  #cap nhat du lieu moi
            Manage_User.object_folder.save_json(self.data_use,Manage_User.path_user) # luu du lieu moi vao file
            common_object.obj_log.info(f"Lưu {user_name} thành công vào list File User")
            return True,"Tạo thành công tài khoản"
        else:
            arr_user.append(object_user.to_dict())
            Manage_User.object_folder.save_json(arr_user,Manage_User.path_user)
            common_object.obj_log.info(f"Lưu {user_name} vào phần tử đầu tiên trong list File User")
            return True,"Tạo thành công tài khoản"
    def delete_user(self, user_name: str):
        """Xóa user theo user_name"""
        if not user_name:
            common_object.obj_log.error("Chưa cung cấp user_name để xóa")
            return False

        # Load dữ liệu user hiện tại
        self.data_use = Manage_User.object_folder.get_data_grandaugter(
            Manage_User.NAME_FILE_JSON_USER,
            common_value.NAME_FOLDER_USER,
            common_value.NAME_FILE_STATIC
        )

        if not self.data_use:
            common_object.obj_log.error("Danh sách user đang trống, không thể xóa")
            return False

        # Tìm và xóa user
        new_data_use = [user for user in self.data_use if user.get("user_name", "").strip() != user_name.strip()]

        if len(new_data_use) == len(self.data_use):
            common_object.obj_log.warning(f"Không tìm thấy user {user_name} để xóa")
            return False

        # Lưu lại file JSON sau khi xóa
        Manage_User.object_folder.save_json(new_data_use, Manage_User.path_user)
        common_object.obj_log.info(f"Xóa user {user_name} thành công")
        return True
    def create_admin(self, admin_name: str = "", admin_password: str = None):
        if not all([admin_name,admin_password]):
            common_object.obj_log.error("Thiếu dữ liệu khi tạo tài khoản Admin tạo tài khoản admin mặc định")
            obj_acc_admmin = acc_admmin()
            self.data_admin  = obj_acc_admmin.to_dict()
            Manage_User.object_folder.save_json(self.data_admin,Manage_User.path_admin) # luu du lieu moi vao file
        if admin_name and admin_password:
            obj_acc_admmin = acc_admmin(admin_name,admin_password)
            self.data_admin  = obj_acc_admmin.to_dict()
            Manage_User.object_folder.save_json(self.data_admin,Manage_User.path_admin) # luu du lieu moi vao file

    def check_account(self, account_name: str, password: str):
        """
        Kiểm tra tài khoản:
        - Nếu tồn tại trả về (True, True) nếu admin
        - Trả về (True, False) nếu user
        - Nếu không tồn tại trả về (False, False)
        """
        # Kiểm tra admin
        self.data_admin = Manage_User.object_folder.get_data_grandaugter(
            Manage_User.NAME_FILE_JSON_ADMIN,
            common_value.NAME_FOLDER_USER,
            common_value.NAME_FILE_STATIC
        )
        if self.data_admin:
            if (self.data_admin.get("admin_name", "").strip() == account_name.strip() and
                self.data_admin.get("admin_password", "") == password):
                return True, True

        # Kiểm tra user
        self.data_use = Manage_User.object_folder.get_data_grandaugter(
            Manage_User.NAME_FILE_JSON_USER,
            common_value.NAME_FOLDER_USER,
            common_value.NAME_FILE_STATIC
        )
        if self.data_use:
            for user in self.data_use:
                if (user.get("user_name", "").strip() == account_name.strip() and
                    user.get("use_password", "") == password):
                    return True, False
        return False, False



# manager_one = Manage_User()
# print(manager_one.check_account("use_password","use_password"))
# manager_one.delete_user("user_name21")
# manager_one.create_admin()


    
