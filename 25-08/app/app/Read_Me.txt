# Model → load 1 lần duy nhất khi khởi động phần mềm.
# Master data (shape, quy định) → load khi chọn ID sản phẩm hoặc khi người dùng thay đổi quy chuẩn.
# Detection data (kết quả model trên từng ảnh) → luôn tạo mới cho từng ảnh.

# main_pc.click_page_html = 4  --> Là vào thêm sản phẩm mới
# main_pc.click_page_html = 1  --> Là vào trang main chính
# main_pc.click_page_html = 3  --> Là lấy master 
# main_pc.click_page_html = 2  --> Training model
# main_pc.click_page_html = 5  --> Choose master
# main_pc.click_page_html = 6  --> Add master
# main_pc.click_page_html = 7  --> Thay đổi cồng COM
# main_pc.click_page_html = 8 # Câu hình cổng camera