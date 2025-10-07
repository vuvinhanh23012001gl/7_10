from producttype import ProductType
from typing import Dict,Any,List
from folder_create import Create
from process_master import Proces_Shape_Master
from common_value import NAME_FILE_STATIC,NAME_FILE_CHOOSE_MASTER
import json
import os
import func


class ProductTypeManager:
    
    FILE_NAME_STATIC  = NAME_FILE_STATIC
    NAME_FOLDER_PRODUCT_LIST = "Product_list"
    NAME_DATA_PRODUCT_LIST = "data.json"
    Proces_Shape = Proces_Shape_Master()

    def __init__(self):
        self.product_types = {}
        self.path_product_list = self.get_patd_datajson()    # Trả về đường dẫn của dẫn tới nơi lưu dữ liệu data.json
        self.data = self.get_file_data()                     # Lấy dữ liệu từ File đấy ra
        self.load_from_file()                                # Load File đấy ra

    def get_patd_datajson(self):
        """"Hàm này trả về đường dẫn,dẫn tới data.json"""
        object_folder = Create()
        return object_folder.get_path_grandaugter(ProductTypeManager.NAME_DATA_PRODUCT_LIST,ProductTypeManager.NAME_FOLDER_PRODUCT_LIST,ProductTypeManager.FILE_NAME_STATIC)

    def load_from_file(self):
        """Load File vào trong đối tượng Point dầu"""
        print("📥 Đang tải dữ liệu từ file JSON...")
        if self.data:
            for key in self.data.keys():
                type_id = self.data[key].get("type_id",-1)
                type_name = self.data[key].get("type_name",-1)
                xyz  = self.data[key].get("xyz",-1)
                if type_id == -1 or type_name == -1 or xyz == -1:
                    print("❌Không Tìm Thấy 1 Số Dữ liệu Khi Load Trả về False")
                    return
                product = ProductType(type_id,type_name,xyz)
                product.Init_path() #Tao File luon cho no
                for point in self.data[key]["point_check"]:
                    product.add_list_point(point["x"], point["y"], point["z"], point["brightness"])
                self.product_types[key] = product   #Thêm vào Sản phẩm
                # self.show_all()
        else:
            print("❌Data rỗng chưa có dữ liệu")
    def save_json_data(self, data_file_path:str):
        "Luu dữ liệu điểm vào đường link data data.json"
        try:
            dir_name = os.path.dirname(data_file_path)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name)
            with open(data_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.return_data_dict_all(), f, ensure_ascii=False, indent=4)
            print(f"✅ Đã lưu dữ liệu JSON vào: {data_file_path}")
        except Exception as e:
            print(f"❌ Lỗi khi lưu dữ liệu JSON: {e}")
    def add_product_type(self,id:str,name:str,xyz:list,description:str="")->bool:
        """Thêm đối tượng ProductType vào danh 1 loại sản phẩm mới vào danh sách các ProductType để quản lý
        Kiểm tra type nếu trùng rồi thì trả về  False
        Trả về True nếu thêm thành công và print lỗi
        Trả về False nếu thêm không thành công và print lỗi
        """
        product = ProductType(id,name,xyz)
        if description:
            product.description_product(description)
        status  = self.check_id_in_data(id)
        if status == 1: # Du lieu da co
            print("Dữ liệu đã có bị trùng ID Không lưu")
            return False
        elif status == 0:
            if(product.check_xyz()):
                print("🔔Kiểm tra trước khi thêm OKE")
                product.Init_path()
                self.product_types[product.type_id] = product
                try:

                    self.save_json_data(self.path_product_list)
                    self.data = self.get_file_data()
                    self.load_from_file()
                    return True
                except Exception as e:
                    print(f"❌ Lỗi khi lưu JSON sau khi thêm: {e}")
                    return False
            else:
                print("❌Lỗi Data Không Hợp Lệ")
                False
        else:
            print("File Trống Cứ Thế Lưu")
            product.Init_path()
            self.product_types[product.type_id] = product
            self.save_json_data(self.path_product_list)
            self.data = self.get_file_data()
            self.load_from_file()
            return True

    def get_file_data(self)->Dict[str, Any]:
        """Trả về data sản phẩm hiện tại ở trong tao File co ten neu khong co file do
           Trả về rỗng nếu không có dữ liệu trong file
        """
        object_folder = Create()
        return object_folder.get_data_grandaugter(ProductTypeManager.NAME_DATA_PRODUCT_LIST,ProductTypeManager.NAME_FOLDER_PRODUCT_LIST,ProductTypeManager.FILE_NAME_STATIC)

    def check_id_in_data(self, id: str) -> bool:
            """Trả về -1 nếu File trắng trả về 1 nếu có , trả về 0 nếu k có"""
            list_id = self.get_list_id_product()
            if list_id:
                if id in list_id:
                    return 1
                else:
                    return 0
            return -1

    def get_list_id_product(self)->List[any]:
        """Trả về list danh sách các ID,Nếu không có trả về mảng rỗng"""
        return [pt.type_id for pt in self.product_types.values()]

    def get_list_path_master(self)->List[any]:
        "Trả về danh sách đường dẫn đầy đủ của các lis path master c:\\Users\\anhuv\\Desktop\\26_08\\25-08\\app\\app\\static\\Master_Photo\\Master_Vinhanh', 'c:\\Users\\anhuv\\Desktop\\26_08\\25-08\\app\\app\\static\\Master_Photo\\Master_Vinhan132' "
        return [pt.path_img_master for pt in self.product_types.values()]

    def get_list_path_master_product_img_name(self,idtype:str)->List[Any]:
        """Trả về danh sách các path ảnh Master của loại ID đó"""
        if idtype is not None and  self.product_types is not None:
            for pt in self.product_types.values():
                if pt.type_id == idtype.strip():
                    # pt.get_path_name_folder_master_img() = static/Master_Photo/Master_SP01
                    return func.get_image_paths_from_folder(pt.get_path_name_folder_master_img())
        else:
            print("Tên ID hoặc dữ liệu chưa có")


    def find_by_id(self, type_id:str)->object:
        """Trả về đối tượng có id trùng với id nhập  nếu không có trả về -1"""
        return self.product_types.get(type_id,-1 )

    def get_list_point_find_id(self,type_id_product:str)->dict:
        """Trả về None nếu không tìm thấy, Trả về mảng danh sách điểm có ID trùng"""
        result =  self.find_by_id(type_id_product)
        if result == -1:
            return  None
        else :
            return result.get_list_point()

    def get_product_name_find_id(self,type_id_product:str)->dict:
        """Trả về tên sản phẩm nếu trùng ID nếu không trả về None"""
        result =  self.find_by_id(type_id_product)
        if result == -1:
            return None
        else :
            return result.get_type_name()

    def get_path_product_img_name(self,idtype:str):
        """Trả về None nêu không tìm thấy sp có typeid còn không trả về link ảnh của sản phẩm"""
        if idtype is not None and  self.product_types is not None:
            for pt in self.product_types.values():
                if pt.type_id == idtype.strip():
                     return pt.get_path_name_folder_product_img()
        else:
            print("Tên ID hoặc dữ liệu chưa có")

    def absolute_path(self,idtype:str):
        """object :Trả về None nêu không tìm thấy sp có typeid còn không trả về link đường dẫn tuyệt đối của sản phẩm"""
        if idtype is not None and  self.product_types is not None:
            for pt in self.product_types.values():
                if pt.type_id == idtype.strip():
                    return pt.Path_Product
        else:
            print("Tên ID hoặc dữ liệu chưa có")

    def show_all(self):
        """object : show toàn bộ thông tin có trong đối tượng"""
        if not self.product_types:
            print("❌ Chưa có loại sản phẩm nào.")
            return
        print("📦 Danh sách loại sản phẩm:")
        for pt in self.product_types.values():
            pt.show_product_type()
            print("-" * 40)

    def get_all_ids_and_names(self):
        """Trả về dict ID và Name của các sản phẩm hiện có"""
        return {
            "list_id": [pt.type_id for pt in self.product_types.values()],
            "list_name": [pt.type_name for pt in self.product_types.values()],
            "xyz":    [pt.xyz for pt in self.product_types.values()]
        }

    def return_data_dict_all(self):
        """object: Trả về danh sách dữ data dict có trong đối tượng"""
        result = {}
        for i in self.product_types.values():
            result[i.type_id] = i.protype_to_dict()
        # print(result)
        return result

    def get_all_id(self):
        """Trả về danh sách các ID"""
        return list(self.product_types.keys())

    def count(self):
        """Đếm số lượng sản phảm hiện có"""
        return len(self.product_types)

    def return_data_dict(self,type_id):
        """Trả về dict của ID nhập"""
        if(self.find_by_id(type_id)!= -1):
             return self.find_by_id(type_id).protype_to_dict()
    def return_data_list_point(self,type_id:str)->list:
        """Trả về list point cua id loại cần nhập trả về None nếu không tìm thấy ID"""
        if(self.find_by_id(type_id)!= -1):
             return [ i.dict_point_oil()  for i in self.find_by_id(type_id).get_list_point()]
    def remove_product_in_file_data(self,id:str):
        """Xóa sản phẩm có ID trả về True nếu thành công không ngược lại  > Chỉ thực hiện xóa data thông chưa xóa đường linh ảnh . link treain, link sản phẩm"""
        if id in self.get_all_id():
            status_pop = self.product_types.pop(id,None)
            if status_pop is None:
                print(f"Xóa File có ID:{id} không thành công")
                return False
            else:
                print(self.return_data_dict_all())
                self.save_json_data(self.path_product_list)
                self.data = self.get_file_data()
                self.load_from_file()
                print(f"Xóa ID:{id} thành công trong file data.json")
                return True
        else:
            print("Không tìm thấy ID trong danh sách")
            return False

    def add_list_point_to_product(self,type_id:str,x:int,y:int,z:int,brightness:int)->bool:
        if type_id is None or x is None or y is None or z is None or brightness is None:
            print("Giá trị đầu vào khác Null")
            return False
        isObject = self.find_by_id(type_id)
        if isObject != -1:
            #Kiem tra xem co diem nao giong diem cho truoc khong
            arr_list_locations = self.get_list_point_find_id(type_id)
            if arr_list_locations is None: return False
            for arr_list_location in arr_list_locations:
                x_location = arr_list_location.get_x()
                y_location = arr_list_location.get_y()
                z_location = arr_list_location.get_z()
                if x_location == x and y_location == y and z_location == z:
                     print("Điểm đã tồn tại, không thể thêm điểm trùng.")
                     return False
                # Kiem tra lon hon 0
                if x < 0 or y < 0 or z < 0:
                    print("Giá trị x, y, z phải lớn hơn hoặc bằng 0.")
                    return False
                # Kiem tra co nho hon xyz quy định
                xyz = isObject.get_xyz()
                if x > xyz[0] or y > xyz[1] or z > xyz[2]:
                    print(f"Giá trị x, y, z phải nhỏ hơn hoặc bằng {xyz}.")
                    return False
            isObject.add_list_point(x, y, z, brightness)
            self.update_data_json()
            print("Thêm điểm thành công")
            return True
        print("Không tìm thấy ID trong danh sách")
        return False
    def fix_score_point_product(self,type_id:str,x:int,y:int,z:int,brightness:int,index)->bool:
        if type_id is None or x is None or y is None or z is None or brightness is None:
            print("Giá trị đầu vào khác Null")
            return False
        isObject = self.find_by_id(type_id)
        if isObject != -1:
            if x < 0 or y < 0 or z < 0:
                    print("Giá trị x, y, z phải lớn hơn hoặc bằng 0.")
                    return False
            xyz = isObject.get_xyz()
            if x > xyz[0] or y > xyz[1] or z > xyz[2]:
                    print(f"Giá trị x, y, z phải nhỏ hơn hoặc bằng {xyz}.")
                    return False
            print("đã vào đây")
            status_update_point = isObject.update_point_by_index(index,x, y, z, brightness)
            if status_update_point:
                self.update_data_json()
                print("Thêm điểm thành công")
                return True
            print("Thêm điểm không thành công")
            return False
        print("Không tìm thấy ID trong danh sách")
        return False
    def update_data_json(self)->None:
        self.save_json_data(self.path_product_list)
        self.data = self.get_file_data()
        self.load_from_file()
        print("Cập nhật lại dữ liệu")

    def create_file_and_path_img_master(self,idtype:str,name_img:str)->bool:
        """đầu vào: ID cần tìm , tên ảnh nếu tìm thấy
        chức năng hàm :  Tạo ra 1 đường dẫn ảnh có tên name_img nằm trong thư mục ảnh master của loại sản phẩm
        """
        strip_data = idtype.strip()
        result =  self.find_by_id(strip_data)
        if result != -1:
            path_master = result.get_path_img_master()
            if not path_master:
                print("Không tìm thấy đường dẫn Path")
                return False
            object_folder = Create()
            status = object_folder.create_file_in_folder(path_master,name_img)
            # self.path_img_master =
            return status
        else :
            print("Không tìm thấy ID")
            return False

    def remove_product_type(self, type_id:str)->bool:
        """Xóa tất cả liên quan đến ID như master, đường link ảnh, đường link
        sản phẩm choose master,đường link retraing,dât lưu trong file data"""
        print("Tiến Hành Xóa ID")
        type_id = type_id.strip()
        isObject = self.find_by_id(type_id)
        if isObject!= -1:
            path_master = isObject.get_path_img_master()
            path_retraining = isObject.get_path_img_retraning()
            if path_master is not None and path_retraining is not None:
                print("File Tồn tại")
                object_folder = Create()
                print(path_master,"\n",path_retraining)
                status_img_master = object_folder.delete_folder(path_master)
                status_img_retraining = object_folder.delete_folder(path_retraining)
                if not status_img_master:
                    print("Xóa Path Img master Không Thành công")
                    return False
                if not status_img_retraining:
                    print("Xóa Path IMG retraining không thành công")
                    return False
                if status_img_master:
                    print("Xóa Folder matster thành công")
                if status_img_retraining:
                    print("Xóa Folder retraining thành công")
                path_product = isObject.get_Path_Product()
                if path_product:
                     path_img = object_folder.find_file_in_folder(path_product,f"Img_{isObject.type_id.strip()}.png")
                     if(path_img):
                        print("Xóa File ảnh thành công",path_img)
                        status_img_product = object_folder.delete_file(path_img)
                        if not status_img_product:
                            print("Xóa File ảnh sản phẩm không thành công")
                        else:
                            print("Xóa File ảnh sản phẩm thành công")
                     else :
                        print("Không tìm thấy File ảnh lưu sản phẩm xóa ảnh chưa đc")
                else:
                    print("Đường dẫn tới Product_Photo không tồn tại")
                ProductTypeManager.Proces_Shape.get_file_data_json()  #Dam bao tat ca du lieu la moi nhat
                status_erase_master = ProductTypeManager.Proces_Shape.erase_product_master(type_id)
                status = self.remove_product_in_file_data(type_id)
                if status !=False  and status_erase_master != False:
                    print("Xóa thành công 4 File")
                    func.create_choose_master(NAME_FILE_CHOOSE_MASTER) # tạo file choose_master nếu tạo rồi thì thôi
                    choose_master_index = func.read_data_from_file(NAME_FILE_CHOOSE_MASTER)# đọc lại file choose master cũ xem lần trước  người dùng chọn gì
                    choose_product = choose_master_index.strip()
                    print(type(choose_product))
                    print("choose_product",choose_product)
                    if choose_product == type_id:
                        #xoa du lieu reset neu dang chon ve 0
                        func.clear_file_content(NAME_FILE_CHOOSE_MASTER)
                        func.write_data_to_file(NAME_FILE_CHOOSE_MASTER,"0")
                    print("Xóa thành công")
                    return True
                else:
                    print("Xóa bị False")
                    return False
            else:
                print("File không tồn tại")
                return False
        else:
            print("Không tìm thấy ID")
            return False
    def remove_img_master_index_of_product(self,ID,index):
        """Xóa ảnh master có index ở vị trí index"""
        print("Tiến hành xóa ảnh master thứ index")
        list_id = self.get_list_id_product()
        if ID in list_id:
                if index < 0:
                    print("Index phải lớn 0")
                    return False  
                try:      
                   isObject = self.find_by_id(ID)
                   path_master = isObject.get_path_img_master()
                   print("Tìm ảnh có tên trong đường dẫn",path_master)
                   list_file_in_dir_befor_index = os.listdir(path_master)
                   if not list_file_in_dir_befor_index:
                       print("Danh sách rỗng")
                       return False
                   if len(list_file_in_dir_befor_index) <= index:
                       print("Trong thư mục ảnh chứa không index không hợp lệ") # trường hợp này xảy ra khi Data vị trí có nhưng chưa chụp ảnh lưu 
                       return False
                   else:
                       print(f"Tìm ảnh có index :{index}")
                       name_file_index = self.find_file_by_index(list_file_in_dir_befor_index,index)
                       patd_index = os.path.join(path_master,name_file_index)
                       if not os.path.exists(patd_index):
                           print("File không tồn tại")
                           return False
                       else:
                           print("File tồn tại Tiến hành xóa File")
                           os.remove(patd_index)
                           print("Tiến hành đổi tên File ảnh")
                           list_file_in_dir_after_index = os.listdir(path_master)
                           print("Danh sách trước khi xóa",list_file_in_dir_befor_index)
                           print("Danh sách sau khi xóa",list_file_in_dir_after_index)
                           arr_new = self.insert_missing_files(list_file_in_dir_after_index,len(list_file_in_dir_after_index)-1)
                           for value1,value2 in zip(list_file_in_dir_after_index,arr_new):
                               path_value1 = os.path.join(path_master,value1)
                               path_value2 = os.path.join(path_master,value2)
                               print(path_value1)
                               print(path_value2)
                               os.rename(path_value1,path_value2)
                           print("Đổi tên thành cống")
                           print(f"Xóa file {name_file_index} thành công")
                           return True
                except:
                    print("Xóa lỗi, ko xóa được")
                    return False
        else:
            print("Không tìm thấy ID trong list ID")
            return False

    def remove_data_index_of_product(self,ID:str,index:int):
        """Sẽ xóa data ơ vi tri index có trong 1 ID trả về True nếu xóa thành công tra về False nếu xóa không thành công"""
        list_id = self.get_list_id_product()
        if ID in list_id:
            arr_point = self.get_list_point_find_id(ID)
            if arr_point:
                if len(arr_point) <= index:
                    print("Index phải nhỏ hơn số lượng điểm trong sách điểm")
                    return False
                if index < 0:
                    print("Index phải lớn 0")
                    return False  
                try:      
                   self.product_types[ID].list_point.pop(index)
                   self.update_data_json()
                   print("Xóa index thành công")
                   return True
                except:
                    print("Xóa lỗi, ko xóa được")
                    return False
            else:
                print("Sản phẩm chưa có list ID")
                return False

        else:
            print("Không tìm thấy ID trong list ID")
            return False
    def find_file_by_index(self, file_list, index):
        target_file_name = f"img_{index}.png"
        if target_file_name in file_list:
            return target_file_name
        else:
            return None  # or you can return a custom message
    def insert_missing_files(self,file_list, max_index):
        result = []
        for i in range(max_index + 1):
            file_name = f"img_{i}.png"
            if file_name in file_list:
                result.append(file_name)
            else:
                result.append(file_name)  # still add to maintain order; can be handled differently if needed
        return result
    
    def remove_all_master_index(self,ID:str,index:int):
        print("--------------------------------------Remove All Master Index ------------------------------------")
        print("--------------------------------------Cần theo dõi hàm này ------------------------------------")
        statuse_erase_master_index = ProductTypeManager.Proces_Shape.erase_master_index(ID,index)
        print("--------------------------------------Kết thúc theo dõi hàm này ------------------------------------")
        statuse_erase_img = self.remove_img_master_index_of_product(ID,index)
        statuse_erase_data = self.remove_data_index_of_product(ID,index)
        if statuse_erase_img == True and statuse_erase_data == True:
            print("Xóa thành công ảnh master thứ ",index)
            print("Xóa thành công dữ liệu master thú",index)
            if not statuse_erase_master_index:
                print("Xóa không thành công dữ liệu master do....")
            else:
                print("Xóa thành công dữ liệu master")
        print("---------------------------------------------o0o--------------------------------------------------")




# #----------------------------------------------------------------------------------------------------------------------------
# quanly = ProductTypeManager()
# quanly.remove_data_index_of_product("SP01",3)

# quanly = ProductTypeManager()
# quanly.remove_all_master_index("SP01",1)

# quanly = ProductTypeManager()
# quanly.remove_img_master_index_of_product("SP01",0)
# quanly = ProductTypeManager()
# quanly.remove_product_type("SP02")

# quanly = ProductTypeManager()
# quanly.remove_data_index_of_product("SP01",3)

# quanly = ProductTypeManager()
# print(quanly.get_list_path_master())

# quanly = ProductTypeManager()
# print(quanly.remove_product_in_file_data('S201'))

# quanly = ProductTypeManager()
# print(quanly.get_list_path_master_product_img_name("SP01"))

# quanly = ProductTypeManager()
# print(quanly.create_file_and_path_img_master("SP01","anh1.png"))

# quanly = ProductTypeManager()
# quanly.remove_product_type("0")

# quanly = ProductTypeManager()
# print(quanly.return_data_dict("SP01"))

# quanly = ProductTypeManager()
# print(quanly.return_data_list_point("SP02"))

# quanly = ProductTypeManager()
# print(quanly.get_all_ids())

# quanly = ProductTypeManager()
# print(quanly.count())

# quanly = ProductTypeManager()
# print(quanly.find_by_id("SP1"))


# quanly = ProductTypeManager()
# for i in quanly.get_list_point_find_id("SP001"):
#     print(i)

# quanly = ProductTypeManager()
# print(quanly.get_product_name_find_id("SP12"))

# quanly = ProductTypeManager()
# quanly.show_all()

# quanly = ProductTypeManager()
# print(quanly.get_all_ids_and_names())

# quanly = ProductTypeManager()
# print(quanly.get_file_data())

# # # # # quanly.load_from_file()

# quanly = ProductTypeManager()
# quanly.add_list_point_to_product("SP01",1,41,8,80)
# quanly.add_list_point_to_product("SP01",56,70,10,80)
# quanly.add_list_point_to_product("SP01",80,60,12,80)

# quanly = ProductTypeManager()
# quanly.fix_score_point_product("SP01",12,40,12,80,2)
# # # # # quanly = ProductTypeManager()
# # # # # print(quanly.get_list_id_product())

# # # # # quanly = ProductTypeManager()
# # # # # print(quanly.get_list_path_master())
# # print(quanly.get_list_path_master_product_img_name("typeid1"))

# quanly.add_product_type("typeid1","xinchoa",[1,2,3])
# quanly.add_product_type("typeid2","xinchoa2",[1,2,3])

# quanly = ProductTypeManager()
# print(quanly.return_data_dict_all())


# print(quanly.find_by_id("idtype1"))
# print(quanly.get_list_point_find_id("idtype1"))
# # path = quanly.get_list_path_master()

# # # print(path)
# # path  = quanly.get_list_path_master_product_img_name("idtype1")
# # print(path)

# quanly = ProductTypeManager()
# # # # # # print(quanly.find_by_id("typeid2"))
# print(quanly.get_path_product_img_name("SP01"))

# quanly = ProductTypeManager()
# print(quanly.absolute_path("SP01"))

# # print(quanly.get_file_data())
# # # # # # Tạo các loại sản phẩm
# pt1 = ProductType("idtype4", "Loại A")
# pt2 = ProductType("idtype5", "Loại B")

# # # # # # # # # Thêm các điểm
# pt1.add_list_point(1, 2, 3, 10)
# pt1.add_list_point(4, 5, 6, 20)

# pt2.add_list_point(7, 8, 9, 30)
# pt2.add_list_point(10, 11, 12, 40)
# # # # # # # # # Thêm vào danh sách quản lý


# quanly.return_data_dict_all()
# pt3 = ProductType("idtype3", "Loại C")
# pt3.add_list_point(7, 8, 9, 30)
# pt3.add_list_point(10, 11, 12, 40)





# quanly.return_data_dict_all()
# # # # Hiển thị toàn bộ

# # quanly.show_all()
# quanly.load_from_file()
# quanly.remove_product_type("idtype1")
# print(quanly.return_data_dict("idtype2"))
# print(quanly.return_data_dict_all())
# print(quanly.get_file_data())
# print(quanly.return_data_dict_all())
# Hiển thị sau khi xóa



# Loai_1  = ProductType("SP02", "Loại A",[1,2,3])
# Loai_1.add_list_point(1, 2, 3, 10)
# Loai_1.add_list_point(1, 2, 3, 10)
# Loai_1.add_list_point(1, 2, 3, 10)
# Loai_1.add_list_point(3, 2, 5, 10)