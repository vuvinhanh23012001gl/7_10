import common_value 
class Count():
    from folder_create import Create
    obj_folder = Create()
    NAME_FILE_COUNT_PRODUCT = "count.json"
    NAME_VALUE_OK = "product_ok"
    NAME_VALUE_NG = "product_ng"
    path_file_count = obj_folder.get_or_create_json(NAME_FILE_COUNT_PRODUCT,common_value.NAME_FILE_STATIC)
    def __init__(self):
        self.OK = None
        self.NG = None
        self.total = None 
        self.default_data_if_file_emptry()
    def read_data_in_file(self):
        """Tra ve san pham ok, san pham ng"""
        data = Count.obj_folder.read_json_from_file(Count.path_file_count)   
        self.OK = data.get( f"{Count.NAME_VALUE_OK}",0)
        self.NG = data.get(f"{Count.NAME_VALUE_NG}",0) 
        return self.OK, self.NG
    def write_data(self,OK,NG):
        self.OK = OK
        self.NG = NG
        data_write = {
                f"{Count.NAME_VALUE_OK}":self.OK,
                f"{Count.NAME_VALUE_NG}":self.NG,
            }
        Count.obj_folder.write_json_to_file(Count.path_file_count,data_write)
    def default_data_if_file_emptry(self):
        data = Count.obj_folder.read_json_from_file(Count.path_file_count)
        self.OK = data.get( f"{Count.NAME_VALUE_OK}",0)
        self.NG = data.get(f"{Count.NAME_VALUE_NG}",0)
        self.write_data(self.OK,self.NG)
    def reset(self):
        self.OK = 0
        self.NG = 0
        self.write_data(self.OK,self.NG)
    def increase_ok(self, value=1):
        """Tăng số lượng sản phẩm OK"""
        self.read_data_in_file()  # Đảm bảo dữ liệu mới nhất
        self.OK += value
        self.write_data(self.OK, self.NG)

    def increase_ng(self, value=1):
            """Tăng số lượng sản phẩm NG"""
            self.read_data_in_file()
            self.NG += value
            self.write_data(self.OK, self.NG)


# count_produc  = Count()
# # oke,ng = count_produc.read_data_in_file()
# # print("ok",oke,"ng",ng)
# # count_produc.increase_ok()
# # count_produc.increase_ok()
# # count_produc.increase_ok()
# # count_produc.increase_ok()
# # count_produc.increase_ok()
# # oke,ng = count_produc.read_data_in_file()
# # print("ok",oke,"ng",ng)
# # count_produc.increase_ng()
# # count_produc.increase_ng()
# # count_produc.increase_ng()
# # count_produc.increase_ng()
# # oke,ng = count_produc.read_data_in_file()
# # print("ok",oke,"ng",ng)
# # count_produc.reset()





        




    
        










