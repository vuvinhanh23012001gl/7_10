@echo off
cd /d %~dp0

REM Chạy Flask app trong nền
start "" python run.py

REM Đợi 2 giây cho Flask khởi động (có thể tăng thêm nếu cần)
timeout /t 2 /nobreak > nul

REM Mở trình duyệt với địa chỉ Flask app
start "" http://localhost:5000

REM Giữ cửa sổ cmd mở (nếu bạn muốn nhìn log)
pause
@REM @echo off
@REM cd /d %~dp0

@REM REM Chạy Flask app ẩn qua file vbs
@REM cscript //nologo run_flask.vbs

@REM REM Đợi vài giây cho server khởi động
@REM timeout /t 3 /nobreak > nul

@REM REM Mở trình duyệt mặc định tới localhost:5000
@REM start "" http://localhost:5000