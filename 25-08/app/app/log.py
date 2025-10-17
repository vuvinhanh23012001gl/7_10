import logging
import threading
import os


class Log:
    def __init__(self, name=__name__, log_file="app.log"):
        self.name = name
        self.log_file = log_file
        self.console_enabled = False
        self.file_enabled = False
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # Cho phép tất cả mức log
        self.formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(threadName)s] (%(name)s:%(lineno)d): %(message)s"
        )

        # Dùng Lock để đảm bảo việc thêm/bỏ handler thread-safe
        self._lock = threading.Lock()

    # ===============================
    # Cấu hình
    # ===============================
    def log_and_print(self, msg, value=None, level="info"):
        # Ghép message nếu có value
        full_msg = f"{msg}: {value}" if value is not None else msg
        if level == "debug":
            self.logger.debug(full_msg)
        elif level == "warning":
            self.logger.warning(full_msg)
        elif level == "error":
            self.logger.error(full_msg)
        elif level == "critical":
            self.logger.critical(full_msg)
        else:
            self.logger.info(full_msg)
            
    def enable_console(self):
        with self._lock:
            if not self.console_enabled:
                ch = logging.StreamHandler()
                ch.setLevel(logging.DEBUG)
                ch.setFormatter(self.formatter)
                self.logger.addHandler(ch)
                self.console_enabled = True

    def disable_console(self):
        with self._lock:
            for h in list(self.logger.handlers):
                if isinstance(h, logging.StreamHandler):
                    self.logger.removeHandler(h)
            self.console_enabled = False

    def enable_file(self):
        with self._lock:
            if not self.file_enabled:
                os.makedirs(os.path.dirname(self.log_file) or ".", exist_ok=True)
                fh = logging.FileHandler(self.log_file, encoding="utf-8")
                fh.setLevel(logging.DEBUG)
                fh.setFormatter(self.formatter)
                self.logger.addHandler(fh)
                self.file_enabled = True

    def disable_file(self):
        with self._lock:
            for h in list(self.logger.handlers):
                if isinstance(h, logging.FileHandler):
                    self.logger.removeHandler(h)
            self.file_enabled = False

    # ===============================
    # Các hàm log tiện dụng
    # ===============================
    def debug(self, msg):
        self.logger.debug(msg)
        

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

# import time
# logger = Log(__name__)
# logger.enable_console()
# logger.enable_file()
# def worker(n):
#     for i in range(3):
#         logger.info(f"Luồng {n}: chạy lần {i}")
#         time.sleep(0.3)

# threads = []
# for i in range(3):
#     t = threading.Thread(target=worker, args=(i+1,), name=f"Thread-{i+1}")
#     threads.append(t)
#     t.start()

# for t in threads:
#     t.join()