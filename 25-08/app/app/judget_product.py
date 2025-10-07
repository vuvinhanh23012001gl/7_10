
from point_oil_detected_manage import Manage_Point_Oil_Detect
from ultralytics import YOLO
from folder_create import Create
from master_circle_shape import  Master_Circle_Shape
from master_rect_shape import  Master_Rect_Shape
from process_master import Proces_Shape_Master
import numpy as np
import cv2
class Judget_Product:
    """Lớp này chỉ phán định sản phẩm có 
    lớp này chỉ khởi tạo 1 lần
    OK hay NG"""

    folder =  Create()
    file_path = folder.create_file_in_folder_two("best.pt","model")
    img = np.zeros((640,480,3),dtype= np.uint8)
    model = YOLO(file_path)
    model(img)

    def __init__(self):
        pass
    def judget_img(self,atitude_z,index_picture,img:np.ndarray,data_one_point_master):
                # ✅ Kiểm tra giá trị đầu vào
                if img is None:
                    print(f"Lỗi: Ảnh đầu vào None tại index_picture: {index_picture}")
                    return False

                if atitude_z is None:
                    print("Lỗi: Giá trị atitude_z None")
                    return False

                if index_picture is None:
                    print("Lỗi: index_picture None")
                    return False
            # ========================= BẮT ĐẦU XỬ LÝ ========================= #
                """Khi cho 1 bức ảnh vào thì nó sẽ phán định ok hay ng"""
                print("data_one_point_master sau",data_one_point_master)
            
                data_regulation = Judget_Product.model(img)                                                  # Dữ liệu đi ra từ mô hình 
                object_one_point_detect = Manage_Point_Oil_Detect(data_regulation,atitude_z)                 # Đưa vào đối tượng điểm của mô hình
                polygons = object_one_point_detect.get_contourn_polygon_standardization()                    # Lấy các điểm bao 
                if not polygons:
                    print(f"Không có điểm dầu hoặc không phát hiện điểm dầu trong ảnh thứ:{index_picture} của")
                    #Phan nay cần phải thêm Logic xem điểm dầu hợp lệ hay không
                # object_one_point_detect.draw_all()                                                         # Vẽ các điểm dầu
                # print(data_one_point_master)
                # img = self.draw_polylines_on_image(img,polygons)   
                arr_object_shape = [] 
                if not data_one_point_master:
                    print("Dữ liệu không đúng")
                    return False                 
                for shape in data_one_point_master:
                    if shape["type"] == "circle":
                        shape_object = Master_Circle_Shape(shape)
                                #  img  = shape_object.draw(img)
                        arr_object_shape.append(shape_object)
                    elif shape["type"] == "rect":
                        shape_object = Master_Rect_Shape(shape)
                                #  img  = shape_object.draw(img)
                        arr_object_shape.append(shape_object)
                is_frame_ok = True
                for shape_master in arr_object_shape:
                     arr_specified_size_data = []
                    #  img  = shape_master.draw(img)
                     name = shape_master.get_name()
                     data_area = shape_master.area(img)
                     print(f"------------------------Kiểm tra vùng  Master:{name}-------------------------------")
                     is_inside = True         
                     index_detect_point = 0
                     count_oil_in_point = 0
                     for poly in polygons:   
                        object_point = object_one_point_detect.get_object_index_area_while(index_detect_point) #Trả về đối tượng từng điểm ảnh phát hiện đc
                        index_detect_point += 1
                        dict_data_detect = shape_master.contains_polygon(poly, img)
                        status = dict_data_detect.get("status",-1)
                        inside_percent = dict_data_detect.get("inside_percent",-1)
                        if inside_percent == -1 or status == -1:
                            print("Lỗi dữ liệu output")
                        if status == "inside":
                            print(f"--Thuộc tính điểm thứ {count_oil_in_point + 1} phát hiện ra--")
                            width_reality = max(object_point.estimate_area_with_calib(atitude_z,object_one_point_detect.calib_Z,object_one_point_detect.calib_scale))
                            print("--Vật thể")
                            print(f"Khung {name} có điểm {count_oil_in_point + 1} max đường kính thực tế của vật thể :{width_reality} mm")
                            print(f"Khung {name} có điểm {count_oil_in_point + 1} số px trắng phát hiện là :{object_point.count_mask_white_pixels()} px")
                            print("--Master quy định")
                            print(f"Kích thước điểm dầu MIN :{shape_master.size_min} MAX: {shape_master.size_max}")
                            if(width_reality >shape_master.size_max or width_reality < shape_master.size_min):
                                specified_size_data = {"name_master":name,"name_point":count_oil_in_point + 1}
                                arr_specified_size_data.append(specified_size_data)
                            print(f"Khung {name} có điểm {count_oil_in_point + 1} master quy định nằm trong hình:{data_area["shape"]} có diện tích khung là:{data_area["area"]} px")
                            print("Phán định")
                            print(f"Tỷ lệ chiếm của điểm {count_oil_in_point + 1} với khung master :{self.calc_area_percentage(object_point.count_mask_white_pixels(),data_area["area"])} %")
                            print(f"{inside_percent} % nằm trọn trong khung")
                            print(f"==> Điểm {count_oil_in_point + 1} nằm trong khung {name}")
                            count_oil_in_point +=1
                            is_inside =  True
                        if status == "partial":
                             print(f"Khung {name} phát hiện {inside_percent} % nằm một phần trong khung")
                     if not is_inside:
                        print(f"Hình {name} có không có Polygon nằm trong")
                     print(f"Khung {name} số lượng điểm phát hiện nằm trong là :{count_oil_in_point} và master đặt là:{shape_master.number_point}")
                     if count_oil_in_point != shape_master.number_point:
                         print(f"=>Số lượng điểm phát hiện khác với quy định")
                         is_frame_ok =  False
                     else:
                          print(f"=>Số lượng điểm phát hiện giống với quy định")
                          if len(arr_specified_size_data) > 0:
                              print("Tìm được những điểm dầu sau không đúng với kích thước quy định",arr_specified_size_data)
                              is_frame_ok =  False
                     print("------------------------END master-------------------------------")
                if is_frame_ok:
                     print("=======================> Bức Hình OK")
                else:
                     print("=======================> Bức Hình NG")
                # cv2.imshow("Processing IMG",img)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
        
    def judget(self,atitude_z,img:np.ndarray,data_one_point_master):
            """Khi cho 1 bức ảnh vào thì nó sẽ 
            phán định ok hay ng
            hàm này để test phán định
            """
            data_model_output = Judget_Product.model(img)                                              # Dữ liệu đi ra từ mô hình 
            object_frame_detect = Manage_Point_Oil_Detect(data_model_output,atitude_z)                 # Đưa vào đối tượng điểm của mô hình
            # object_frame_detect.draw_all()
            polygons = object_frame_detect.get_contourn_polygon_standardization()                    # Lấy các điểm bao 
            img = self.draw_polylines_on_image(img,polygons)   
            arr_shape_master = self.setting_object_master(data_one_point_master,img)
            data_send_detect,is_frame_ok = self.process_judment(object_frame_detect,img,atitude_z,polygons,arr_shape_master)
            # self.show_image(img)
            return data_send_detect,img,is_frame_ok

    def setting_object_master(self,data_one_point_master,img=None):  
        """Hàm này setting các đối tượng điểm master 
        Input  :đầu vào là dữ liệu 1 frame master và tiến hành vẽ dữ liệu master trực tiếp lên ảnh
        Output :đầu ra là 1 arr hình kiểu hình vuông và hình tròn
        """
        print("-----------------------Khởi tạo master-----------------------")
        arr_object_shape = [] 
        if not data_one_point_master:
            print("Dữ liệu không đúng")
            return False       
        for shape in data_one_point_master:
            type_shape = shape.get("type",-1)
            if type_shape == "circle":
                shape_object = Master_Circle_Shape(shape) #  
                img  = shape_object.draw(img)
                arr_object_shape.append(shape_object)
            elif type_shape == "rect":
                shape_object = Master_Rect_Shape(shape)
                arr_object_shape.append(shape_object)   # 
                img  = shape_object.draw(img)
        print("Khởi tạo thành công Master")
        return arr_object_shape
    def process_judment(self,object_frame_detect,img,atitude_z,polygons,arr_shape_master):
        print("-----------------------Bắt đầu phán định-----------------------")
        data_send_server_judgement = {}
        is_frame_ok =  True

        for index,shape_master in enumerate(arr_shape_master):
                count_oil_point_avaiable = 0
                count_oil_points_inside_master = 0
                # area_master = shape_master.area(img)
                name_master = shape_master.get_name()
                index_point_detect = 0
                # print(name_master)
                arr_point_detect_send_server = []
                for poly in polygons:    
                            object_point = object_frame_detect.get_object_index_area_while(index_point_detect) #Trả về đối tượng từng điểm ảnh phát hiện đc  print(object_point)
                            index_point_detect+=1
                            dict_data_detect = shape_master.contains_polygon(poly,img)                    # Trả về các phán định thuộc tính của các điểm nhận đc 
                            status_detect_shape = dict_data_detect.get("status",-1)  
                            inside_percent = dict_data_detect.get("inside_percent",-1)
                            # print(dict_data_detect)
                            if status_detect_shape == "inside":
                                # print(f"Số px trắng phát hiện là :{object_point.count_mask_white_pixels()} px")
                                # print(f"Quy ra mm :{object_point.estimate_area_while_with_calib(atitude_z,object_frame_detect.calib_Z,object_frame_detect.calib_scale)}mm")
                                # occupancy_rate = self.calc_area_percentage(object_point.count_mask_white_pixels(),area_master["area"])
                                # print(f"Tỷ lệ chiếm trong khung master:{occupancy_rate} %")
                                width_reality = object_point.estimate_area_with_calib(atitude_z,object_frame_detect.calib_Z,object_frame_detect.calib_scale)
                                take_max_width_or_height = max(width_reality[0],width_reality[1])
                                print(f"--Điểm:{index_point_detect} nằm trong khung master:{name_master}--")
                                print(f"Điểm phát hiện {index_point_detect} Chiều dài {width_reality[0]} mm Chiều rộng {width_reality[1]} mm")
                                count_oil_points_inside_master += 1
                                properties_oil = self.create_properties_oil(index_point_detect,width_reality,inside_percent,True)
                                arr_point_detect_send_server.append(properties_oil)
                    
                                if(take_max_width_or_height <= shape_master.size_max and  take_max_width_or_height >= shape_master.size_min):
                                    print(f"Điểm phát hiện {index_point_detect} có size hợp lệ MIN:{shape_master.size_min} Thực tế:{take_max_width_or_height} MAX:{shape_master.size_max}")
                                    count_oil_point_avaiable += 1
                            elif status_detect_shape == "partial":
                                width_reality = object_point.estimate_area_with_calib(atitude_z,object_frame_detect.calib_Z,object_frame_detect.calib_scale)
                                take_max_width_or_height = max(width_reality[0],width_reality[1])
                                print(f"--Điểm phát hiện {index_point_detect} nằm trên viền khung Master {name_master}--")
                                print(f"Điểm phát hiện {index_point_detect} Chiều dài {width_reality[0]} mm Chiều rộng {width_reality[1]} mm")
                                print(f"Không xét size điểm {index_point_detect}")
                                properties_oil = self.create_properties_oil(index_point_detect,width_reality,inside_percent,False)
                                arr_point_detect_send_server.append(properties_oil)
                               
                data_send_server_judgement.update({ 
                    f"{index}":{
                    "name_master":name_master,
                    "number_point":shape_master.number_point,
                    "max_point":shape_master.size_max,
                    "min_point":shape_master.size_min,
                    "arr_pointr":arr_point_detect_send_server
                    }
                })
                
                check_all_point = False
                check_size_point = False
                statuse_check_number_oil_in_master = self.check_number_oil_inside_master(shape_master.number_point,count_oil_points_inside_master)
                if not statuse_check_number_oil_in_master :
                    print(f"Tổng số điểm nằm trong master quy định {shape_master.number_point},Tổng số điểm nằm trong hợp lệ {count_oil_points_inside_master}==>NG")
                else :
                    check_all_point = True
                print("count_oil_points_inside_master",count_oil_points_inside_master,"count_oil_point_avaiable",count_oil_point_avaiable)
                statuse_check_size_oil_in_master  = self.check_number_oil_inside_master(count_oil_points_inside_master,count_oil_point_avaiable)
                if not statuse_check_size_oil_in_master:
                    print(f"Tổng số size đúng master {shape_master.number_point},Tổng số size đúng hợp lệ{count_oil_point_avaiable}==>NG")
                else :
                    check_size_point = True
                if check_all_point and check_size_point:
                     print(f"Master {name_master} OK")
                else:
                    if not  check_all_point:
                            is_frame_ok = False
                            print(f"Master {name_master} lỗi do số điểm")
                    if not check_size_point :
                            is_frame_ok = False
                            print(f"Master {name_master} lỗi do size ")
                    print(f"Master {name_master} NG")
                     
        # print(data_send_server_judgement)
        # import json
        # json_str = json.dumps(data_send_server_judgement, ensure_ascii=False, indent=4,
        #               default=lambda x: float(x) if isinstance(x, np.floating) else x)

        # print(json_str)
        if is_frame_ok:
            print("=====>>  OK") 
        else:
            print("=====>>  NG")  
        print("-----------------------Kết thúc phán định-----------------------")
        return data_send_server_judgement,is_frame_ok
    def create_properties_oil(self,index_point_detect, width_reality, inside_percent, status_oil: bool):
        """
        Trả về dict properties_oil.
        - status_oil: True => "OK", False => "NG"
        """
        return {
            "name": f"Point{index_point_detect}",
            "width_reality": width_reality[0],
            "height_reality": width_reality[1],
            "inside_percent": inside_percent,   # Phần trăm nằm trọn master
            "status_oil": "OK" if status_oil else "NG"
        }
    def check_len_list(self, number_point, list_data):
        print(number_point)
        print(len(list_data))
        # Kiểm tra kiểu dữ liệu và giá trị
        if not isinstance(number_point, int):
            return False
        if number_point <= 0:
            return False
        if not isinstance(list_data, list):
            return False
        return len(list_data) == number_point
    def check_number_oil_inside_master(self, number_point, master_point):
        # Kiểm tra kiểu dữ liệu và giá trị > 0
        """Kiểm tra 2 số int có bằng nhau hay không nếu khác nhau trả về False nếu bằng nhau tra về True"""
        if not (isinstance(number_point, int) and isinstance(master_point, int)):
            return False
        if number_point <= 0 or master_point <= 0:
            return False

        # So sánh
        return number_point == master_point
    
          
   
    def show_image(self,img, window_name="Processing IMG"):
        """
        Hiển thị một ảnh và chờ nhấn phím bất kỳ để đóng cửa sổ.
        :param img: Ảnh dạng numpy array (BGR).
        :param window_name: Tên cửa sổ hiển thị.
        """
        cv2.imshow(window_name, img)
        cv2.waitKey(0)           # 0 nghĩa là chờ vô hạn cho tới khi nhấn phím
        cv2.destroyAllWindows()  # Đóng tất cả cửa sổ

    def show_infor_send_server(self,object_point:None,atitude_z:None,calib_Z:None,calib_scale:None,inside_percent:None,status_point:None,name_master=None):
        dict_data_send = {}
        shape_obj_reality = object_point.estimate_area_with_calib(atitude_z,calib_Z,calib_scale)
        dict_data_send["shape_obj_detect"] = shape_obj_reality
        dict_data_send["inside_percent"] = inside_percent
        dict_data_send["status_point"] = status_point
        dict_data_send["name_master"] =  name_master
        print(dict_data_send)
    def calc_area_percentage(self,area_shape, area_frame):
        """
        Tính tỷ lệ % diện tích của hình so với diện tích khung
        - area_shape: diện tích của hình
        - area_frame: diện tích khung (lớn hơn 0)
        """
        if area_frame <= 0:
            raise ValueError("Diện tích khung phải lớn hơn 0")

        percent = (area_shape / area_frame) * 100
        return percent

    def draw_polylines_on_image(self, image, polygons=None):
        """
        image: numpy array (H, W, 3) ảnh RGB
        polygons: list các contour (numpy array Nx2) giá trị normalized [0-1]
        """
        h, w = image.shape[:2]
        result = image.copy()

        if polygons is not None:
            for idx, poly in enumerate(polygons, start=1):
                # Chuyển normalized -> pixel
                pts = np.array([[int(x * w), int(y * h)] for x, y in poly], dtype=np.int32)
                pts = pts.reshape((-1, 1, 2))

                # Vẽ đường polygon
                cv2.polylines(result, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

                # Tính tâm polygon (centroid)
                centroid = np.mean(pts.reshape(-1, 2), axis=0).astype(int)
                cx, cy = centroid

                # Ghi số thứ tự (1,2,3,...)
                cv2.putText(result, str(idx), (cx, cy),
                            cv2.FONT_HERSHEY_SIMPLEX,   # font
                            1,                          # scale
                            (0, 0, 255),                # màu đỏ
                            2,                          # độ dày
                            cv2.LINE_AA)
        return result
       
    
# index_picture  =  4
# PATH_MODEL = r"C:\Users\anhuv\Desktop\26_08\25-08\app\app\static\Master_Photo\Master_SP01\img_4.png"  
# img = cv2.imread(PATH_MODEL)  
# class_regulation = Proces_Shape_Master()
# master_one_frame =  class_regulation.get_data_shape_of_location_point("SP01",index_picture)
# print(master_one_frame)
# judget1 = Judget_Product()
# print(f"Phán định tại Index:{index_picture}")
# judget1.judget(2,img,master_one_frame)






