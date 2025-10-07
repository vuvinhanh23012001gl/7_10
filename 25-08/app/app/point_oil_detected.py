import cv2
import numpy as np
class point_oil_detect:
    def __init__(self,conf=None,xyxyn=None,contourn_polygon=None, contourn_polygon_standardization = None,masks_data = None):
        """
        lớp này được tạo nhiều lần mỗi khi có dữ liệu mới cần kiểm tra
        - xywh: [x_center, y_center, width, height] (pixel)
        - xyxy: [x1, y1, x2, y2] (pixel)
        - xyxyn: [x1/W, y1/H, x2/W, y2/H]
        - xywhn: [x_center/W, y_center/H, width/W, height/H]
        - conf: độ tin cậy (float)
        """
        self.sum_area = None
        self.conf = conf
        self.xyxyn = xyxyn
        self.contourn_polygon = contourn_polygon
        self.contourn_polygon_standardization = contourn_polygon_standardization
        self.masks_data = masks_data
        
        self.scale = None
        self.reality_w = None             # Giá trị khung điểm dầu ngoài thực tế cùng
        self.reality_h = None             # Giá trị khung điểm dầu ngoài thực tế cùng
        self.reality_area = None          # Giá trị khung điểm dầu ngoài thực tế cùng

        self.area_calculate = None             # Giá trị khung điểm dầu tính toán
        self.area_region = None             # Giá trị vùng tính toán điểm dầu
  

    def check_condition_conf(self):
        return True if self.conf else False
    def check_condition_xyxyn(self):
        return True if self.conf else False
    def check_condition_contourn_polygon(self):
        return self.contourn_polygon is not None and self.contourn_polygon.size > 0
    def check_condition_contourn_polygon_standardization(self):
        return self.contourn_polygon_standardization is not None and self.contourn_polygon_standardization.size > 0

    def get_predict_point_oil(self):
        if self.check_condition_conf():
            print("ty le nhan dien diem dau",self.conf[4])
            return True
        else:
            print("Dữ liệu conf không tồn tại")

    def get_sum_area(self):
        """Hàm trả về sum arae tính theo pixel """
        return self.sum_area if self.sum_area else None

    def count_mask_max_pixels(self):
        """
        Trả về (width, height) theo pixel từ contour chuẩn hóa theo chiều dài và rộng của ảnh xuất ra ở đây là mình dùng 1920x1200
        """
        if not self.check_condition_contourn_polygon():
            print("Dữ liệu contour không tồn tại")
            return None, None
        x, y, w, h = cv2.boundingRect(self.contourn_polygon)
        # print(f"Chiều rộng (px): {w}, Chiều cao (px): {h}")
        return x, y,w, h

    def draw_mark_data(self) -> None:
        """Vẽ từng điểm dầu"""
        mask0 = self.masks_data.cpu().numpy()
        mask_img = (mask0 * 255).astype(np.uint8)  # 0-255

        # --- đếm pixel ---
        count_zero, count_one, ratio = self.count_mask_pixels(mask_img)
        print(f"Pixel 0: {count_zero}, Pixel 1: {count_one}, Tỷ lệ: {ratio:.2%}")

        # --- hiển thị ảnh ---
        if mask_img.size > 0:
            cv2.imshow("Mask Object 0", mask_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Mask rỗng, không thể hiển thị")
    def count_mask_pixels(self,mask: np.ndarray):
        """
        Đếm số pixel 0 và 1 (hoặc 0 và 255)
        Trả về: (count_zero, count_one, ratio)
        """
        height,width = mask.shape
        print(f"Kich thuoc chieu height,width la:{height},{width}")
        # Nếu mask là 255 → đổi về 1 để dễ tính toán
        if mask.max() > 1:
            binary_mask = (mask > 0).astype(np.uint8)
        else:
            binary_mask = mask.astype(np.uint8)

        count_one = int(np.sum(binary_mask))
        total = binary_mask.size
        count_zero = total - count_one
        ratio = count_one / total if total > 0 else 0
        return count_zero, count_one, ratio
    

    def estimate_area_with_calib(self, Z: int, calib_Z: list, calib_scale: list):
        """
        Tính diện tích thật (tương đối) từ mask và Z
        Trả về kích thước (w, h) với 1 chữ số thập phân
        """
        x, y, w, h = self.count_mask_max_pixels()
        scale = np.interp(Z, calib_Z, calib_scale)
        reality_w = round(w * scale, 1)
        reality_h = round(h * scale, 1)
        return reality_w, reality_h
    def get_scale(self,Z:int,calib_Z:list,calib_scale:list):
        scale = np.interp(Z, calib_Z, calib_scale)
        return scale
    def count_mask_white_pixels(self, width=1920, height=1200):
        if not self.check_condition_contourn_polygon():
            print("Dữ liệu contour không tồn tại")
            return 0

        if self.contourn_polygon is None or len(self.contourn_polygon) == 0:
            print("Contour rỗng")
            return 0

        mask = np.zeros((height, width), dtype=np.uint8)
        contour_int = np.array(self.contourn_polygon, dtype=np.int32)
        cv2.drawContours(mask, [contour_int], -1, color=255, thickness=-1)
        white_pixels = cv2.countNonZero(mask)
        # cv2.imshow("Processing IMG",mask)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return white_pixels
    def estimate_area_while_with_calib(self,Z:int,calib_Z:list,calib_scale:list):
        """
        Tính diện tích thật (tương đối) từ mask và Z
        """
        area_white = self.count_mask_white_pixels()
        scale = np.interp(Z, calib_Z, calib_scale)
        return area_white * scale
    def get_bbox_area(self):
        """
        Tính diện tích bounding box (px²) bao ngoài contour
        """
        if not self.check_condition_contourn_polygon():
            print("Dữ liệu contour không tồn tại")
            return None

        x, y, w, h = cv2.boundingRect(self.contourn_polygon)
        return w * h
    def to_dict_need_data(self):
        """
        Trả về dictionary chứa toàn bộ thông tin vùng tính toán và thực tế
        """
        return {
            "area_reality": self.reality_area,
            "area_calculate": self.area_calculate,
        }
    # def get_conf(self):
    #     print("Contour border xy:", self.contour_border_xy)
    #     return self.contour_border_xy
    # def get_contour_border_xyn(self):
    #     print("Contour border xyn:", self.contour_border_xyn)
    #     return self.contour_border_xyn
    # def get_fill_mask(self):
    #     print("Fill mask:", self.fill_mask)
    #     return self.fill_mask
    # def get_area_pixel(self):
    #     x1, y1, x2, y2 = self.xyxy
    #     width = max(0, x2 - x1)
    #     height = max(0, y2 - y1)
    #     return width * height
    # def draw_on_image(self, img):
    #     print(self.xyxy)
    #     if img is not None and self.xyxy is not None:
    #         x1, y1, x2, y2 = self.xyxy

    #         # Ép kiểu rõ ràng
    #         x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

    #         color = (0, 255, 0)  # Màu xanh lá
    #         thickness = 1

    #         print("Rectangle:", x1, y1, x2, y2)
    #         cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)

    #     else :
    #         print("❌ Không thể vẽ lên ảnh: img hoặc xyxy không hợp lệ") 
    #         return False
    # def get_center_pixel(self):
    #     """Trả về tọa độ tâm (x_center, y_center) dạng pixel"""
    #     return tuple(self.xywh[:2])

    # def get_box_normalized(self):
    #     """Trả về [x_center, y_center, width, height] đã chuẩn hóa"""
    #     return self.xywhn
    # def __str__(self):
    #     return f"xywh:{self.xywh}\n xyxy:{self.xyxy} \nxyxyn:{self.xyxyn}\n xywhn:{self.xywhn}\n"
    # def draw_fill_mask(self, img, mask_color=(0, 255, 0), alpha=0.4):
    #     pass
        
    # def draw_contour_border_xy(self, img, img_height, img_width, contour_color=(255, 0, 0), thickness=1):
    #     """
    #     Vẽ contour từ danh sách các điểm (self.contour_border_xy) lên ảnh.
    #     """
    #     if img is None:
    #         print("❌ Ảnh không hợp lệ.")
    #         return False

    #     # Fix lỗi: không dùng `not` với array
    #     if self.contour_border_xy is None or len(self.contour_border_xy) == 0:
    #         print("⚠️ Không có contour_border_xy để vẽ.")
    #         return False

    #     try:
    #         # Chuẩn hóa và kiểm tra giới hạn điểm
    #         valid_points = []
    #         for point in self.contour_border_xy:
    #             x, y = map(int, point)
    #             if 0 <= x < img_width and 0 <= y < img_height:
    #                 valid_points.append([x, y])
    #             else:
    #                 print(f"⚠️ Điểm ({x},{y}) vượt ngoài kích thước ảnh.")

    #         if len(valid_points) < 3:
    #             print("❌ Không đủ điểm hợp lệ để tạo contour.")
    #             return False

    #         contour = np.array(valid_points, dtype=np.int32).reshape((-1, 1, 2))
    #         cv2.drawContours(img, [contour], contourIdx=-1, color=contour_color, thickness=thickness)
    #         return True

    #     except Exception as e:
    #         print(f"❌ Lỗi khi vẽ contour: {e}")
    #         return False
    # def draw_contour_border_xyn(self, img, img_height, img_width, contour_color=(255, 0, 0), thickness=1):
    #     """
    #     Vẽ contour từ tọa độ chuẩn hóa (self.contour_border_xyn) lên ảnh gốc.
    #     - img: ảnh gốc (numpy array)
    #     - img_height, img_width: kích thước ảnh
    #     - contour_color: màu vẽ (BGR)
    #     - thickness: độ dày nét vẽ
    #     """

    #     if img is None:
    #         print("❌ Ảnh không hợp lệ.")
    #         return False

    #     if self.contour_border_xyn is None or len(self.contour_border_xyn) == 0:
    #         print("⚠️ Không có contour_border_xyn để vẽ.")
    #         return False

    #     try:
    #         valid_points = []
    #         for x_norm, y_norm in self.contour_border_xyn:
    #             x = int(x_norm * img_width)
    #             y = int(y_norm * img_height)

    #             if 0 <= x < img_width and 0 <= y < img_height:
    #                 valid_points.append([x, y])
    #             else:
    #                 print(f"⚠️ Điểm chuẩn hóa ({x_norm:.4f}, {y_norm:.4f}) → ({x},{y}) vượt ngoài kích thước ảnh.")

    #         if len(valid_points) < 3:
    #             print("❌ Không đủ điểm hợp lệ để tạo contour.")
    #             return False

    #         contour = np.array(valid_points, dtype=np.int32).reshape((-1, 1, 2))
    #         cv2.drawContours(img, [contour], contourIdx=-1, color=contour_color, thickness=thickness)
    #         return True

    #     except Exception as e:
    #         print(f"❌ Lỗi khi vẽ contour chuẩn hóa: {e}")
    #         return False
    # def draw_xyxy_box(self, img, color=(0, 255, 0), thickness=2, label=None):
    #     """
    #     Vẽ hình chữ nhật lên ảnh từ tọa độ xyxy: [x1, y1, x2, y2]
    #     - img: ảnh gốc (numpy array)
    #     - self.xyxy: list hoặc tuple [x1, y1, x2, y2]
    #     - color: màu vẽ (BGR), mặc định xanh lá
    #     - thickness: độ dày đường viền
    #     - label: chuỗi chữ để hiển thị bên trên (nếu có)
    #     """

    #     # Lấy kích thước ảnh
    #     h, w = img.shape[:2]

    #     # Lấy tọa độ box, ép kiểu int
    #     x1, y1, x2, y2 = map(int, self.xyxy)

    #     # Giới hạn trong phạm vi ảnh (clip)
    #     x1, y1 = max(0, x1), max(0, y1)
    #     x2, y2 = min(w - 1, x2), min(h - 1, y2)

    #     # Vẽ hình chữ nhật
    #     cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)

    #     # Nếu có label thì thêm vào
    #     if label:
    #         font = cv2.FONT_HERSHEY_SIMPLEX
    #         font_scale = 0.5
    #         font_thickness = 1

    #         # Lấy kích thước chữ
    #         text_size, _ = cv2.getTextSize(label, font, font_scale, font_thickness)
    #         text_w, text_h = text_size

    #         # Đảm bảo label không bị vẽ ra ngoài ảnh (sát viền trên)
    #         y1_label = max(y1, text_h + 4)

    #         # Vẽ nền chữ (filled rectangle)
    #         cv2.rectangle(img,
    #                     (x1, y1_label - text_h - 4),
    #                     (x1 + text_w, y1_label),
    #                     color, -1)

    #         # Vẽ chữ màu trắng
    #         cv2.putText(img, label,
    #                     (x1, y1_label - 2),
    #                     font, font_scale,
    #                     (255, 255, 255),
    #                     font_thickness,
    #                     cv2.LINE_AA)

    #     return img

    # def area_of_oil(self):
    #     if self.fill_mask is not None and self.fill_mask.numel() > 0:
    #         # sum  = 0
    #         # print("seoomasssssssssssssssssssssssssssssssssssssssssssssssss",len(self.fill_mask))
    #         # for i in self.fill_mask:
    #         #     print(f"Phan tu:{i} \n")
    #         #     for j in i:
    #         #         print(j)
    #         # print(self.fill_mask.cpu())
    #         # sum = 0
    #         # for i in self.fill_mask:
    #         #     for j in i:
    #         #         if(int(j)!=0):
    #         #             sum = sum +1
                        
                
        
    #         # print(self.fill_mask[678])
    #         nn = np.array(self.fill_mask * 255, dtype=np.uint8)
    #         new_size = (1920,1200)  # (width, height)
    #         resized_nn = cv2.resize(nn, new_size, interpolation=cv2.INTER_NEAREST)
    #         sum = 0
    #         for i in resized_nn:
    #             for j in i:
    #                 if(int(j)==255):
    #                     sum  = sum + 1
    #         print(sum)
    #         cv2.imshow("kk", resized_nn)
    #         cv2.waitKey(0)
    #         # for i in self.fill_mask:
    #         #      print(f"Phan tu:{i} \n")
           
            
            
            
    #     else:
    #         print("Không có mask điểm")
        
# # import cv2
# # import numpy as np
# img = np.ones((480, 640, 3), dtype=np.uint8) * 255
# # # Giả lập 1 bounding box phát hiện
# # # [x1, y1, x2, y2, conf, cls_id]
# raw = [100, 150, 200, 250, 0.89, 0]  # box 100x100
# xywh = [150, 200, 100, 100]          # tâm (150,200), w=100, h=100
# xyxyn = [100/640, 150/480, 200/640, 250/480]
# xywhn = [150/640, 200/480, 100/640, 100/480]
# conf = 0.89
# cls_id = 0

# box = point_oil_detect(raw, xywh, xyxyn, xywhn, conf, cls_id)
# # # # Vẽ đối tượng lên ảnh
# # box.draw_on_image(img)
# # # Hiển thị ảnh
# box.draw_on_image(img)
# cv2.imshow("Test Box", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# # print("Tâm pixel:", box.get_center_pixel())
# # print("Box normalized:", box.get_box_normalized())
# ----------------------------------------------------------------------------------------------------------------------------------------

# def draw_mask_and_contour_on_image(point, img, mask_color=(0, 0, 255), contour_color=(255, 0, 0), alpha=0.4):
#     overlay = img.copy()

#     if point.fill_mask is not None and point.fill_mask.dtype == bool:
#         mask = point.fill_mask.astype(np.uint8) * 255
#         color_mask = np.zeros_like(img)
#         color_mask[:, :] = mask_color
#         overlay = np.where(mask[:, :, None], (1 - alpha) * overlay + alpha * color_mask, overlay).astype(np.uint8)

#     if point.contour_border_xy:
#         try:
#             contour = np.array(point.contour_border_xy, dtype=np.int32).reshape(-1, 1, 2)
#             cv2.drawContours(overlay, [contour], -1, contour_color, 1)
#         except Exception as e:
#             print("Lỗi khi vẽ contour:", e)

#     img[:, :] = overlay
#     return img

# # ---------------------------------------------
# # Tạo dữ liệu test
# # ---------------------------------------------
# img = np.ones((300, 300, 3), dtype=np.uint8) * 255  # ảnh trắng

# # Bounding box: từ (80, 80) đến (220, 220)
# xyxy = [80, 80, 220, 220]
# x1, y1, x2, y2 = xyxy
# width = x2 - x1
# height = y2 - y1
# xywh = [x1 + width // 2, y1 + height // 2, width, height]

# img_h, img_w = img.shape[:2]
# xyxyn = [x1 / img_w, y1 / img_h, x2 / img_w, y2 / img_h]
# xywhn = [xywh[0] / img_w, xywh[1] / img_h, width / img_w, height / img_h]

# # Fill mask: hình vuông nhỏ nằm trong bounding box
# fill_mask = np.zeros((img_h, img_w), dtype=bool)
# fill_mask[100:200, 100:200] = True

# # Contour: đường viền vuông ngoài của fill mask
# contour_border_xy = [(100, 100), (200, 100), (200, 200), (100, 200)]

# # ---------------------------------------------
# # Khởi tạo object point_oil_detect
# # ---------------------------------------------
# point = point_oil_detect(
#     xywh=xywh,
#     xyxy=xyxy,
#     xyxyn=xyxyn,
#     xywhn=xywhn,
#     fill_mask=fill_mask,
#     contour_border_xy=contour_border_xy,
#     contour_border_xyn=None,
#     conf=0.9,
#     cls_id=1
# )

# # ---------------------------------------------
# # Vẽ kết quả lên ảnh
# # ---------------------------------------------
# point.draw_on_image(img)
# # draw_mask_and_contour_on_image(point, img)
# point.draw_fill_mask(img, mask_color=(0, 0, 255), alpha=0.4)
# point.draw_contour_border_xy(img,1920,1200, contour_color=(255, 0, 0), thickness=1)
# # ---------------------------------------------
# # Hiển thị kết quả
# # ---------------------------------------------
# cv2.imshow("Test point_oil_detect", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()