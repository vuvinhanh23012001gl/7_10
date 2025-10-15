from flask import Flask
from flask import Flask,request,jsonify
from flask import Blueprint,render_template
from flask_socketio import SocketIO
from connect_camera import BaslerCamera
from flask import redirect, url_for
from producttypemanager import ProductTypeManager
from process_master import Proces_Shape_Master
from config_software import OilDetectionSystem
from common_value import NAME_FILE_CHOOSE_MASTER
import threading
import time
import func
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
manage_product = ProductTypeManager()
shape_master = Proces_Shape_Master()


main_html = Blueprint("main",__name__)
api = Blueprint("api",__name__)
api_new_model = Blueprint("api_new_model",__name__)
api_choose_master = Blueprint("api_choose_master",__name__)
api_take_master = Blueprint("api_take_master",__name__)
api_run_application = Blueprint("api_run_application",__name__)
api_new_product = Blueprint("api_new_product",__name__)
api_add_master = Blueprint("api_add_master",__name__)
api_config_camera = Blueprint("api_config_camera",__name__)
api_config_com = Blueprint("api_config_com",__name__)
api_config_software = Blueprint("api_config_software",__name__)

#-------open thread--------
OPEN_THREAD_LOG =  True
OPEN_THREAD_STREAM =  True
OPEN_THREAD_IMG = True

# -----------------------Task-----------------------------------------------
def stream_frames():
    while OPEN_THREAD_STREAM:
         cam_basler.run_cam_html()
         time.sleep(1)
    cam_basler.release()
    print("Thoát luồng gửi video thành công")


def stream_img(): # queue_tx_web_main gồm ảnh và data
    global OPEN_THREAD_IMG
    arr_save_status_frame_ok = []
    while OPEN_THREAD_IMG:
        if queue_tx_web_main.qsize() > 0:
            data_img_detect = queue_tx_web_main.get(block=False)
            img = data_img_detect.get("img",None)
            try:
                img_convert  = func.frame_to_jpeg_bytes(img)
                data_img_detect["img"] = img_convert
                index = data_img_detect.get("index",-1)
                length = data_img_detect.get("length",-1)
                status_frame = data_img_detect.get("status_frame",-1)
                if status_frame != -1 and index >= 0:
                    arr_save_status_frame_ok.append(status_frame)
                if index!=-1 and length != -1:
                    if index == length -1 :
                        main_pc.mumber_total_product += 1
                        data_img_detect["total_product"] = main_pc.mumber_total_product
                        status_judment = func.check_all_true(arr_save_status_frame_ok)
                        data_img_detect["status_judment"] = status_judment
                        if status_judment : main_pc.mumber_product_oke+=1
                        data_img_detect["total_product_ok"] = main_pc.mumber_product_oke
                        arr_save_status_frame_ok = []
                socketio.emit("photo_taken",data_img_detect, namespace="/img_and_data")
            except:
                print("convert anh khong thong cong")
        time.sleep(0.01)

def stream_logs(): # gồm các loại log   # va trang thai kết nối cam
    while OPEN_THREAD_LOG:  
            socketio.emit("status_connect_com_arm", {"status": main_pc.status_check_connect_arm}, namespace='/log')
            socketio.emit("status_connect_camera", {"status": main_pc.status_check_connect_arm}, namespace='/log')   
            match main_pc.click_page_html:
                case 3:
                    if not queue_tx_web_log.empty():
                        socketio.emit("log_take_master", {"log": f"{queue_tx_web_log.get()}"}, namespace='/log')
                case 4:
                    log_message = manage_product.get_all_ids_and_names()      # Gửi log cho thêm sản phẩm mới
                    if log_message:
                        socketio.emit("log_message", {"log_create_product": log_message}, namespace='/log')
                case 6:
                    if not queue_tx_web_log.empty():
                        socketio.emit("log_data", {"log": f"{queue_tx_web_log.get()}"}, namespace='/log')
                case 2:
                    if not queue_tx_web_log.empty():
                        socketio.emit("log_message", {"log_training": f"{queue_tx_web_log.get()}"}, namespace='/log')    #Gửi log cho File Training
                case 1: # main
                    # queue_tx_web_log.put("xin chao ban")
                    if not queue_tx_web_log.empty():
                        socketio.emit("log_message_judment", {"log_data": f"{queue_tx_web_log.get()}"}, namespace='/log')
            print(main_pc.click_page_html)
            time.sleep(1)

# -----------------------End Task-----------------------------------------------


@main_html.route("/empty_page.html")
def already_open():
    # Đây là trang báo lỗi khi user mở tab thứ 2
    return render_template("empty_page.html")
@socketio.on('connect', namespace='/video')
def video_connect():
    print("Client connected to /video")
@socketio.on('connect', namespace='/img_and_data')
def handle_video_connect():
    print("📡 Client connected to /img_and_data")
@socketio.on('connect', namespace='/log')
def handle_log_connect():
    print("📡 Client connected to /log")
@socketio.on('connect',namespace='/data_add_master')  #'/data_add_master' img + loction point,...
def handle_data_send_connect():
    print("📡 Client connect to /data_add_master") #img hiển thị hình ảnh sản phẩm

# Blueprint main---------------------------------------------------------------------------------
@main_html.route("/")
def show_main():
    """Là hàm hiển thị giao diện chính trên Html"""
    func.create_choose_master(NAME_FILE_CHOOSE_MASTER) #tạo file choose_master nếu tạo rồi thì thôi
    choose_master_index = func.read_data_from_file(NAME_FILE_CHOOSE_MASTER)#đọc lại file choose master cũ xem lần trước  người dùng chọn gì
    arr_type_id = manage_product.get_list_id_product()
    # print("arr_type_id :",arr_type_id)
    # print("choose_master_index :",choose_master_index)
    main_pc.click_page_html = 1  # thong bao dang o trang web chinh
    data_strip = choose_master_index.strip()
    if data_strip in  arr_type_id:
        print(f"gui data master co ten {choose_master_index}")
        path_arr_img = manage_product.get_list_path_master_product_img_name(data_strip)
        print(path_arr_img)
        return render_template("show_main.html",path_arr_img = path_arr_img)
    return render_template("show_main.html",path_arr_img = None)
@main_html.route('/out_app', methods=['GET'])
def out_app():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Server không hỗ trợ shutdown trực tiếp")




    print("Người dùng thoát tab")
    return jsonify({"status":"OK"})
#--------------------------------------------------------Api_run_application---------------------------------------------
@api_run_application.route('/run_application',methods = ['GET'])
def run_application():
    """Hàm này đê chạy run khi người dùng nhấn "chạy" trên giao diện chính"""
    main_pc.is_run = 1      #bat bien Run len bat dau qua trinh chay
    print("Đã nhấn nút Run application")
    return jsonify({"status":"OK"})
#--------------------------------------------------------Api_master_take---------------------------------------------

@api_take_master.route("/master_close",methods=["POST"])
def master_close():
    main_pc.click_page_html = 1  #Ve lai main chinh
    data = request.get_json()
    print(data)
    return jsonify({'status':"OKE"})


@api_take_master.route("/master_take",methods=["POST"])  #Khi nhan vao take masster thi thuc hien gui anh len truoc
def master_take():
    cam_basler.disable_send_video() #dung luong gui video khi nguoi dung vao lai
    main_pc.click_page_html = 3  
    data = request.get_json()
    print(data)
    func.create_choose_master(NAME_FILE_CHOOSE_MASTER) # tạo file choose_master nếu tạo rồi thì thôi
    choose_master_index = func.read_data_from_file(NAME_FILE_CHOOSE_MASTER)# đọc lại file choose master cũ xem lần trước  người dùng chọn gì
    arr_type_id = manage_product.get_list_id_product()
    data_strip = choose_master_index.strip()
    if data_strip in  arr_type_id:
        print(f"gui data master co ten {choose_master_index}")
        path_arr_img = manage_product.get_list_path_master_product_img_name(data_strip)
        print("path_arr_img",path_arr_img)
        shape_master.load_file()
        print("\nshape_master.get_data_is_id(data_strip) la:------------------------\n",shape_master.get_data_is_id(data_strip))
        return {"path_arr_img": path_arr_img,"Shapes":shape_master.get_data_is_id(data_strip)}
    return {"path_arr_img": None,"Shapes":None}





@api_take_master.route("/config_master",methods=["POST"])
def config_master():
    data = request.get_json()
    choose_master_index = func.read_data_from_file(NAME_FILE_CHOOSE_MASTER) # đọc lại file choose master cũ xem lần trước  người dùng chọn gì
    choose_master_index = str(choose_master_index).strip()
    status_check = shape_master.check_all_rules(data)
    if status_check:
        status_save = shape_master.save_shapes_to_json(choose_master_index,data)
        queue_tx_web_log.put_nowait("[Server]Lưu dữ liệu thành công") if status_save else queue_tx_web_log.put_nowait("[Server]Lưu dữ liệu thất bại")
    else:
        print("Dữ liệu bị lỗi")
        queue_tx_web_log.put_nowait("[Server]Kiểm tra dữ liệu bị sai")
    return jsonify({'status':"OKE"})



#--------------------------------------------------------Api_new_product ---------------------------------------------
@api_new_product.route("/add")
def add():
     cam_basler.disable_send_video() #dung luong gui video khi nguoi dung vao lai
     main_pc.click_page_html = 4

     return render_template("save_product_new.html")
@api_new_product.route("/upload", methods=["POST"])
def upload_product():
    # ---- Lấy dữ liệu text từ form ----
    product_id = request.form.get("product_id")
    product_name = request.form.get("product_name")
    limit_x = request.form.get("limit_x")
    limit_y = request.form.get("limit_y")
    limit_z = request.form.get("limit_z")
    description = request.form.get("description")
    # ---- Lấy file từ form ----
    file = request.files.get("file_upload")
    try:
        product_id = str(product_id)
        product_name = str(product_name)
        limit_x = int(limit_x.strip())
        limit_y = int(limit_y.strip())
        limit_z = int(limit_z.strip())
    except:
        print("Dữ liệu gưi về lỗi")
        return jsonify({"success": False, "ErrorDataIncorect": "Dữ liệu bị gửi sai"}), 400
    if not file:
        print("Chưa nhận được File ảnh sản phẩm")
        return jsonify({"success": False, "ErrorNotSendFile": "Hãy chọn hình ảnh sản phẩm"}), 400

    # ---- Thư mục và tên file muốn lưu ----
    status_create_manage = manage_product.add_product_type(product_id,product_name,[limit_x,limit_y,limit_z],description)
    print("status_create_manage la:............",status_create_manage)
    if not status_create_manage:
        print("Sản phẩm loại này đã tồn tại .Hãy đặt ID khác hoặc tìm sản phẩm trong danh sách sản phẩm")
        return jsonify({"success": False, "ErroHasExitsed": "Sản phẩm loại này đã tồn tại .Hãy đặt ID khác hoặc tìm sản phẩm trong danh sách sản phẩm"}), 400
    save_dir = manage_product.absolute_path(product_id)
    if not save_dir:
        print("Tìm không ra sản link ảnh sản phẩm vừa tạo ra")
        return jsonify({"success": False, "ErroNotFileImg": "Tìm không ra sản link ảnh sản phẩm vừa tạo ra"}), 400
    print("Đường dẫn tới ảnh",save_dir)
    save_filename = f"Img_{product_id}.png"     # tên file mong muốn
    print("Tên ảnh lưu là",save_filename)
    save_path = os.path.join(save_dir, save_filename)
    # ---- Lưu file ----
    file.save(save_path)
    # ---- Trả kết quả về client ----
    manage_product.load_from_file()
    return jsonify({
        "success": True,
        "product_id": product_id,
        "product_name": product_name,
        "limit_x": limit_x,
        "limit_y": limit_y,
        "limit_z": limit_z,
        "saved_path": save_path,                       # đường dẫn trên server
        "url": f"/static/Product_Photo/{save_filename}"  # đường dẫn để truy cập từ browser
    })
#--------------------------------------------------------Api_choose_master---------------------------------------------
@api_choose_master.route("/get_show_main",methods = ["POST"])
def get_content():
    json_data = request.get_json()
    choose_master = json_data.get('data')
    print(f"Master được chọn là : {choose_master}")
    func.clear_file_content(NAME_FILE_CHOOSE_MASTER)
    func.write_data_to_file(NAME_FILE_CHOOSE_MASTER,choose_master)
    response = {
        'redirect_url':'/'
    }
    return jsonify(response)
@api_choose_master.route("/chose_product")
def chose_product():
    cam_basler.disable_send_video() # ngan nguoi dung nhan linh tinh khi dang gui video len nha
    main_pc.click_page_html = 5
    data =  manage_product.get_file_data() 
    choose_master_index = func.read_data_from_file(NAME_FILE_CHOOSE_MASTER)
    print("Data gui len server ",data)
    return render_template("chose_product.html",data = data,choose_master = choose_master_index)

@api_choose_master.route("/exit")
def exit_choose_master():
    response = {
        'redirect_url':'/'
    }
    return jsonify(response)
@api_choose_master.route("/erase_product",methods = ["POST"]) #phan nay co ban la oke1 roi 
def erase_product():
    print("------------------------------------------Tiến hành xóa bắt đầu----------------------------------")
    data = request.get_json()
    print(data)
    Choose_product_erase = data.get("Choose_product_erase",-1)
    print(Choose_product_erase)
    if Choose_product_erase != -1 :
        status_erase_product = manage_product.remove_product_type(Choose_product_erase)
        if status_erase_product:
            shape_master.update_data() 
            manage_product.init()
            response = {
                'redirect_url':'/'
            }
            print("------------------------------------------Xoa thanh cong master----------------------------------")
            return jsonify(response)

        else :
            print("------------------------------------------Tiến hành xóa kết thúc 2----------------------------------")
            return jsonify({"status":"200OK","erase":"NG"})
    else:
        print("------------------------------------------Tiến hành xóa kết thúc 3----------------------------------")
        print("Không nhận được data chuẩn Form")
    return jsonify({"status":"200OK","erase":None})


#----------------------------------------------api_add_master------------------------------------------------------


@api_add_master.route("/run_all_master",methods=["POST"],strict_slashes=False)
def run_all_master():
    data = request.get_json()
    func.create_choose_master(NAME_FILE_CHOOSE_MASTER) # tạo file choose_master nếu tạo rồi thì thôi
    choose_master_index = func.read_data_from_file(NAME_FILE_CHOOSE_MASTER)# đọc lại file choose master cũ xem lần trước  người dùng chọn gì
    arr_type_id = manage_product.get_list_id_product()
    data_strip = choose_master_index.strip()
    if data_strip in  arr_type_id:
        arr_point = manage_product.return_data_list_point(data_strip)
        print("arr_point",arr_point)
        print("len arr_point",len(arr_point))
        if arr_point:
            for point in arr_point:
                   x=point.get("x",-1)
                   y=point.get("y",-1)
                   z=point.get("z",-1)
                   brightness=point.get("brightness",-1)
                   if x == -1 or y == -1 or z==-1 or brightness==-1:
                       return jsonify({"status_run":"erro"})
                   else :
                       data_send = f"cmd:{x},{y},{z},{brightness}"
                   print(data_send)
                   queue_rx_web_api.put(data_send)
            return jsonify({"status_run":"oke"})
        else:
            print("Không tìm thấy ID ")
            return jsonify({"status_run":"erro"})
    else:
        return jsonify({"status_run":"erro"})

@api_add_master.route("/exit")
def exit_add_master():
    cam_basler.disable_send_video() #dung luong gui video khi nhan thoat
    response = {
        'redirect_url':'/'
    }
    return jsonify(response)

@api_add_master.route("/",methods=["POST"],strict_slashes=False)
def api_add_master_tree():
    main_pc.click_page_html = 6  #Ve lai main chinh
    data = request.get_json()
    print(data)
    func.create_choose_master(NAME_FILE_CHOOSE_MASTER) # tạo file choose_master nếu tạo rồi thì thôi
    choose_master_index = func.read_data_from_file(NAME_FILE_CHOOSE_MASTER)# đọc lại file choose master cũ xem lần trước  người dùng chọn gì
    arr_type_id = manage_product.get_list_id_product()
    data_strip = choose_master_index.strip()
    cam_basler.enable_send_video()
    if data_strip in  arr_type_id:
        print(f"gui data master co ten {choose_master_index}")
        path_arr_img = manage_product.get_list_path_master_product_img_name(data_strip)
        arr_point = manage_product.return_data_list_point(data_strip)
        print(path_arr_img)
        inf_product = manage_product.get_all_ids_and_names()
        socketio.emit("data_realtime", {
            "path_arr_img": path_arr_img,
            "arr_point": arr_point,
            "inf_product": inf_product
        },namespace='/data_add_master')
        return {"path_arr_img": path_arr_img,"arr_point":arr_point,"inf_product":inf_product}
    return {"path_arr_img": None,"arr_point":None,"inf_product":None}

# "Shapes":shape_master.get_data_is_id(data_strip)
@api_add_master.route("/erase_index",methods=["POST"],strict_slashes=False)
def erase_index():
    data  =  request.get_json()
    func.create_choose_master(NAME_FILE_CHOOSE_MASTER) # tạo file choose_master nếu tạo rồi thì thôi
    choose_id = func.read_data_from_file(NAME_FILE_CHOOSE_MASTER)# đọc lại file choose master cũ xem lần trước  người dùng chọn gì
    choose_id_strip = choose_id.strip()
    index = data.get("index",-1)
    if index != -1:
        print("choose_id_strip",choose_id_strip)
        print("index :",index)
        manage_product.remove_all_master_index(str(choose_id_strip),int(index))
        path_arr_img = manage_product.get_list_path_master_product_img_name(choose_id_strip)
        arr_point = manage_product.return_data_list_point(choose_id_strip)
        print(path_arr_img)
        inf_product = manage_product.get_all_ids_and_names()
        socketio.emit("data_realtime", {
                            "path_arr_img": path_arr_img,
                            "arr_point": arr_point,
                            "inf_product": inf_product
                    },namespace='/data_add_master')
    return jsonify({"message":"OK"})


@api_add_master.route("/capture_master",methods=["POST"],strict_slashes=False)
def capture_master():
       #néu có ảnh sẵn rồi thì không tạo file nữa và chỉnh sửa điểm trong index nếu chua có điểm thì đó là sản phẩm mới thì sẽ tạo ra file mới ảnh mới , thêm điẻm mới
       data = request.get_json()
       index_capture = data.get("index",-1)
       x = data.get("x",-1)
       y = data.get("y",-1)
       z = data.get("z",-1)
       k = data.get("k",-1)

       print("type",type(x),type(y))
       func.create_choose_master(NAME_FILE_CHOOSE_MASTER) # tạo file choose_master nếu tạo rồi thì thôi
       choose_master_index = func.read_data_from_file(NAME_FILE_CHOOSE_MASTER)# đọc lại file choose master cũ xem lần trước  người dùng chọn gì
       arr_type_id = manage_product.get_list_id_product()
       data_strip = choose_master_index.strip()
       if data_strip in  arr_type_id:
            status_camera = cam_basler.is_camera_stable()
            if status_camera :
                status = manage_product.create_file_and_path_img_master(data_strip,f"img_{index_capture}.png")
                print(status)
                if status:
                    status_create_file = status.get("return",-1)
                    path = status.get("path",-1)
                    if status_create_file != -1 and path!=-1 and status_create_file == True:
                        print("Tiến hành lưu ảnh mới điểm mới...")
                        print("xyz",x,y,z,k,index_capture)
                        queue_accept_capture.put_nowait({"training":3,"name_capture":path})
                        manage_product.add_list_point_to_product(data_strip,int(x.strip()),int(y.strip()),int(z.strip()),int(k.strip()))
                    elif (status_create_file != -1 and path!=-1 and status_create_file == False):
                        print("Tiến hành sửa điểm cũ lưu ảnh mới...")
                        print("xyz",x,y,z,k,index_capture)
                        queue_accept_capture.put_nowait({"training":3,"name_capture":path})
                        manage_product.fix_score_point_product(data_strip,int(x.strip()),int(y.strip()),int(z.strip()),int(k.strip()),index_capture)
                        # print("datatata su khhi adddddd la")
                        # print(manage_product.return_data_dict(data_strip))
                    else:
                        print("Tạo File thất bại")

                    path_arr_img = manage_product.get_list_path_master_product_img_name(data_strip)
                    arr_point = manage_product.return_data_list_point(data_strip)
                    print(path_arr_img)
                    inf_product = manage_product.get_all_ids_and_names()
                    socketio.emit("data_realtime", {
                            "path_arr_img": path_arr_img,
                            "arr_point": arr_point,
                            "inf_product": inf_product
                    },namespace='/data_add_master')
                else:
                    print("Tạo File thất bại")
                    queue_tx_web_log.put_nowait("\nThêm thất bại")
            else:
                queue_tx_web_log.put_nowait("Camera hiện tại không hoạt động nên không thể chụp ảnh được\n")
                print("Camera hiện tại không hoạt động nên không thể chụp ảnh được")
       else:
           print("Không tìm thấy sản phẩm có ID trong danh sách ID đã lưu để chụp ảnh\n")
       return jsonify({'status':"200OK"})

#----------------------------------------------------api_config_camera-------------------------------------------
@api_config_camera.route("/exit")
def exit_api_config_camera():
    response = {
        'redirect_url':'/'
    }
    return jsonify(response)

@api_config_camera.route("/get_data_show",strict_slashes=False)
def get_data_show():
    cam_basler.disable_send_video() #dung luong gui video khi nguoi dung vao lai
    main_pc.click_page_html = 8 # Câu hình cổng com
    data_show = cam_basler.show_file_config()
    return jsonify({"status":"200OK","data":data_show})





@api_config_software.route("/exit")
def exit_api_config_software():
    response = {
        'redirect_url':'/'
    }
    return jsonify(response)

@api_config_software.route("/config_software",strict_slashes=False)
def config_software():
    cam_basler.disable_send_video() #dung luong gui video khi nguoi dung vao lai
    data_information = OilDetectionSystem()
    data_send_client = data_information.to_dict()
    return jsonify({"status":"200OK","data":data_send_client})

@api_config_software.route("/change_log",methods=["POST"],strict_slashes=False)
def change_log():
    data_change = request.get_json()
    status_log_img = data_change.get("log_img",True)
    status_log_product = data_change.get("log_product",True)
    status_log_software = data_change.get("log_software",True)
    data_information = OilDetectionSystem()
    data_information.update_open_btn(status_log_img,status_log_product,status_log_software)
    return jsonify({"status":"200OK"})

@api_config_com.route("/exit")
def exit_api_config_com():
    response = {
        'redirect_url':'/'
    }
    return jsonify(response)

@api_config_com.route("/get_list_com",strict_slashes=False)
def get_list_com():
    main_pc.click_page_html = 7 # Câu hình cổng com
    cam_basler.disable_send_video() #dung luong gui video khi nguoi dung vao lai
    arr_com = main_pc.obj_manager_serial.serial_com.show_list_port()
    data_connect = main_pc.obj_manager_serial.get_dict_data_send_server()
    return jsonify({"status":"200OK","data":arr_com,"data_connected":data_connect})

@api_config_com.route("/open_and_save_inf",methods=["POST"],strict_slashes=False)
def open_and_save_inf():
    data = request.get_json()
    # print(data)
    com_choose = data.get("com_choose",-1)
    baudrate_choose = data.get("baudrate_choose", -1)
    if baudrate_choose == -1 or com_choose == -1:
        print("Lỗi nhận dũ liệu")
        return jsonify({"error": "Không dữ liệu không hợp lệ"}), 400
    if not data:
        return jsonify({"error": "Không trống dữ liệu"}), 400
    com_choose = str(com_choose).strip()
    baudrate_choose = int(baudrate_choose)
    print("com_choose",com_choose,"baudrate_choose",baudrate_choose)
    status_config =  main_pc.obj_manager_serial.update_com(com_choose,baudrate_choose)
    if status_config:
        print("Đổi cổng thành công nha !!!!!!!!")
        main_pc.the_first_connect = True  # bat dau  reset lai gui 200 OK
        data_connect = main_pc.obj_manager_serial.get_dict_data_send_server()
        return jsonify({"status":"200OK","data":data_connect})
    else:
        return jsonify({"error": "Lỗi không mở được cổng com"}), 400


#--------------------------------------------------------Api_new_model----------------------------------------------

@api_new_model.route('/stop-video', methods=['POST'])
def stop_video():
    main_pc.click_page_html = 1
    print("Người dùng đã thoát khỏi trang Training Model")
    return "ok"
@api_new_model.route('/replay', methods=['GET'])
def handle_replay():
    main_pc.is_data_train = 1
    print("🔁 Người dùng đã nhấn nút replay!")
    return jsonify({
        "message": "Đã nhận tín hiệu từ nút Replay",
        "status": "ok"
    })
@api_new_model.route("/run_point",methods=['POST'])
def run_point():
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')
    z = data.get('z')
    brightness = data.get('brightness')
    data_send = f"cmd:{x},{y},{z},{brightness}"
    print(f'x ={x}, y = {y}, z = {z} brightness ={brightness}')
    queue_rx_web_api.put(data_send)  # //Can than Request nhieu de bi day
    return jsonify({"message": "Ok"})

@api_new_model.route("/run_all_points", methods=["POST"])
def run_all_points():
    data = request.get_json()
    points = data.get("points", [])
    print(f"📥 Nhận {len(points)} điểm dầu:")
    for i, p in enumerate(points):
        print(f"  • Điểm {i+1}: x={p['x']}, y={p['y']}, z={p['z']}, k={p['k']}")
        data_send = f"cmd:{p['x']},{p['y']},{p['z']},{p['k']}"
        queue_rx_web_api.put(data_send)
        time.sleep(2)
    return jsonify({"message": f"Đã nhận {len(points)} điểm dầu"})
@api_new_model.route("/exit-training")
def exit_training():
    main_pc.click_page_html = 1
    print("Người dùng đã thoát khỏi trang Training Model")
    return redirect(url_for("main.show_main"))
# @api_new_model.route("/get_status")
# def get_status():
#     param = request.args.get("param1")
#     print(f"Client hỏi trạng thái với param1 = {param}")
#     if param == "status_connect":
#         print("Trạng thái connect hiện tại ",main_pc.STATUS_CHECK_CONNECT)
#         if(main_pc.STATUS_CHECK_CONNECT==0 ):   #trang thai ket noi
#             return "0"
#         elif(main_pc.STATUS_CHECK_CONNECT==1):
#             return "1"
#         else:
#             return "2"
@api_new_model.route('/submit', methods=['POST'])
def submit():
    """Training khong the anh huong truc tiep den file chay hayg lam tap trung vao master lay master."""
    form_data = request.form
    status_check_submit = func.Check_form_data(form_data)  #status_check_submit co thể la typeid
    print(status_check_submit)
    if status_check_submit:
        queue_tx_web_log.put("🔔Dữ liệu hợp lệ")
        queue_tx_web_log.put("🔔Tiến hành Traing Data")
        #Gui Tin hieu vao file main
        main_pc.is_data_train = 1
    else:
        queue_tx_web_log.put("🔔Dữ liệu không hợp lệ")
        return "X Dữ liệu không hợp lệ"
    return "✅ Đã nhận dữ liệu"
@api_new_model.route("/training-model")
def take_photo_trainning_model():
    func.clear_queue(queue_rx_web_api)   #rst bufff nhan
    main_pc.click_page_html = 2           #Training model
    return render_template("take_photo.html")
#--------------------------------------------------------end Api----------------------------------------------
app.register_blueprint(main_html)
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(api_new_model, url_prefix="/api_new_model")
app.register_blueprint(api_choose_master, url_prefix="/api_choose_master")
app.register_blueprint(api_take_master, url_prefix="/api_take_master")
app.register_blueprint(api_run_application, url_prefix="/api_run_application")
app.register_blueprint(api_new_product, url_prefix="/api_new_product")
app.register_blueprint(api_add_master, url_prefix="/api_add_master")
app.register_blueprint(api_config_camera, url_prefix="/api_config_camera")
app.register_blueprint(api_config_com, url_prefix="/api_config_com")
app.register_blueprint(api_config_software, url_prefix="/api_config_software")


from shared_queue import queue_accept_capture
cam_basler = BaslerCamera(queue_accept_capture,socketio,config_file="Camera_25129678.pfs")

if __name__ == "__main__":
    import main_pc
    from shared_queue import queue_rx_web_api,queue_tx_web_log,queue_tx_web_main
    import threading
    threading.Thread(target=stream_logs,daemon = True).start()
    threading.Thread(target=stream_img,daemon = True).start()
    threading.Thread(target = stream_frames,daemon=True).start()
    socketio.run(app, host="0.0.0.0", port=5000, debug=False, use_reloader=False)
    print("Đã thoát chương trình chính")



