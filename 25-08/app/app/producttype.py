from point_oil import PointOil
from common_value import NAME_FILE_STATIC
from common_value import NAME_FILE_IMG_RETRAINING 
import os

class ProductType:
    #Variable
    NAME_FILE_PRODUCT_PHOTO = "Product_Photo"
    NAME_FILE_STATIC_CLASS = NAME_FILE_STATIC
    NAME_FILE_MASTER_PHOTO = "Master_Photo"
    def __init__(self, type_id:str, type_name:str,xyz:list):
        self.xyz = xyz
        self.type_id = str(type_id)
        self.type_name = type_name
        self.list_point = []
        self.description =  " Description deafaut "    #se tao ra duong dan anh trong file static/Product_Photo
        self.Path_Product = None
        self.path_img_master = None
        self.path_img_retraining = None
    def get_xyz(self):
        return self.xyz
    def set_xyz(self, value):
        self.xyz = value
    def check_xyz(self):
         if not self.xyz:
              return False
         if(self.xyz[0] < 0 or self.xyz[1] < 0 or self.xyz[2]<  0):
              print("Dữ liệu bị âm")
              return False
         return True
    def Init_path(self):
        """Tao ra cac duong dan neu co roi thi thoi khong thong bao loi"""
        name_file_parent = os.path.dirname(os.path.abspath(__file__))
        static = os.path.join(name_file_parent,ProductType.NAME_FILE_STATIC_CLASS)
        path_product = os.path.join(static,ProductType.NAME_FILE_PRODUCT_PHOTO )  #tao ra duong dan chuan Product_Photo
        path_img_retraining = os.path.join(static,NAME_FILE_IMG_RETRAINING)  #tao ra duong dan chuan Product_Photo
        path_master = os.path.join(static,ProductType.NAME_FILE_MASTER_PHOTO)   #tao ra duong dan chuan Master_Photo
        # print(path_master)
        # print(path_product)
        os.makedirs(path_product, exist_ok=True)  #tao ra 2 thu muc path_product va path_master
        os.makedirs(path_master, exist_ok=True)
        os.makedirs(path_img_retraining, exist_ok=True)
        path_img_master = os.path.join(path_master,f"Master_{self.type_id}")
        path_img_retraining = os.path.join(path_img_retraining,f"IMG_Retraining_{self.type_id}")
        self.path_img_master = path_img_master
        self.path_img_retraining = path_img_retraining
        self.Path_Product = path_product
        os.makedirs(path_img_master, exist_ok=True)
        os.makedirs(path_img_retraining, exist_ok=True)
        return {"Path_Product":path_product,
                "Path_Master": path_img_master,
                "Path_img_retraining":path_img_retraining
        }
    def description_product(self,commment):
        self.description = commment
        return self.description 
    def add_list_point(self, x, y, z, brightness):
        if self.type_id is not None and self.type_name is not None:
            self.list_point.append(PointOil(x, y, z, brightness))
            print("✅ Thêm điểm thành công.")
        else:
            print("❌ Một trong hai giá trị 'type_id' hoặc 'type_name' chưa được khởi tạo.")

    def remove_item_list_point_index(self, index):  # index tính từ 0
        if self.type_id is not None and self.type_name is not None:
            if not self.list_point:
                print("❌ Danh sách rỗng, không thể xóa.")
                return False
            elif 0 <= index < len(self.list_point):
                print(f"🗑️ Đang xóa phần tử tại vị trí {index}...")
                self.list_point.pop(index)
                print("✅ Xóa thành công.")
                return True
            else:
                print(f"❌ Index {index} không hợp lệ. Độ dài hiện tại: {len(self.list_point)}")
                return False
        else:
            print("❌ 'type_id' hoặc 'type_name' chưa được khởi tạo.")
            return False
    def show_product_type(self):
        print("🛠️ Thông tin sản phẩm:")
        print("🔹 ID Type     :", self.type_id)
        print("🔹 Type Name   :", self.type_name)
        print("🔹Desception product :",self.description)
        print("🔹XYZ :",self.xyz )
        [print(i) for i in self.list_point]
    def return_lent_poit_of_product(self):
        return len(self.list_point)
    def protype_to_dict(self):
        return {
            "type_id": self.type_id,
            "type_name": self.type_name,
            "description": self.description,
            "len": self.return_lent_poit_of_product(),
            "xyz" :self.get_xyz(),
            "path_img_product":self.get_path_name_folder_product_img(),
            "path_img_master":self.get_path_name_folder_master_img(),
            "point_check":[i.dict_point_oil()  for i in self.list_point ]
        }
    def get_path_name_folder_product_img(self):  #
                file_path = os.path.abspath(__file__)
                path_static = os.path.join(file_path,ProductType.NAME_FILE_STATIC_CLASS)
                path_Product_Photo = os.path.join(path_static,ProductType.NAME_FILE_PRODUCT_PHOTO )
                path_img = os.path.join(path_Product_Photo,f"IMG_{self.type_id}.png".replace(" ", ""))
                path_img_ok = self.get_path_from_static(path_img)
                return path_img_ok.replace('\\', '/')
    def get_path_name_folder_master_img(self):
                path_img_ok = self.get_path_from_static(self.path_img_master)
                return path_img_ok.replace('\\', '/')
    
    def get_path_from_static(self,full_path):
        parts = full_path.split(ProductType.NAME_FILE_STATIC_CLASS, 1)
        if len(parts) > 1:
            return ProductType.NAME_FILE_STATIC_CLASS + parts[1]
        else:
            return None
    def get_list_point(self)->list[set]:
        """Hàm này trả về danh sách các điểm dầu của một loại sản phẩm
           Trả về mảng rỗng nếu không có
        """
        return self.list_point
  
    def get_path_img_retraning(self):
         """Trả về None nếu không tìm có path nếu có trả về đường dẫn đến ảnh Retraining data"""
         return self.path_img_retraining
    def get_type_name(self):
        """ Trả về tên loại sản phẩm"""
        return self.type_name
    # Getter
    def get_Path_Product(self):
        """Trả về đường dẫn ảnh của sản phẩm"""
        return self.Path_Product    
    def get_path_img_master(self):
        """Trả về đường dẫn tuyệt đối của sản IMG Master"""
        return self.path_img_master
    def update_point_by_index(self, index: int, x=None, y=None, z=None, brightness=None):
        """
        Cập nhật thông tin của một điểm dầu theo vị trí index.
        - index: vị trí phần tử trong list_point (bắt đầu từ 0)
        - x, y, z, brightness: giá trị mới (nếu None thì giữ nguyên giá trị cũ)
        Trả về True nếu cập nhật thành công, False nếu lỗi.
        """
        if not self.list_point:
            print("❌ Danh sách rỗng, không thể sửa.")
            return False

        if 0 <= index < len(self.list_point):
            point = self.list_point[index]

            # Giữ nguyên giá trị cũ nếu không truyền vào
            point.x = x if x is not None else point.x
            point.y = y if y is not None else point.y
            point.z = z if z is not None else point.z
            point.brightness = brightness if brightness is not None else point.brightness

            print(f"✏️ Đã cập nhật điểm tại index {index}: (x={point.x}, y={point.y}, z={point.z}, brightness={point.brightness})")
            return True
        else:
            print(f"❌ Index {index} không hợp lệ. Độ dài hiện tại: {len(self.list_point)}")
            return False
         
# Loai_1  = ProductType("1", "Loại A",[1,2,3])
# Loai_1.add_list_point(1, 2, 3, 10)
# Loai_1.add_list_point(1, 2, 3, 10)
# Loai_1.add_list_point(1, 2, 3, 10)
# Loai_1.add_list_point(3, 2, 5, 10)
# Loai_1.show_product_type()
# print(type(Loai_1.list_point))



# data = Loai_1.get_path_name_folder_product_img()
# # # print(data)
# # # # Loai_1.description_product("San pham duoc san xuat nam 2024")  

# # # print(Loai_1.protype_to_dict())
# # # # #print(Loai_1.Init_path()) #tra ve duong dan den master va product

# # # # print(Loai_1.return_lent_poit_of_product())
# # # # # Loai_1.get_list_images_by_type_name()
# # # # # # print("-------------xoa-----------------")
# # # # # # Loai_1.remove_item_list_point_index(1)
# # # # # # Loai_1.show_product_type()
# # # # print(Loai_1.protype_to_dict())
# print(Loai_1.get_list_point()[0].)