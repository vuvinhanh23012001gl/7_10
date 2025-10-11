import cv2
import time
from datetime import datetime
import base64
from pypylon import pylon
from folder_create import Create
from shared_queue import process_capture_detect
import threading
import traceback
import os
import queue

class BaslerCamera:
    foler = Create()
    VIDEO_IMAGE_QUALITY = 50  #chất lượng hình ảnh video gửi lên
    NAME_FILE_RETRAIN = "retraing"
    NAME_FOLDER_TRAIN = "training"
    SET_TIME_TAKE_IMG = 20000
    def __init__(self,queue_wait = None ,emit_func=None,config_file = None):
        self.camera = None
        self.converter = None
        self.emit_func = emit_func  # Hàm để gửi dữ liệu qua SocketIO (nếu có)
        self.config_file = config_file
        self.queue = queue_wait
        self.lock = threading.Lock()
        self.sender_thread = None
        self.queue_send_video = None
        self.acc_run = True

     
    def initialize_camera(self):
        """
        Khởi tạo camera Basler:
        - Nếu config_file tồn tại -> load cấu hình từ file
        - Nếu không -> dump config mặc định hiện tại ra file
        - Nếu chưa kết nối camera, sẽ thử lại mỗi 2 giây
        """
        try:
            tl_factory = pylon.TlFactory.GetInstance()
            self.camera = None

            # Loop liên tục dò camera
            if self.camera is None:
                try:
                    self.camera = pylon.InstantCamera(tl_factory.CreateFirstDevice())
                except Exception as e:
                    print(f"⚠️ Chưa tìm thấy camera Basler ({e}), thử lại sau 2 giây...")
                    time.sleep(2)  # chờ 2 giây trước khi thử lại
                    return
            self.camera.Open()

            # Nếu có file config -> load
            if self.config_file and os.path.exists(self.config_file):
                # Có file -> load từ file xuống camera
                print(f"🔹 Loading camera config from {self.config_file}")
                pylon.FeaturePersistence.Load(self.config_file, self.camera.GetNodeMap(), True)

                # Sau khi load, nếu bạn muốn đảm bảo camera đang dùng config đó thì không cần làm gì thêm.
                # Nếu muốn "save lại" (cập nhật file nếu có thay đổi nhỏ) thì có thể thêm:
                # pylon.FeaturePersistence.Save(self.config_file, self.camera.GetNodeMap())

            else:
                # Không có file -> dump config hiện tại của camera ra file
                print("⚡ No config file found, using current camera settings and saving...")
                if self.config_file:
                    try:
                        pylon.FeaturePersistence.Save(self.config_file, self.camera.GetNodeMap())
                        print(f"💾 Saved current camera config to {self.config_file}")
                    except Exception as e:
                        print(f"❌ Không thể save config: {e}")

            self.show_camera_info()
            # Chuẩn bị converter sang BGR8 để OpenCV xử lý
            
            
            self.converter = pylon.ImageFormatConverter()
            self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
            self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

            print("✅ Camera initialized successfully")
        except:
            print("Cau hinh loi cam")
    def configure_camera(self):
        try:
            if hasattr(self.camera, "BalanceWhiteAuto"):
              self.camera.BalanceWhiteAuto.SetValue("Once")  # cân màu 1 lần
 
        except Exception as e:
            print("Lỗi khi cấu hình camera:", e)
    def show_camera_info(self):
            device_info = self.camera.GetDeviceInfo()
            print("  Model Name:", device_info.GetModelName())
            print("  Serial Number:", device_info.GetSerialNumber())
            print("  Vendor Name:", device_info.GetVendorName())
            print("  Device Class:", device_info.GetDeviceClass())
    # def _emit_loop(self):
    #     while self.acc_run:
    #         try:
    #             # Luôn chỉ lấy frame mới nhất
    #             jpg_as_text = None
    #             while not self.queue_send_video.empty():
    #                 frame = self.queue_send_video.get_nowait()
    #                 # print("sO LUONG QUEUE TRONG QUEUE LA",self.queue_send_video.qsize())
    #                 _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY),BaslerCamera.VIDEO_IMAGE_QUALITY])
    #                 jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    #                 if jpg_as_text:
    #                     self.emit_func.emit(
    #                         'camera_frame',
    #                         {'image': jpg_as_text},
    #                         namespace='/video'
    #                     )
    #                 time.sleep(1/120)
    #             time.sleep(1/120)
    #         except Exception as e:
    #             time.sleep(1)
    #             print(f"Lỗi gửi ảnh: {e}")

    def configure_camera(self):
        try:
            if hasattr(self.camera, "BalanceWhiteAuto"):
              self.camera.BalanceWhiteAuto.SetValue("Once")  # cân màu 1 lần
 
        except Exception as e:
            print("Lỗi khi cấu hình camera:", e)
    def start_stream(self):
        """1 luu anh vao file trainig 2 luu anh vao file retrain"""
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        self.last_emit_time = time.time()
        self.min_emit_interval = 1/40  # Giới hạn: gửi ảnh mỗi 40ms (20 FPS)  #dieu chinh
        # self.queue_send_video = None
        # sender_started = False
        # self.sender_thread = None    
        while self.camera.IsGrabbing() and self.acc_run == True:
            # if not sender_started:
            #     self.queue_send_video = queue.Queue(maxsize=2)  
            #     self.sender_thread = threading.Thread(target=self._emit_loop, daemon=True)
            #     self.sender_thread.start()
            #     sender_started = True   
            # if not self.sender_thread.is_alive():
            #     print("⚠️ Thread gửi ảnh đã chết, khởi động lại...")
            grabResult = self.camera.RetrieveResult(BaslerCamera.SET_TIME_TAKE_IMG,pylon.TimeoutHandling_Return)
            if grabResult.GrabSucceeded():
                # now = time.time()
                # if self.emit_func and (now - self.last_emit_time) >= self.min_emit_interval:
                #     image_cv = self.converter.Convert(grabResult)
                #     frame = image_cv.GetArray()
                #     # print("sO LUONG QUEUE TRONG QUEUE LA",self.queue_send_video.qsize())
                #     # print("put vao trong queue")
                #     if not self.queue_send_video.full():
                #         self.queue_send_video.put(frame)
                #     else:
                #         # Nếu queue đã đầy thì bỏ frame cũ, thay bằng frame mới
                #         try:
                #             self.queue_send_video.get_nowait()
                #         except queue.Empty:
                #             pass
                #         self.queue_send_video.put(frame)  
                # self.last_emit_time = now
                if self.queue.qsize() > 0:
                        data = self.queue.get()
                        product_name = data.get("productname", -1)
                        index        = data.get("index", -1)
                        lengt_index  = data.get("lengt_index", -1)
                        training     = data.get("training", -1)
                        name_capture  = data.get("name_capture", -1)
                        capture_detect = data.get("capture_detect",-1)
                        #training == 1 chup anh 
                        #training == 2 traing lai
                        #training == 3 chup anh
                        if training == 1 and product_name !=-1  and index!=-1 and  lengt_index != -1:
                            print("Lưu ảnh Vào File Training")
                            self.capture_image_train(product_name,index,lengt_index,"Training")
                        if training == 2  and product_name !=-1  and index!=-1 and  lengt_index != -1:
                            self.capture_image_train(product_name,index,lengt_index,"Retraining")
                        if training == 3:
                            if  name_capture != -1:
                                print("Đang chụp ảnh ")
                                print("name_capture",name_capture)
                                self.capture_one_frame_path(name_capture)
                            if capture_detect!= -1:
                                print("Chụp ảnh nhận diện")
                                img = self.capture_one_frame()
                                try:
                                    process_capture_detect.put(img,block=True,timeout=1)
                                except:
                                    print("Queue đầy không chụp được ảnh")
            grabResult.Release()
            time.sleep(1/60)
        print("Camera chưa sẵn sàng chạy khởi động")
        time.sleep(1)
    def show_camera_window(self):
        try:
            self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

            while self.camera.IsGrabbing():
                grabResult = self.camera.RetrieveResult(BaslerCamera.SET_TIME_TAKE_IMG, pylon.TimeoutHandling_ThrowException)

                if grabResult.GrabSucceeded():
                    image_cv = self.converter.Convert(grabResult)
                    frame = image_cv.GetArray()

                    height, width, _ = frame.shape
                    small_frame = cv2.resize(frame, (int(width / 4), int(height / 4)))
                    cv2.imshow("Camera Feed", small_frame)

                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        # # self.capture_image_train(file_name_product="Product_01", index_point=0, len_arr_list_point=3,name_foder_in_static="Training")  
                        # img = self.capture_one_frame()
                        # cv2.imshow("anh",img)
                        # cv2.waitKey(0)  # Nhấn phím bất kỳ để đóng cửa sổ
                        # cv2.destroyAllWindows()
                        # print("👉 Đã chụp ảnh theo yêu cầu.")
                        break            

                else:
                    print("Lỗi khi chụp:", grabResult.ErrorCode, grabResult.ErrorDescription)

                grabResult.Release()
        except:
            print("Chua ket noi duoc cam nen khong show dc thong tin")
    def capture_image_train(self, file_name_product: str, index_point: int, len_arr_list_point: int,name_foder_in_static:str):
            with self.lock:
                if self.camera is None or not self.camera.IsOpen():
                    print("❌ Camera chưa khởi tạo hoặc không mở được.")
                    return
                if not self.camera.IsGrabbing():
                    self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

                try:
                    self.folder_retrain = Create(BaslerCamera.NAME_FOLDER_TRAIN)
                    # Tạo base: .../static/Training
                    product_folder = self.folder_retrain.create_subfolder_support(name_foder_in_static)
                    # Cho FolderCreator biết base mới
                    self.folder_retrain.base_path = product_folder
                    # Tạo sẵn các thư mục con: Training/<product>/Diem_i
                    for i in range(len_arr_list_point):
                        self.folder_retrain.create_nested_subfolder(file_name_product, f"Diem_{i}")

                    grabResult = self.camera.RetrieveResult(BaslerCamera.SET_TIME_TAKE_IMG,
                                                            pylon.TimeoutHandling_ThrowException)

                    if grabResult.GrabSucceeded():
                        image_cv = self.converter.Convert(grabResult)
                        frame = image_cv.GetArray()

                        if frame is None or frame.size == 0:
                            print("❌ Khung hình rỗng, không thể lưu.")
                        else:
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                            # ✅ ĐÚNG CẤP THƯ MỤC:
                            save_dir = product_folder / file_name_product / f"Diem_{index_point}"
                            save_dir.mkdir(parents=True, exist_ok=True)  # an toàn dù đã tạo trước

                            filename = save_dir / f"img_{timestamp}.png"

                            ok = cv2.imwrite(os.fspath(filename), frame)
                            if ok:
                                print(f"📸 Đã lưu ảnh: {filename}")
                            else:
                                print(f"❌ cv2.imwrite() thất bại: {filename}")
                    else:
                        print("❌ Lỗi khi chụp ảnh:", grabResult.ErrorCode, grabResult.ErrorDescription)

                    grabResult.Release()

                except Exception as e:
                    print(f"⚠️ Lỗi khi lấy ảnh từ camera: {e}")
                    traceback.print_exc()
    def capture_one_frame_path(self, save_path: str = None):
        """
        Chụp một ảnh từ camera và trả về frame (numpy array).
        Nếu save_path được cung cấp, sẽ lưu ảnh vào đường dẫn đó.
        Trả về frame nếu thành công, None nếu lỗi.
        """
        with self.lock:
            if self.camera is None or not self.camera.IsOpen():
                print("❌ Camera chưa khởi tạo hoặc không mở được.")
                return None

            if not self.camera.IsGrabbing():
                self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

            try:
                grabResult = self.camera.RetrieveResult(
                    BaslerCamera.SET_TIME_TAKE_IMG,
                    pylon.TimeoutHandling_ThrowException
                )
                if grabResult.GrabSucceeded():
                    image_cv = self.converter.Convert(grabResult)
                    frame = image_cv.GetArray()
                    grabResult.Release()

                    if frame is None or frame.size == 0:
                        print("❌ Ảnh rỗng, không lấy được frame.")
                        return None
                    # Nếu có đường dẫn lưu, lưu ảnh ngay
                    if save_path:
                        try:
                            ok = cv2.imwrite(save_path, frame)
                            if ok:
                                print(f"📸 Đã lưu ảnh: {save_path}")
                            else:
                                print(f"❌ Lưu ảnh thất bại: {save_path}")
                        except Exception as e:
                            print(f"❌ Lỗi khi lưu ảnh: {e}")

                    return frame  # trả về frame numpy array
                else:
                    print("❌ Lỗi khi chụp ảnh:", grabResult.ErrorCode, grabResult.ErrorDescription)
                    grabResult.Release()
                    return None

            except Exception as e:
                print(f"⚠️ Lỗi khi lấy ảnh từ camera: {e}")
                traceback.print_exc()
                return None
            
    def capture_one_frame(self):
        """
        Chụp một ảnh từ camera và trả về frame (numpy array).
        Trả về None nếu lỗi hoặc không lấy được ảnh.
        """
        with self.lock:
            if self.camera is None or not self.camera.IsOpen():
                print("❌ Camera chưa khởi tạo hoặc không mở được.")
                return None

            if not self.camera.IsGrabbing():
                self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

            try:
                grabResult = self.camera.RetrieveResult(
                    BaslerCamera.SET_TIME_TAKE_IMG,
                    pylon.TimeoutHandling_ThrowException
                )
                if grabResult.GrabSucceeded():
                    image_cv = self.converter.Convert(grabResult)
                    frame = image_cv.GetArray()
                    grabResult.Release()

                    if frame is None or frame.size == 0:
                        print("❌ Ảnh rỗng, không lấy được frame.")
                        return None

                    return frame  # ✅ Trả về ảnh dưới dạng numpy array
                else:
                    print("❌ Lỗi khi chụp ảnh:", grabResult.ErrorCode, grabResult.ErrorDescription)
                    grabResult.Release()
                    return None

            except Exception as e:
                print(f"⚠️ Lỗi khi lấy ảnh từ camera: {e}")
                traceback.print_exc()
                return None
    def release(self):
        print("Đang dừng camera...")
        if self.sender_thread:
            self.sender_thread.join(timeout=1)  # đợi thread kết thúc
        if self.camera:  
            self.camera.StopGrabbing()
            self.camera.Close()
        cv2.destroyAllWindows()
        self.acc_run = False   # tat luong va came
        print("Đã giải phóng tài nguyên camera.")
    def run_cam(self):
        self.initialize_camera()
        try:
            self.show_camera_window()
        except :
            print("Lỗi pylon:1")
            self.initialize_camera()
    def run_cam_html(self):
        try:
            self.show_camera_info()
            self.start_stream()
        except:
            print("Lỗi pylon:2")
            self.initialize_camera()
        
    def try_connect(self):
        while True:
            try:
                self.initialize_camera()
                self.show_camera_info()
                break
            except:
                print("Xin Hãy kết nối với cam, Cam đang lỗi")
                
    def is_camera_stable(self):
        """
        Kiểm tra camera có đang hoạt động hay không.
        Tránh conflict với luồng start_stream (không gọi RetrieveResult nữa).
        """
        try:
            if self.camera is None:
                print("❌ Camera chưa khởi tạo.")
                return False

            if not self.camera.IsOpen():
                print("❌ Camera chưa mở.")
                return False

            if self.camera.IsGrabbing():
                # Camera đang grabbing (có thể từ start_stream)
                print("✅ Camera đang chạy (luồng start_stream hoạt động).")
                return True
            else:
                print("⚠️ Camera đã mở nhưng chưa grabbing.")
                return False

        except Exception as e:
            print(f"⚠️ Lỗi khi kiểm tra camera: {e}")
            return False
    def show_file_config(self):
        path_file_config = BaslerCamera.foler.get_path_same_level("Camera_25129678.pfs")
        if path_file_config and self.camera is not None:
            data_file_config = BaslerCamera.foler.read_file_in_path(path_file_config)
            device_info = self.camera.GetDeviceInfo()

            # Lấy các giá trị từ file config
            frame = self.get_parameter_value(data_file_config, "AcquisitionFrameRateAbs")
            width = self.get_parameter_value(data_file_config, "Width")
            height = self.get_parameter_value(data_file_config, "Height")
            exposure = self.get_parameter_value(data_file_config, "ExposureTime")  # ví dụ thêm ExposureTime
            gain = self.get_parameter_value(data_file_config, "Gain")  # ví dụ thêm Gain
 
            # Lấy thêm thông tin camera từ DeviceInfo
            model = device_info.GetModelName()
            serial = device_info.GetSerialNumber()
            vendor = device_info.GetVendorName()
            device_class = device_info.GetDeviceClass()

            # Trả về tất cả thông tin dưới dạng dictionary
            return {
                "frame": frame,
                "width": width,
                "height": height,
                "exposure": exposure,
                "gain": gain,
                "model": model,
                "serial": serial,
                "vendor": vendor,
                "device_class": device_class
            }
        return False

            
    def get_parameter_value(self,data, parameter_name):
        """
        From the text data 'data', find 'parameter_name' and return its value.
        Each line format: ParameterName\tValue
        """
        if not data:
            return None

        # Split data into lines
        for line in data.splitlines():
            # Remove leading/trailing whitespace
            line = line.strip()
            # Check if the line starts with the parameter name
            if line.startswith(parameter_name):
                # Split by whitespace or tab
                parts = line.split()
                if len(parts) >= 2:
                    return parts[1]  # value
        return None
# def main():
#     cam = BaslerCamera(config_file="Camera_25129678.pfs")
#     # print(cam.is_camera_stable())
#     # datawew= cam.show_file_config()
#     # print(datawew)

#     print(cam.show_file_config())
#     cam.run_cam()
# if __name__ == "__main__":
#     main()
