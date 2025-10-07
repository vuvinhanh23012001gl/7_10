import cv2
import func
import numpy as np
class Master_Rect_Shape:
    def __init__(self,shape):
        """
        Đại diện 1 hình chữ nhật
        - (x1, y1): góc trên trái
        - (x2, y2): góc dưới phải
        """
        self.shape = shape
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.corners = None
        self.name = None
        self.rotation =  None
        self.size_max = None
        self.size_min = None
        self.compatible_max = None
        self.compatible_min = None
        self.Init()
    def set_name(self, name: str):
        self.name = name
    # getter
    def get_name(self) -> str:
        return self.name
    def draw(self, img, color=(255, 0, 0)):
        h, w = img.shape[:2]

        if self.corners and self.corners != -1:
            # Lấy 4 điểm corners (chuẩn hóa -> pixel)
            pts = np.array([[int(c["x"] * w), int(c["y"] * h)] for c in self.corners], dtype=np.int32)

            # Vẽ polygon từ corners
            cv2.polylines(img, [pts], isClosed=True, color=color, thickness=2)
           

            # Tính tâm polygon
            cx, cy = np.mean(pts, axis=0).astype(int)
            # Vẽ tên tại đỉnh đầu tiên
            cv2.putText(img, func.remove_vietnamese_tone(self.name), (cx-10, cy-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            return img
        else:
            # Vẽ bounding box nếu không có corners
            x1, y1 = int(self.x1 * w), int(self.y1 * h)
            x2, y2 = int(self.x2 * w), int(self.y2 * h)
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(img, func.remove_vietnamese_tone(self.name), (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            return img
    def Init(self):
        self.name = self.shape.get("ten_hinh_min",-1)
        print(f"--Khởi tạo master tên {self.name} type:rect--")
        self.x1 = self.shape.get("x1",-1)
        self.y1 = self.shape.get("y1",-1)
        self.x2 = self.shape.get("x2",-1)
        self.y2 = self.shape.get("y2",-1)
        self.corners = self.shape.get("corners",-1)
        
        self.rotation = self.shape.get("rotation",None)

        self.size_max = self.shape.get("kich_thuoc_max",-1)
        self.size_min = self.shape.get("kich_thuoc_min",-1)

        self.number_point = self.shape.get("so_diem_dau",-1)

        if(self.corners == -1):
            print(f"Không xoay")
        else:
            print(f"Bị xoay hình")
        if( self.name  == -1 or self.x1 ==-1 or self.y1 == -1 or self.x2  == -1 or self.y2   == -1 or self.size_max  == -1 or self.size_min  == -1 or  self.number_point == -1):
            print("Lỗi init dũ liệu hình vuông không đúng")
        else:
            print(f"--Init thành công điểm {self.name}--\n")
    def area(self, img_shape=None):
        """
        Tính diện tích hình chữ nhật (pixel^2)
        - img_shape: (height, width) hoặc numpy.ndarray (ảnh)
        """
        # Xác định h, w từ tham số truyền vào
        if isinstance(img_shape, np.ndarray):          # Nếu truyền vào cả ảnh
            h, w = img_shape.shape[:2]
        elif isinstance(img_shape, (tuple, list)):     # Nếu truyền vào tuple (h, w)
            h, w = img_shape
        else:                                          # Nếu không truyền gì
            h, w = (1, 1)

        # Nếu có corners (hình xoay / polygon)
        if self.corners and self.corners != -1:
            pts = np.array(
                [[int(c["x"] * w), int(c["y"] * h)] for c in self.corners],
                dtype=np.float32
            )
            x = pts[:, 0]
            y = pts[:, 1]
            area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
            return {"area":area,"shape":"rect"}
        else:
            # Bounding box không xoay
            x1, y1 = int(self.x1 * w), int(self.y1 * h)
            x2, y2 = int(self.x2 * w), int(self.y2 * h)
            area = abs((x2 - x1) * (y2 - y1))

            return {"area":area,"shape":"rect"}
    
    def contains_polygon(self, polygon, img_shape):
        """
        Kiểm tra polygon nằm trong / ngoài / một phần trong hình chữ nhật
        - polygon: list hoặc np.ndarray Nx2 (tọa độ normalized [0-1])
        - img_shape: (H, W) hoặc numpy.ndarray (ảnh)

        Trả về dict:
        {
            "status": "inside" | "partial" | "outside",
            "inside_percent": float  (0-100 % polygon nằm trong)
        }
        """
        import numpy as np
        import cv2

        # Lấy kích thước ảnh
        if isinstance(img_shape, np.ndarray):
            h, w = img_shape.shape[:2]
        else:
            h, w = img_shape

        # Nếu có corners (rect xoay)
        if self.corners and self.corners != -1:
            rect_pts = np.array(
                [[int(c["x"] * w), int(c["y"] * h)] for c in self.corners],
                dtype=np.int32
            ).reshape((-1, 1, 2))
        else:
            x1, y1 = int(self.x1 * w), int(self.y1 * h)
            x2, y2 = int(self.x2 * w), int(self.y2 * h)
            rect_pts = np.array(
                [[x1, y1], [x2, y1], [x2, y2], [x1, y2]],
                dtype=np.int32
            ).reshape((-1, 1, 2))

        # Scale polygon sang pixel
        poly_pts = np.array([[int(x * w), int(y * h)] for x, y in polygon])

        # Kiểm tra từng điểm của polygon có nằm trong rect không
        inside_count = 0
        for pt in poly_pts:
            inside = cv2.pointPolygonTest(rect_pts, (float(pt[0]), float(pt[1])), False)
            if inside >= 0:
                inside_count += 1

        inside_percent = inside_count / len(poly_pts) * 100

        # Quyết định trạng thái
        if inside_percent == 100:
            status = "inside"
        elif inside_percent == 0:
            status = "outside"
        else:
            status = "partial"

        return {
            "status": status,
            "inside_percent": inside_percent
        }
