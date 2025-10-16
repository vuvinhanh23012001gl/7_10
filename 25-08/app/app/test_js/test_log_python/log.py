import logging

logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)

# handler ghi ra console
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# handler ghi vào file (append)
fh = logging.FileHandler("app.log", encoding="utf-8")
fh.setLevel(logging.DEBUG)

# định dạng
fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
ch.setFormatter(fmt)
fh.setFormatter(fmt)

logger.addHandler(ch)
logger.addHandler(fh)

logger.debug("Một message debug")
logger.info("Ứng dụng bắt đầu")
logger.warning("Cảnh báo: something odd")
logger.error("Lỗi rồi")
