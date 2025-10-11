import cv2
import func
import math
import numpy as np
from shapely.geometry import Point, Polygon
class Master_Circle_Shape():
    def __init__(self,shape):
        self.shape =  shape
        self.name = None
        self.x = None
        self.y = None
        self.r = None
        self.size_max = None
        self.size_min = None
        self.number_point =  None 
        self.init()
    def set_name(self, name: str):
        self.name = name
    # getter
    def get_name(self) -> str:
        return self.name
    def init(self):
         self.name = self.shape.get("ten_hinh_min",-1)
         print(f"--Khởi tạo master tên {self.name} type:circle--")
         self.x = self.shape.get("cx",-1)
         self.y = self.shape.get("cy",-1)
         self.r = self.shape.get("r",-1)
         self.size_max = self.shape.get("kich_thuoc_max",-1)
         self.size_min = self.shape.get("kich_thuoc_min",-1)
         self.number_point = self.shape.get("so_diem_dau",-1)
         if( self.name  == -1 or self.x ==-1 or self.y == -1 or self.r == -1 or self.size_max == -1 or  self.size_min == -1 or self.number_point == -1):
            print("Lỗi init dũ liệu hình tròn không đúng")
         else:
             print(f"--Init thành công điểm {self.name}--\n")
    def draw(self, img, color=(255, 0, 0)):
        """
        Vẽ hình tròn trực tiếp từ chính object này chỉ vẽ thôi không làm thay đổi dữ liệu
        """
        # Vẽ hình tròn
        h, w = img.shape[:2]
        cx, cy, rx = int(self.x * w), int(self.y * h),(int(self.r * w))
        cv2.circle(img,(cx,cy),rx, color, 2)
        if self.name:
            cv2.putText(img,func.remove_vietnamese_tone(self.name),
                        (cx, cy - rx - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, color, 1)
        return img
    
    
    def area(self, img_shape=None):
        """
        Tính diện tích hình tròn (pixel^2)
        - img_shape: numpy.ndarray (ảnh)
        """
        # Xác định h, w
        h, w = img_shape.shape[:2]

        # Bán kính tính theo pixel (đang scale theo width)
        r_pixel = self.r * w
        area = math.pi * (r_pixel ** 2)
        return {"area":area,"shape":"circle"}


    def contains_polygon(self, polygon, img_shape):
        """
        Kiểm tra polygon nằm trong / ngoài / một phần trong hình tròn
        - polygon: list hoặc np.ndarray Nx2 (tọa độ normalized [0-1])
        - img_shape: (H, W) hoặc numpy.ndarray (ảnh)
        Trả về dict:
        {
            "status": "inside" | "partial" | "outside",
            "inside_percent": float (0-100 % diện tích polygon nằm trong)
        }
        """
        # Lấy kích thước ảnh
        if isinstance(img_shape, np.ndarray):
            h, w = img_shape.shape[:2]
        else:
            h, w = img_shape

        # Tâm & bán kính theo pixel
        
        cx, cy = self.x * w, self.y * h
        r_pixel = self.r * w

        # Scale polygon sang pixel
        poly_pts = np.array([[x * w, y * h] for x, y in polygon], dtype=np.float64)
        poly = self.safe_polygon(poly_pts)
        # Tạo đối tượng hình học
        poly = Polygon(poly_pts)
        circle = Point(cx, cy).buffer(r_pixel, resolution=256)  
        # resolution cao hơn -> đường tròn mịn hơn

        # Diện tích giao nhau
        inter_area = poly.intersection(circle).area
        poly_area = poly.area
        inside_percent = (inter_area / poly_area * 100) if poly_area > 0 else 0

        # Xác định trạng thái
        if np.isclose(inside_percent, 100, atol=1e-3):
            status = "inside"
        elif inside_percent == 0:
            status = "outside"
        else:
            status = "partial"

        return {
            "status": status,
            "inside_percent": inside_percent
        }
    def safe_polygon(self,poly_pts):
        """
        Chuyển poly_pts (list of points) thành Polygon hợp lệ
        """
        poly = Polygon(poly_pts)
        if not poly.is_valid:
            poly = poly.buffer(0)  # sửa topology
        if poly.is_empty or poly.area == 0:
            return None
        return poly
    def get_center_and_radius(self):
        """
        Lấy tọa độ tâm và bán kính của hình tròn
        Trả về:
            {
                "x": float (normalized 0-1),
                "y": float (normalized 0-1),
                "r": float (normalized 0-1)
            }
        """
        return {
            "x": self.x,
            "y": self.y,
            "r": self.r
        }