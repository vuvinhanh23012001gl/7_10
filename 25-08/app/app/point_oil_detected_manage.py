from point_oil_detected import point_oil_detect
import matplotlib.pyplot as plt
import numpy as np
import cv2

class Manage_Point_Oil_Detect: 
    # lớp này được tạo nhiều lần mỗi khi có dữ liệu mới cần kiểm tra
    calib_Z = [0,1,2,3,4,5,6,7,8,9,10,11,12]         #Z (mm)
    calib_scale =[0.02803687, 0.02819555, 0.02781955, 0.02737275, 0.02645114, 0.02617547, 0.02583149, 0.0253135, 0.02422303, 0.02326263, 0.02251462, 0.02176587, 0.02129404] #scale (mm/pixel)
    def __init__(self,data=None,Z=None):
        self.data = data
        self.list_object_point = []  #danh sach doi tuong diem
        self.number_point = None #nhieu ham can 
        self.Init_Object_Oil(Z) #cu co danh sach diem dau duoc tao thi se tao ngay ra cac diem # Chạy luôn thuộc tính diện tích để đối tượng từng khung master 1 có luôn diện tích
    def check_list_object_point(self):
        """Trả về True nếu tồn tại Ngược lại là False """
        return True if self.list_object_point else False
    def check_data(self):
        return True if self.data else False
    def check_number_point(self):
        """Trả về True nếu tồn tại Ngược lại là False """
        return True if self.number_point else False
    
    def show_data_all_yollo(self):
        """Show tất cả thông tin nhận được"""
        print(self.data)

    def get_speed_detect_and_time_total(self):
        """Hàm này trả về thông tin ảnh cho vào mô hình và thời gian xử lý và training
        {'preprocess': 3.1358999985968694, 'inference': 56.27849999291357, 'postprocess': 4.37370000872761}
        """
        if self.data:
            try:
                # print(self.data[0].speed)
                return self.data[0].speed
            except Exception as e:
                print("Không tìm thấy Speed:", e)
                return None
        else:
            print("data khong ton tai")
    def get_object_index(self,index):
        """Trả về đối tượng điểm thứ index"""
        if self.list_object_point:
            quanlity_object_oil =  len(self.list_object_point)
            if quanlity_object_oil <= index:
                print("Không tồn tại object tại index")
                return None
            else:
                return  self.list_object_point[index]   
        else:
            print("Không tìm thấy dữ liệu nào")
            return None
    def get_object_index_area_while(self,index):
        """Trả về đối tượng điểm thứ index"""
        if self.list_object_point:
            quanlity_object_oil =  len(self.list_object_point)
            if quanlity_object_oil <= index:
                print("Không tồn tại object tại index")
                return None
            else:
                return  self.list_object_point[index]
        else:
            print("Không tìm thấy dữ liệu nào")
            return None
    def get_orig_shape(self)->tuple:
        """Trả về thông tin chiều shape của ảnh cho vào"""
        if self.data:
            try:
                # print(self.data[0].orig_shape)
                return self.data[0].orig_shape
            except Exception as e:
                print("Không tìm thấy orig_shape:", e)
                return None
        else:
            print("data khong ton tai")
    def get_boxes_data(self):
        """ trả về thông tin tất cả box của ảnh 
        boxes.xyxy : góc trên trái, góc dưới phải
        boxes.xywh Tọa độ dạng [x, y, w, h] (tâm, rộng, cao).
        boxes.xywhn  Toa do chuan hoa
        conf : độ tin cậy cho từng đối tượng
        cls: tensor([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]) Nhãn của từng đối tượng
        data: tensor(toa do x1,y1,x2,y2,do chính xác , label)
        """
        if self.data:
            try:
                # print(self.data[0].boxes)
                return self.data[0].boxes
            except Exception as e:
                print("Không tìm thấy names:", e)
                return None
        else:
            print("data khong ton tai")
    def get_data_tensor(self)->list:
        """Hàm này sẽ chứa thông tin data tọa độ x1,y1,x2,y2,do chính xác , label tra ve none neu khong co data """
        return self.data[0].boxes.data.tolist() if self.data else  None
    def get_number_object_detect_and_number_data(self)->list:
        """Trả về số lượng đối tượng phát hiện và data trả về tương ứng"""
        return list(self.data[0].boxes.shape)  if self.data else  None
    def get_xywh_data(self)->list:
        """Trả về mảng tọa độ x y w h của từng đối tượng"""
        return self.data[0].boxes.xywh.tolist()  if self.data else  None
    def get_xywhn_data(self)->list:
        """Trả về mảng tọa độ x y w h của từng đối tượng da qua chuan hoa voi chieu dai va chieu rong cua anh"""
        return self.data[0].boxes.xywhn.tolist()  if self.data else  None 
    def get_xyxy_data(self)->list:
        """Trả về mảng 2 điểm px theo tọa đô góc trên góc dưới"""
        return self.data[0].boxes.xyxy.tolist()  if self.data else  None
    def get_xyxyn_data(self)->list:
        """Trả về mảng 2 điểm chuẩn hóa theo tọa đô góc trên góc dưới"""
        return self.data[0].boxes.xyxyn.tolist()  if self.data else  None
    def get_masks(self):
        """Trả về đối tượng mark gồm nhiều dữ liệu"""
        return self.data[0].masks if self.data else  None
    def get_masks_data(self):
        """Trả về đối tượng mark gồm nhiều dữ liệu trắng đen dùng để tính diện tích 1 điểm hoặc tất cả điểm đâu"""
        return self.data[0].masks.data if self.data else  None
    def get_contourn_polygon(self):
        """Trả về đường bao xung quanh nhiều điểm dầu để quyết định vi phạm hay không"""
        return self.data[0].masks.xy if self.data else  None
    def get_contourn_polygon_standardization(self):
        """Trả về đường bao xung quanh nhiều điểm dầu chuẩn hóa để quyết định vi phạm hay không"""
        return  self.data[0].masks.xyn if self.data else  None
    def Init_Object_Oil(self,z)->bool:
        """Hàm này trả True nếu khởi tạo thành công danh sách các điểm dầu, ngược lại trả False"""
        if self.data:
            data_tensor_data = self.get_data_tensor()
            xyxyn_data  = self.get_xyxyn_data()
            contourn_polygon_data  = self.get_contourn_polygon()
            contourn_polygon_standardization_data= self.get_contourn_polygon_standardization()
            masks_data = self.get_masks_data()
            if (data_tensor_data and xyxyn_data and contourn_polygon_data and contourn_polygon_standardization_data and masks_data) is not None:
                print("---------------------------- Tiến hành khởi tạo danh sách các điểm mô hình phát hiện ----------------------------")
                number_point = self.get_number_object_detect_and_number_data() 
                self.number_point = number_point[0]
                if number_point:
                    print("Số lượng điểm phát hiện:",number_point[0])
                    for i in range(0,number_point[0]):
                        print(f"--------Khởi tạo điểm thứ {i+1}----------")
                        point = point_oil_detect(conf = data_tensor_data[i],xyxyn = xyxyn_data[i],contourn_polygon = contourn_polygon_data[i],contourn_polygon_standardization = contourn_polygon_standardization_data[i], masks_data = masks_data[i])
                        # point.draw_mark_data()  # test ham nay oke
                        # point.get_predict_point_oil()
                        # point.count_mask_max_pixels()
                        reality_w , reality_h  = point.estimate_area_with_calib(z,Manage_Point_Oil_Detect.calib_Z,Manage_Point_Oil_Detect.calib_scale)
                        point.reality_w = reality_w  #  Gia tri ngoai doi ngoài cùng
                        point.reality_h = reality_h  #  Gia tri ngoai doi khung bên ngoài cùng
                        point.reality_area = reality_w*reality_h 
                        point.area_region = point.count_mask_white_pixels()  # vung tinh toan
                        # point.scale = point.get_scale(z,Manage_Point_Oil_Detect.calib_Z,Manage_Point_Oil_Detect.calib_scale) #lay ty le
                        self.list_object_point.append(point)
                        # point_detect.area_calculate = point_detect.get_bbox_area()  diện tích vùng khung trắng bên ngoài bao vật thể 
                        # print("Số điểm khung màu trắng",point_detect.area_calculate)
                        print("Số điểm vùng màu trắng :",point.area_region)
                        print(f"Chiều dài thực tế :{point.reality_w}mm \r\nChiều cao thực tế :{point.reality_h}mm \r\nDiện tích thực tế :{point.reality_area}mm")
                    print("Khởi tạo thành công danh sách điểm dầu")
                    return True
                else:
                    print("Giá trị điểm Number point không tồn tại")
                    return False
            else:
                print("Init Point Thất bại")
                return False
        else:
            print("Dữ liệu Data Không Tồn Tại")
            return False
    def draw_all(self):
        """Hàm vẽ tất cả các điểm dầu có trong ảnh đã phát hiện đc"""
        masks = self.get_masks_data()
        if masks is not None:
            combined_mask = masks.max(dim=0)[0]   # (H, W)
            combined_mask = (combined_mask > 0).float()
            plt.imshow(combined_mask.cpu().numpy(), cmap="gray")
            plt.title("Combined Mask")
            plt.show()
        else:
            print("masks không tồn tại")
    def draw_mark_data(self)->None:  #ham oke
        """Vẽ ảnh từng điểm dầu"""
        masks = self.get_masks_data()
        mask0 = masks[0].cpu().numpy()   # chuyển sang CPU nếu dùng GPU
        mask_img = (mask0 * 255).astype(np.uint8)  # 0-255
        print(mask_img.shape, mask_img.dtype)
        if mask_img.size > 0:  # kiểm tra không rỗng
            cv2.imshow("Mask Object 0", mask_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Mask rỗng, không thể hiển thị")
        

                 

# manager = Manage_Point_Oil_Detect()
# manager.area_correction(1)
# manager.read_interp_file()

# file_path = Manage_Point_Oil_Detect.folder.create_file_in_folder_two("best.pt","model")
# img = cv2.imread(r"C:\Disk D\Project\Project\Training\img.png")
# model = YOLO(file_path)
# results = model(img)
# manager  = Manage_Point_Oil_Detect(results) 



















# print("Dữ liệu nhận được")
# print("=====================boxes====================")
# print(results[0].boxes)
# print("=====================masks====================")
# print(results[0].masks)





# manager  = Manage_Point_Oil_Detect(results) 
# manager.draw_mark_data()

# manager  = Manage_Point_Oil_Detect(results)
# manager.get_speed_detect_and_time_total()

# manager  = Manage_Point_Oil_Detect(results)
# print(manager.get_orig_shape())

# manager  = Manage_Point_Oil_Detect(results)
# print(manager.get_boxes_data())

# manager  = Manage_Point_Oil_Detect(results)
# print(manager.get_data_tensor())

# manager  = Manage_Point_Oil_Detect(results)
# manager.show_data_all_yollo()

# manager  = Manage_Point_Oil_Detect(results)
# print(manager.get_xywh_data())

# manager  = Manage_Point_Oil_Detect(results)
# print(manager.get_xywhn_data())

# manager  = Manage_Point_Oil_Detect(results)
# print(manager.get_xyxy_data())

# manager  = Manage_Point_Oil_Detect(results)
# print(manager.get_xyxyn_data())

# manager  = Manage_Point_Oil_Detect(results)
# print(manager.get_masks())


# manager  = Manage_Point_Oil_Detect(results)
# print(manager.get_contourn_polygon_standardization())

# manager  = Manage_Point_Oil_Detect(results)
# manager.draw_mark_data()

# manager  = Manage_Point_Oil_Detect(results)
# print(manager.get_number_object_detect_and_number_data())

# manager  = Manage_Point_Oil_Detect(results)
# print(manager.get_masks())

# manager  = Manage_Point_Oil_Detect(results)
# print(manager.get_contourn_polygon())

# manager  = Manage_Point_Oil_Detect(results)
# mark_data = manager.get_masks_data()
# print(mark_data)

# manager  = Manage_Point_Oil_Detect(results)
# manager.draw_all()

# manager.printdata()
# manager.get_speed_detect()
# manager.get_orig_shape()


# while_image = np.ones((480, 640, 3), dtype=np.uint8) * 255
# mark_data = manager.get_masks_data()
# print(mark_data)
# print(manager.get_orig_shape())

# mask = manager.get_boxes_data()
# print(mask)
# mark_data_circurt = manager.get_masks_data_circurt_while()
# print("Số lượng điểm phát hiện:", mark_data_circurt)   #danh sach mask
# data = manager.get_border_point_oil_object_xy()
# print(data[1]) # In ra danh sách các điểm biên
# print(mark_data)
# data = manager.get_border_point_oil_object_xyn()
# print(data[1])
# data  = manager.Init_Object_Oil()

# cv2.imshow("Test point_oil_detect", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
