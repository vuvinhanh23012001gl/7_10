# from shared_queue import queue_tx_web_main,queue_rx_web_main
import threading
import time
import queue
  
class ManagerSerial:
    def __init__(self,queue_rx_arm=None,queue_tx_arm=None):
        from serial_communication import Serial_Com 
        # Khởi tạo lớp giao tiếp Serial
        self.gate_open_com_is_working = None
        self.serial_com = Serial_Com()
        
        self.com_is_open = False
        # Hàng đợi gửi / nhận
        self.tx_queue = queue_tx_arm
        self.rx_queue = queue_rx_arm

        # Cờ chạy luồng
        self.running_tx = True
        self.running_rx = True
        self.running_check_connect = True
        

        self.rx_thread = threading.Thread(target=self._check_connect,daemon=True, name="check_connect_com")
        self.rx_thread.start()

    def open_thread_receive_and_send(self):
    
        self.running_rx = True
        self.running_tx = True

        print("✅ Mở 2 luồng nhận gửi dữ liệu")
        self.rx_thread = threading.Thread(target=self._listen_serial,daemon=True, name="SerialListener")
        self.rx_thread.start()

        self.tx_thread = threading.Thread(target=self._send_serial,daemon = True, name="SerialSender")
        self.tx_thread.start()
    
    def close_thread_receive_and_send(self):
        # Dừng các luồng
        print("🛑 Đang dừng luồng gửi nhận dữ liệu tới COM")

        # Đặt cờ chạy về False để các luồng thoát vòng lặp
        self.running_rx = False
        self.running_tx = False
        self.serial_com.ser = None
        self.serial_com.port = None
        # Nếu luồng đang chạy, join để đảm bảo đã kết thúc
        if hasattr(self, 'rx_thread') and self.rx_thread.is_alive():
            self.rx_thread.join(timeout=1)
            print("✅ Luồng nhận dữ liệu đã dừng")

        if hasattr(self, 'tx_thread') and self.tx_thread.is_alive():
            self.tx_thread.join(timeout=1)
            print("✅ Luồng gửi dữ liệu đã dừng")
        self.clear_rx_queue()
        self.clear_tx_queue()
        print("✅ Đã dừng thành công.")
       
                        
    def _check_connect(self):
        flag = False
        while self.running_check_connect:
            exists, busy = self.serial_com.is_com_busy(self.serial_com.port)
            if not exists:
                # print("Cổng COM đã rút ra")
                self.gate_open_com_is_working = False
                self.com_is_open = False
                self.serial_com.ser = None
                if flag:  # tat cong com 1 lan
                    self.close_thread_receive_and_send()
                    flag = False
                    self.com_is_open = False
            elif busy:
                print("Cổng com đang hoạt động")
                self.gate_open_com_is_working = True
            else:
                if not self.serial_com.ser:
                    status = self.serial_com.open_port()
                    if status:
                        flag =  True
                        print("Mở cổng thành công 2")
                        self.com_is_open = True
                        self.open_thread_receive_and_send()
                    else:
                        print("Mở cổng thất bại")
            time.sleep(1)
    def update_com(self,name_port,baudrate):
        if not self.com_is_open:
            status_open_com = self.serial_com.open_config_manual(name_port,baudrate)
            if status_open_com:
                self.open_thread_receive_and_send()
                self.com_is_open =  True
                print("[1]Update thành công cổng COM")
                return True
            else:
                print("[1]Update thất bại cổng COM")
                self.com_is_open =  False
                return False
        else:
            self.close_thread_receive_and_send()
            status_open_com = self.serial_com.open_config_manual(name_port,baudrate)
            if status_open_com:
                self.open_thread_receive_and_send()
                self.com_is_open =  True
                print("[2]Update thành công cổng COM")
                return True
            else:
                self.com_is_open =  False
                print("[2]Update thất bại")
                return False
            
    def send_data(self, data):
        """Đưa dữ liệu vào hàng đợi gửi"""
        try:
            self.tx_queue.put(data)
            print(f"[TX Queue] ➜ {data}")
        except queue.Full:
            print("⚠️ Hàng đợi gửi đầy. Không thể gửi:", data)

    def receive_data(self):
        """Nhận dữ liệu từ serial và đưa vào hàng đợi nhận"""
        data = self.serial_com.receive_data()
        if data:
            try:
                self.rx_queue.put_nowait(data)
                # print("size queue_rx_arm:", self.rx_queue.qsize())
            except queue.Full:
                print("⚠️ Hàng đợi nhận đầy:", data)
    

    def get_data_from_queue(self):   # co su dung nha
        """Lấy dữ liệu đã nhận ra khỏi hàng đợi"""
        if not self.rx_queue.empty():
            return self.rx_queue.get()
        return None
    
    def _listen_serial(self):
        print("✅[Mở 1]:Luồng lắng nghe")
        while self.running_rx:
            # print("luong  lang nghe dang duoc bat")
            # time.sleep(2)
            try:
                self.receive_data()
                time.sleep(0.001)  # 🔑 nghỉ 1ms tránh CPU 100%
            except Exception as e:
                print("[SerialListener] Lỗi:", e)
                time.sleep(2)
          
            
    def _send_serial(self):
        print("✅[Mở 2] Luồng gửi")
        while self.running_tx:
            # print("luong gui dang duoc bat")
            # time.sleep(2)
            try:
                # block tối đa 0.1s để chờ data, tránh busy-wait
                data = self.tx_queue.get(timeout=0.1)
                self.serial_com.send_data(data)
            except queue.Empty:
                continue  # không có gì để gửi, quay lại vòng lặp
            except Exception as e:
                print("[SerialSender] Lỗi:", e)
                time.sleep(2)

    def get_rx_queue_size(self):
        """Trả về số lượng phần tử trong hàng đợi nhận"""
        size = self.rx_queue.qsize()
        print(f"📥 Số lượng phần tử trong rx_queue: {size}")
        return size
    def get_tx_queue_size(self):
        """Trả về số lượng phần tử trong hàng đợi gửi"""
        size = self.tx_queue.qsize()
        print(f"📦 Số lượng phần tử trong tx_queue: {size}")
        return size
    def clear_rx_queue(self):
        """Xóa sạch toàn bộ hàng đợi nhận"""
        with self.rx_queue.mutex:
            size = len(self.rx_queue.queue)
            self.rx_queue.queue.clear()
        print(f"🗑️ Đã xóa {size} mục trong hàng đợi nhận (clear sạch).")

    def clear_tx_queue(self):
            """Xóa sạch toàn bộ hàng đợi gửi"""
            with self.tx_queue.mutex:
                size = len(self.tx_queue.queue)
                self.tx_queue.queue.clear()
            print(f"🗑️ Đã xóa {size} mục trong hàng đợi gửi (clear sạch).")
    def  get_dict_data_send_server(self):
        dict_data = self.serial_com.to_dict()
        return dict_data 
        


# ms = ManagerSerial(queue_tx_web_main ,queue_rx_web_main)      
# -------------------------------
# Ví dụ chạy trực tiếp
# -------------------------------
# ms = ManagerSerial(queue_tx_web_main ,queue_rx_web_main)
# def listen_update():
#         """Luồng phụ: chờ nhấn Enter để đổi COM"""
#         while True:
#             new_port = input("Nhập cổng mới: ")
#             new_baud = int(input("Nhập baudrate mới: "))
#             ms.update_com(new_port, new_baud)
# update_thread = threading.Thread(target=listen_update, daemon=False)
# update_thread.start()



































