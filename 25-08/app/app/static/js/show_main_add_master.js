import {
    postData,headerMasterAdd,current_panner,setCurrentPanner,
    scroll_content,set_Z_index_canvas_show,canvas_show,ctx_show,ctx,logSocket
} from "./show_main_status.js";

let divCreateList = []; // biến toàn cục luu mang div

const socket_realtime = io("/data_add_master");
const videoSocket = io("/video");

const btn_add_master = document.getElementById("btn-add-master");
const log_master =  document.getElementById("log_add_master");
const anonymous =  document.getElementById("anonymous");
const run_all_master = document.getElementById("run_all_master");
const exit_add_master =  document.getElementById("exit-add-master");
const add_master = document.getElementById("panel-add-master");
let isOpenShowCamVideo = true;
let prevUrl = null;
let isSending = false;
let Max_X = 0;
let Max_Y = 0;
let Max_Z = 0;
let Max_K= 0;

run_all_master.addEventListener("click",()=>{
  postData("api_add_master/run_all_master", { "status": "run"}).then(data => {
          if(data.status_run == "oke"){
            console.log("Chạy thành công");
          }
          else if(data.status_run == "erro"){
            console.log("Chạy all không thành công");
          }
          videoSocket.on("camera_frame", function(data) {
            console.log("ewqeewewewewewqewqewqewq");
    if(isOpenShowCamVideo){                          // data.image là base64
          const img = new Image();
          img.onload = () => {                                             // Khởi tạo canvas kích thước phù hợp
                canvas_show.width = 1328; // hoặc img.width
                canvas_show.height = 830;  // hoặc img.height
                ctx_show.drawImage(img, 0, 0, canvas_show.width , canvas_show.height);
                if (prevUrl) URL.revokeObjectURL(prevUrl);
          };
          img.src = "data:image/jpeg;base64," + data.image;
          console.log("wqewqeqwewewq",img.src);
      }
    });
  });
});
     

exit_add_master.addEventListener("click",()=>{
      fetch('/api_add_master/exit')
      .then(response => {
          if (response.redirected) {
              window.location.href = response.url;
          } else {
              response.json().then(data => {
                  window.location.href = data.redirect_url;
              });
          }
      });
});

btn_add_master.addEventListener("click",function(){

    console.log("Đã nhấn vào nút thêm master");
    const div_create = document.createElement("div");
    div_create.className = "div-index-img-mater";

    const h_create = document.createElement("p");
    h_create.innerText = `Ảnh master`;
    h_create.className = "p-index-img-master";

    const img = document.createElement("img");
    img.src = "./static/img/plus (2).png";
    img.alt = "Click vào đây để chụp ảnh";
    img.style.padding = "35px";
    img.style.width = "200px";
    divCreateList.push(div_create);

    div_create.appendChild(img);
    div_create.appendChild(h_create);
    scroll_content.appendChild(div_create); 
    div_create.addEventListener("click",function(){
             clearn_div(divCreateList);
            div_create.classList.add("div_click");
            console.log("Đã nhấn vào ảnh master mới để thêm master");
            const index = Array.from(scroll_content.children).indexOf(this);
            console.log("Ảnh master đang chỉ tới là 2",index);
            //Tao ra cac nut nhan
            create_table_controler(index);
            isOpenShowCamVideo =  true;  //Tat cam khi la san pham cu
            const input_x = document.getElementById(`input-x-${index}`);input_x.type = "number";
            const input_y = document.getElementById(`input-y-${index}`);input_y.type = "number";
            const input_z = document.getElementById(`input-z-${index}`);input_z.type = "number";
            const input_k = document.getElementById(`input-k-${index}`);input_k.type = "number";
            input_x.value = 0
            input_y.value = 0
            input_z.value = 0
            input_k.value = 0
            const btn_increase_x = document.getElementById(`btn-inc-x-${index}`);
            const btn_decrease_x = document.getElementById(`btn-dec-x-${index}`);
            const btn_increase_y = document.getElementById(`btn-inc-y-${index}`);
            const btn_decrease_y = document.getElementById(`btn-dec-y-${index}`);
            const btn_increase_z = document.getElementById(`btn-inc-z-${index}`);
            const btn_decrease_z = document.getElementById(`btn-dec-z-${index}`);
            const btn_increase_k = document.getElementById(`btn-inc-k-${index}`);
            const btn_decrease_k = document.getElementById(`btn-dec-k-${index}`);

            const btn_run          = document.getElementById(`btn-run-${index}`);
            const btn_capture      = document.getElementById(`btn-capture-${index}`);
            const btn_erase_master = document.getElementById(`btn-erase-master-${index}`);

                // Khai báo các handler (function reference)
            const handleIncreaseX = () => HandleClickBtnIncrease_X(input_x, Max_X, input_x.value, input_y.value, input_z.value, input_k.value);
            const handleDecreaseX = () => HandleClickBtnDecrease_X(input_x, Max_X, input_x.value, input_y.value, input_z.value, input_k.value);

            const handleIncreaseY = () => HandleClickBtnIncrease_Y(input_y, Max_Y, input_x.value, input_y.value, input_z.value, input_k.value);
            const handleDecreaseY = () => HandleClickBtnDecrease_Y(input_y, Max_Y, input_x.value, input_y.value, input_z.value, input_k.value);

            const handleIncreaseZ = () => HandleClickBtnIncrease_Z(input_z, Max_Z, input_x.value, input_y.value, input_z.value, input_k.value);
            const handleDecreaseZ = () => HandleClickBtnDecrease_Z(input_z, Max_Z, input_x.value, input_y.value, input_z.value, input_k.value);

            const handleIncreaseK = () => HandleClickBtnIncrease_K(input_k, Max_K, input_x.value, input_y.value, input_z.value, input_k.value);
            const handleDecreaseK = () => HandleClickBtnDecrease_K(input_k, Max_K, input_x.value, input_y.value, input_z.value, input_k.value);

            const handleRun       = () => HandleClickBtnRun(input_x.value, input_y.value, input_z.value, input_k.value);
            const handleCapture   = () => HandleClickBtnCapture(index, input_x.value, input_y.value, input_z.value, input_k.value);
            const handleErase     = () => HandleClickBtnEraseMaster(index);

            // Gắn event (trước khi add thì remove trước để tránh trùng)
            btn_increase_x.removeEventListener("click", handleIncreaseX);
            btn_increase_x.addEventListener("click", handleIncreaseX);

            btn_decrease_x.removeEventListener("click", handleDecreaseX);
            btn_decrease_x.addEventListener("click", handleDecreaseX);

            btn_increase_y.removeEventListener("click", handleIncreaseY);
            btn_increase_y.addEventListener("click", handleIncreaseY);

            btn_decrease_y.removeEventListener("click", handleDecreaseY);
            btn_decrease_y.addEventListener("click", handleDecreaseY);

            btn_increase_z.removeEventListener("click", handleIncreaseZ);
            btn_increase_z.addEventListener("click", handleIncreaseZ);

            btn_decrease_z.removeEventListener("click", handleDecreaseZ);
            btn_decrease_z.addEventListener("click", handleDecreaseZ);

            btn_increase_k.removeEventListener("click", handleIncreaseK);
            btn_increase_k.addEventListener("click", handleIncreaseK);

            btn_decrease_k.removeEventListener("click", handleDecreaseK);
            btn_decrease_k.addEventListener("click", handleDecreaseK);

            btn_run.removeEventListener("click", handleRun);
            btn_run.addEventListener("click", handleRun);

            btn_capture.removeEventListener("click", handleCapture);
            btn_capture.addEventListener("click", handleCapture);

            btn_erase_master.removeEventListener("click", handleErase);
            btn_erase_master.addEventListener("click", handleErase);

    });  
});



// sự kiện nhấn chuyển tab
headerMasterAdd.addEventListener("click",function(){
      set_Z_index_canvas_show(2);
      console.log("current_panner",current_panner);
      console.log("Chuyển sang trang thêm mẫu");
      scroll_content.innerHTML = ""; 
      postData("api_add_master", { "status": "on" }).then(data => {
      renderMaster(data)
      });
      if (current_panner === add_master) return;
      current_panner.classList.remove("active");
      current_panner.style.zIndex = 1;
      add_master.classList.add("active");
      add_master.style.zIndex = 2;
      setCurrentPanner(add_master);
});

function clearn_div(div_card_arr) {
  if (!div_card_arr) return;
  for (let i = 0; i < div_card_arr.length; i++) {
    div_card_arr[i].classList.remove("div_click");
  }
}
socket_realtime.on("data_realtime", (data) => {
  console.log("data",data);
  renderMaster(data);
});

function renderMaster(data) {
            const imgList = data?.path_arr_img;
            const list_point  = data?.arr_point;
            create_table_product(data)
            //if (!imgList || imgList.length === 0) {log_master.innerHTML = "Hệ thống chưa có ảnh master nào";console.log("Hệ thống chưa có ảnh master nào");return}
            scroll_content.innerHTML = "";
            console.log("Danh sách điểm:", list_point);
            console.log("Danh sách ảnh:", imgList);
            imgList.forEach((imgPath, index) => {
                const div_create = document.createElement("div");
                div_create.className = "div-index-img-mater";
                const h_create = document.createElement("p");
                h_create.innerText = `Ảnh master ${index}`;
                h_create.className = "p-index-img-master";

                const img = document.createElement("img");
                img.src = `${imgPath}?t=${Date.now()}`;  // dam bao  goi moi nhat
                img.alt = "Ảnh sản phẩm";
                img.style.width = "200px";
                img.style.margin = "10px";

                div_create.appendChild(img);
                div_create.appendChild(h_create);
                scroll_content.appendChild(div_create);
                divCreateList.push(div_create);
                div_create.addEventListener("click",function(){
                      clearn_div(divCreateList);
                      div_create.classList.add("div_click");

                      ctx.clearRect(0, 0, 1328, 830);
                      const show_img = new Image();
                      canvas_show.width = 1328;
                      canvas_show.height = 830;
                      show_img.src = `${imgPath}?t=${Date.now()}`;
                      show_img.onload = () => {
                            ctx_show.drawImage(show_img, 0, 0, 1328, 830);
                      };
                      const index = Array.from(scroll_content.children).indexOf(this);
                      console.log("Ảnh master đang chỉ tới là 1",index);
                      create_table_controler(index);
                      isOpenShowCamVideo = false; // Bat cam khi la san pham moi

                      const input_x = document.getElementById(`input-x-${index}`);input_x.type = "number";
                      const input_y = document.getElementById(`input-y-${index}`);input_y.type = "number";
                      const input_z = document.getElementById(`input-z-${index}`);input_z.type = "number";
                      const input_k = document.getElementById(`input-k-${index}`);input_k.type = "number";

                      const btn_increase_x = document.getElementById(`btn-inc-x-${index}`);
                      const btn_decrease_x = document.getElementById(`btn-dec-x-${index}`);
                      const btn_increase_y = document.getElementById(`btn-inc-y-${index}`);
                      const btn_decrease_y = document.getElementById(`btn-dec-y-${index}`);
                      const btn_increase_z = document.getElementById(`btn-inc-z-${index}`);
                      const btn_decrease_z = document.getElementById(`btn-dec-z-${index}`);
                      const btn_increase_k = document.getElementById(`btn-inc-k-${index}`);
                      const btn_decrease_k = document.getElementById(`btn-dec-k-${index}`);

                      const btn_run          = document.getElementById(`btn-run-${index}`);
                      const btn_capture      = document.getElementById(`btn-capture-${index}`);
                      const btn_erase_master = document.getElementById(`btn-erase-master-${index}`);
                      if (
                          list_point[index]?.x == null ||
                          list_point[index]?.y == null ||
                          list_point[index]?.z == null ||
                          list_point[index]?.brightness == null
                        ) 
                              {
                                input_x.value = list_point[index]?.x ?? 0;
                                input_y.value = list_point[index]?.y ?? 0;
                                input_z.value = list_point[index]?.z ?? 0;
                                input_k.value = list_point[index]?.brightness ?? 0;
                              } else {
                                input_x.value = list_point[index].x;
                                input_y.value = list_point[index].y;
                                input_z.value = list_point[index].z;
                                input_k.value = list_point[index].brightness;
                              }
                             
                      // Khai báo các handler (function reference)
                      const handleIncreaseX = () => HandleClickBtnIncrease_X(input_x, Max_X, input_x.value, input_y.value, input_z.value, input_k.value);
                      const handleDecreaseX = () => HandleClickBtnDecrease_X(input_x, Max_X, input_x.value, input_y.value, input_z.value, input_k.value);

                      const handleIncreaseY = () => HandleClickBtnIncrease_Y(input_y, Max_Y, input_x.value, input_y.value, input_z.value, input_k.value);
                      const handleDecreaseY = () => HandleClickBtnDecrease_Y(input_y, Max_Y, input_x.value, input_y.value, input_z.value, input_k.value);

                      const handleIncreaseZ = () => HandleClickBtnIncrease_Z(input_z, Max_Z, input_x.value, input_y.value, input_z.value, input_k.value);
                      const handleDecreaseZ = () => HandleClickBtnDecrease_Z(input_z, Max_Z, input_x.value, input_y.value, input_z.value, input_k.value);

                      const handleIncreaseK = () => HandleClickBtnIncrease_K(input_k, Max_K, input_x.value, input_y.value, input_z.value, input_k.value);
                      const handleDecreaseK = () => HandleClickBtnDecrease_K(input_k, Max_K, input_x.value, input_y.value, input_z.value, input_k.value);

                      const handleRun       = () => HandleClickBtnRun(input_x.value, input_y.value, input_z.value, input_k.value);
                      const handleCapture   = () => HandleClickBtnCapture(index, input_x.value, input_y.value, input_z.value, input_k.value);
                      const handleErase     = () => HandleClickBtnEraseMaster(index);

                      // Gắn event (trước khi add thì remove trước để tránh trùng)
                      btn_increase_x.removeEventListener("click", handleIncreaseX);
                      btn_increase_x.addEventListener("click", handleIncreaseX);

                      btn_decrease_x.removeEventListener("click", handleDecreaseX);
                      btn_decrease_x.addEventListener("click", handleDecreaseX);

                      btn_increase_y.removeEventListener("click", handleIncreaseY);
                      btn_increase_y.addEventListener("click", handleIncreaseY);

                      btn_decrease_y.removeEventListener("click", handleDecreaseY);
                      btn_decrease_y.addEventListener("click", handleDecreaseY);

                      btn_increase_z.removeEventListener("click", handleIncreaseZ);
                      btn_increase_z.addEventListener("click", handleIncreaseZ);

                      btn_decrease_z.removeEventListener("click", handleDecreaseZ);
                      btn_decrease_z.addEventListener("click", handleDecreaseZ);

                      btn_increase_k.removeEventListener("click", handleIncreaseK);
                      btn_increase_k.addEventListener("click", handleIncreaseK);

                      btn_decrease_k.removeEventListener("click", handleDecreaseK);
                      btn_decrease_k.addEventListener("click", handleDecreaseK);

                      btn_run.removeEventListener("click", handleRun);
                      btn_run.addEventListener("click", handleRun);

                      btn_capture.removeEventListener("click", handleCapture);
                      btn_capture.addEventListener("click", handleCapture);

                      btn_erase_master.removeEventListener("click", handleErase);
                      btn_erase_master.addEventListener("click", handleErase);
                });
        });
}
function HandleClickBtnIncrease_X(element,max_element,input_x_value,input_y_value,input_z_value,input_k_value){
       let status_check = CheckData(element,"X",input_x_value,max_element);
       if(status_check){
          console.log("input_x_value", input_x_value);
         element.value = parseInt(input_x_value) + 1;
         HandleClickBtnRun(element.value,input_y_value,input_z_value,input_k_value);
       }

}
function HandleClickBtnDecrease_X(element,max_element,input_x_value,input_y_value,input_z_value,input_k_value) {
    let new_value = parseInt(input_x_value) - 1;
    let status_check = CheckData(element,"X", new_value, max_element);
    if (status_check) {
        element.value = new_value; 
        HandleClickBtnRun(element.value,input_y_value,input_z_value,input_k_value);
    } else {
        element.value = 0; 
    }
}                           
function HandleClickBtnIncrease_Y(element,max_element,input_x_value,input_y_value,input_z_value,input_k_value){
       let status_check = CheckData(element,"Y",input_y_value,max_element);
       if(status_check){
         element.value = parseInt(input_y_value) + 1;
          HandleClickBtnRun(input_x_value,element.value,input_z_value,input_k_value);
       }
}
function HandleClickBtnDecrease_Y(element,max_element,input_x_value,input_y_value,input_z_value,input_k_value){
    let new_value = parseInt(input_y_value) - 1;
    let status_check = CheckData(element,"Y", new_value, max_element);
    if (status_check) {
        element.value = new_value; 
        HandleClickBtnRun(input_x_value,element.value,input_z_value,input_k_value);
    } else {
        element.value = 0; 
    }
}
function HandleClickBtnIncrease_Z(element,max_element,input_x_value,input_y_value,input_z_value,input_k_value){
        let status_check = CheckData(element,"Z",input_z_value,max_element);
        if(status_check){
          element.value = parseInt(input_z_value) + 1;
          HandleClickBtnRun(input_x_value,input_y_value,element.value,input_k_value);
        }
}
function HandleClickBtnDecrease_Z(element,max_element,input_x_value,input_y_value,input_z_value,input_k_value){
    let new_value = parseInt(input_z_value) - 1;
    let status_check = CheckData(element,"Z", new_value, max_element);
    if (status_check) {
        element.value = new_value; 
        HandleClickBtnRun(input_x_value,input_y_value,element.value,input_k_value);
    } else {
        element.value = 0; 
    }

}
function HandleClickBtnIncrease_K(element,max_element,input_x_value,input_y_value,input_z_value,input_k_value){
        let status_check = CheckData(element,"K",input_k_value,max_element);
        if(status_check){
          element.value = parseInt(input_k_value) + 1;
           HandleClickBtnRun(input_x_value,input_y_value,input_z_value,element.value);
    } 
}
function HandleClickBtnDecrease_K(element,max_element,input_x_value,input_y_value,input_z_value,input_k_value){
    let new_value = parseInt(input_k_value) - 1;
    let status_check = CheckData(element,"K", new_value, max_element);
    if (status_check) {
        element.value = new_value; 
        HandleClickBtnRun(input_x_value,input_y_value,input_z_value,element.value);
    } else {
        element.value = 0; 
    }
}



function HandleClickBtnRun(input_x_value,input_y_value,input_z_value,input_k_value){
    let status_check = validatePoint(input_x_value,input_y_value,input_z_value,input_k_value,Max_X,Max_Y,Max_Z,Max_K);
    if(!status_check){
      console.log("Dữ liệu không hợp lệ");
      return;
    }
    console.log("✅Dữ liệu hợp lệ.");
    log_master.innerHTML = "✅Dữ liệu hợp lệ.";
    sendPoint(input_x_value,input_y_value,input_z_value,input_k_value);
    isOpenShowCamVideo = true;         
      //nao xong sẽ sưa phần nến có kết nối với cam thì show video nếu không có thì show ảnh hiện có
    videoSocket.on("camera_frame", function(data) {
        console.log("ewqeewewewewewqewqewqewq");
        if(isOpenShowCamVideo){                          // data.image là base64
            const img = new Image();
            img.onload = () => {                                             // Khởi tạo canvas kích thước phù hợp
                  canvas_show.width = 1328; // hoặc img.width
                  canvas_show.height = 830;  // hoặc img.height
                  ctx_show.drawImage(img, 0, 0, canvas_show.width , canvas_show.height);
                  if (prevUrl) URL.revokeObjectURL(prevUrl);
            };
            img.src = "data:image/jpeg;base64," + data.image;
            }
        });
}

function HandleClickBtnCapture(index,x,y,z,k){
    console.log("Đã nhấn vào chụp")
    postData("api_add_master/capture_master", { "status": "200OK","index":index,"x":x,"y":y,"z":z,"k":k}).then(data => {
    console.log("Server response: " + data);
    });
}
function HandleClickBtnEraseMaster(index){
    fetch('/api_add_master/erase_index', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({"index":index})
    })
    .then(response => response.json())
    .then(data => 
     {
         const show_img = new Image();
         canvas_show.width = 1328;
         canvas_show.height = 830;
         show_img.onload = () => {
              ctx_show.drawImage(show_img, 0, 0, 1328, 830);};                         
        console.log("Trạng thái:",data.message)
        console.log(`✅ Đã gửi điểm ${index} đến thiết bị. Phản hồi: ${data.message}`);
    })
    .catch(error => {
      console.error('Lỗi khi gửi điểm:', error);
      alert('❌ Gửi dữ liệu thất bại.');
    });
}
async function sendPoint(x, y, z, brightness) {
    if (isSending) {
      console.warn("⚠️ Đang gửi dữ liệu, vui lòng đợi...");
      return null; // bỏ qua nếu đang gửi
    }
    isSending = true; // đánh dấu đang gửi
    try {
      const response = await fetch(`/api_new_model/run_point`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ x, y, z, brightness })
      });
      const data = await response.json();
      console.log("Trạng thái:", data.message);
      console.log(`✅ Đã gửi điểm đến thiết bị. Phản hồi: ${data.message}`);
      return data; // trả về để hàm khác dùng tiếp
    } catch (error) {
      console.error('Lỗi khi gửi điểm:', error);
      alert('❌ Gửi dữ liệu thất bại.');
      return null;
    } finally {
      isSending = false; // reset cờ, cho phép gửi tiếp
    }
}

function CheckData(element,str_name, data, value_max) {
    if (str_name == null || data == null || value_max == null ||element.value == ""||element.value == null ) {
        console.log(`⚠️ Dữ liệu "${str_name}" không có giá trị`);
        log_master.innerHTML = `⚠️ Dữ liệu "${str_name}" không có giá trị`;
        element.value = 0;
        return false;
    }
    if (data < 0) {
        console.log(`❌ Giá trị "${str_name}" phải lớn hơn hoặc bằng 0`);
        log_master.innerHTML = `❌ Giá trị "${str_name}" phải lớn hơn hoặc bằng 0`;
        element.value = 0;
        console.log("vao day");
        return false;
    }

    if (data >= value_max) {
        console.log(`❌ Giá trị "${str_name}" phải nhỏ hơn hoặc bằng ${value_max}`);
        log_master.innerHTML = `❌ Giá trị "${str_name}" phải nhỏ hơn hoặc bằng ${value_max}`;
         element.value = value_max;
        return false;
    }
    console.log("data",data);
    console.log(`✅ Giá trị ${str_name} hợp lệ`);
    log_master.innerHTML = `✅ Giá trị ${str_name} hợp lệ`;
    return true;
}
// Hàm kiểm tra một giá trị có hợp lệ hay không
function isInvalid(value) {
  let num = Number(value);

  return (
    value === null ||        // null
    value === undefined ||   // undefined
    value === "" ||          // rỗng
    isNaN(num) ||            // không phải số
    !Number.isInteger(num)   // không phải số nguyên
  );
}

// Hàm validate toàn bộ điểm
function validatePoint(x, y, z, brightness, Limit_x, Limit_y, Limit_z, Limit_k) {
    console.log("Dữ liệu trước khi chạy",x, y, z, brightness, Limit_x, Limit_y, Limit_z, Limit_k);
    if (
      isInvalid(x) || 
      isInvalid(y) || 
      isInvalid(z) || 
      isInvalid(brightness) ||
      isInvalid(Limit_x) ||
      isInvalid(Limit_y) ||
      isInvalid(Limit_z) ||
      isInvalid(Limit_k)
    ) {
      log_master.innerHTML = `❌ Các giá trị X, Y, Z, K và giới hạn phải là số nguyên hợp lệ và không được để trống`;
      console.log(`❌ Các giá trị X, Y, Z, K và giới hạn phải là số nguyên hợp lệ và không được để trống`);
      return false;  // trả về false thay vì string
    }

    // Ép kiểu int sau khi đã check hợp lệ
    x = parseInt(x);
    y = parseInt(y);
    z = parseInt(z);
    brightness = parseInt(brightness);
    Limit_x = parseInt(Limit_x);
    Limit_y = parseInt(Limit_y);
    Limit_z = parseInt(Limit_z);
    Limit_k = parseInt(Limit_k);

    // Các điều kiện giới hạn
    if (x < 0 || y < 0 || z < 0 || brightness < 0) {
      log_master.innerHTML = `❌ Giá trị X, Y, Z, K phải lớn hơn hoặc bằng 0`;
      console.log(`❌ Giá trị X, Y, Z, K phải lớn hơn hoặc bằng 0`);
      return false;
    }
    if (x > Limit_x) {
       log_master.innerHTML = `❌ Giá trị X phải nhỏ hơn hoặc bằng ${Limit_x}`
      console.log(`❌ Giá trị X phải nhỏ hơn hoặc bằng ${Limit_x}`);
      return false;
    }
    if (y > Limit_y) {
      log_master.innerHTML = `❌ Giá trị Y phải nhỏ hơn hoặc bằng ${Limit_y}`
      console.log(`❌ Giá trị Y phải nhỏ hơn hoặc bằng ${Limit_y}`);
      return false;
    }
    if (z > Limit_z) {
       log_master.innerHTML = `❌ Giá trị Z phải nhỏ hơn hoặc bằng ${Limit_z}`;
      console.log(`❌ Giá trị Z phải nhỏ hơn hoặc bằng ${Limit_z}`);
      return false;
    }
    if (brightness > Limit_k) {
      log_master.innerHTML = `❌ Giá trị Z phải nhỏ hơn hoặc bằng ${Limit_z}`;
      console.log(`❌ Giá trị ánh sáng (K) phải nhỏ hơn hoặc bằng ${Limit_k}`);
      return false;
    }
    console.log("✅ Dữ liệu hợp lệ");
    return true; // hợp lệ
}
function create_table_controler(index){
                          // Thêm các input
                          anonymous.innerHTML = "";
      anonymous.appendChild(createInputRow("Nhập X", "Nhập X > 0", `input-x-${index}`));
      anonymous.appendChild(createInputRow("Nhập Y", "Nhập Y > 0", `input-y-${index}`));
      anonymous.appendChild(createInputRow("Nhập Z", "Nhập Z > 0", `input-z-${index}`));
      anonymous.appendChild(createInputRow("Mức sáng", "Nhập độ sáng > 0",`input-k-${index}`));

      anonymous.appendChild(createButtonRow([
          {id: `btn-inc-x-${index}`, icon: "../static/img/add1.png", alt: "Tăng X", text: "Tăng X"},
          {id: `btn-dec-x-${index}`, icon: "../static/img/minus.png", alt: "Giảm X", text: "Giảm X"}
      ]));

      anonymous.appendChild(createButtonRow([
          {id: `btn-inc-y-${index}`, icon: "../static/img/add1.png", alt: "Tăng Y", text: "Tăng Y"},
          {id: `btn-dec-y-${index}`, icon: "../static/img/minus.png", alt: "Giảm Y", text: "Giảm Y"}
      ]));

      anonymous.appendChild(createButtonRow([
          {id: `btn-inc-z-${index}`, icon: "../static/img/add1.png", alt: "Tăng Z", text: "Tăng Z"},
          {id: `btn-dec-z-${index}`, icon: "../static/img/minus.png", alt: "Giảm Z", text: "Giảm Z"}
      ]));
      anonymous.appendChild(createButtonRow([
          {id: `btn-inc-k-${index}`, icon: "../static/img/add1.png", alt: "Tăng ánh sáng", text: "Tăng ánh sáng"},
          {id: `btn-dec-k-${index}`, icon: "../static/img/minus.png", alt: "Giảm ánh sáng", text: "Giảm ánh sáng"}
      ]));

      anonymous.appendChild(createButtonRow([
          {id: `btn-run-${index}`, icon: "../static/img/check.png", alt: "Chạy", text: "Chạy"},
          {id: `btn-capture-${index}`, icon: "../static/img/camera.png", alt: "Chụp", text: "Chụp"},
          {id: `btn-erase-master-${index}`, icon: "../static/img/running.png", alt: "Xóa Master", text: "Xóa Master này"}
      ]));                  
      // Hiện div anonymous
      anonymous.style.display = "block";
}

function createInputRow(labelText, placeholder, id = null) {
    const div = document.createElement("div");
    div.className = "Alight-items-x";

    const label = document.createElement("label");
    label.innerText = labelText;
    if (id) label.setAttribute("for", id);

    const input = document.createElement("input");
    input.type = "number";
    input.placeholder = placeholder;
    if (id) input.id = id;   // ✅ gán id cho input

    div.appendChild(label);
    div.appendChild(input);
    return div;
}

function createButtonRow(buttons) {
    const div = document.createElement("div");
    div.className = "Alight-items-x";

    buttons.forEach(btn => {
        const button = document.createElement("button");
        button.className = "btn";
        if (btn.id) button.id = btn.id;   // ✅ gán id cho button

        const img = document.createElement("img");
        img.src = btn.icon;
        img.alt = btn.alt;

        button.appendChild(img);
        button.append(` ${btn.text}`);
        div.appendChild(button);
    });

    return div;
}

function create_table_product(data) {
       const tbody = document.querySelector(".product-table tbody");
       if (!tbody){
        console.log("Bảng không tồn tại");
        return;
       }
       tbody.innerHTML = "";
       let log = data?.inf_product;
        console.log("Dữ liệu nhận được là ",log);
       let id =  log?.list_id[0];
       let name   = log?.list_name[0];
       let x = log?.xyz[0][0];
       Max_X = x;
       let y = log?.xyz[0][1];
       Max_Y = y;
       let z = log?.xyz[0][2];
       Max_Z = z;
       let k = 100;
       Max_K = k;
      //  console.log(name)
      //  console.log(id)
      //  console.log(x)
      //  console.log(y)
      //  console.log(z)
      const row = document.createElement("tr");
      row.innerHTML =  
      `<td>${name}</td>
       <td>${x}</td>
       <td>${y}</td>
       <td>${z}</td>
       <td>${k}</td>
      `;
      tbody.appendChild(row);
};

//Log sản phẩm
logSocket.on("log_message", function (data) {
       const tbody = document.querySelector(".product-table tbody");
       if (!tbody){
        console.log("Bảng không tồn tại");
        return;
       }
       tbody.innerHTML = "";
       let log = data.log_add_master;
          console.log("Dữ liệu nhận được là ",log);
       let id =  log?.list_id[0];
       let name   = log?.list_name[0];
       let x = log?.xyz[0][0];
       let y = log?.xyz[0][1];
       let z = log?.xyz[0][2];
       let k = 100;
      //  console.log(name)
      //  console.log(id)
      //  console.log(x)
      //  console.log(y)
      //  console.log(z)
      const row = document.createElement("tr");
      row.innerHTML =  
      `<td>${name}</td>
       <td>${x}</td>
       <td>${y}</td>
       <td>${z}</td>
       <td>${k}</td>
      `;
      tbody.appendChild(row);
});

// Log dữ liệu
logSocket.on("log_data", function (data) {
   console.log(data.log);
   if (data.log){
        log_master.innerText += data.log;
   }
});
  
 

 

  




function handleStart(index,inputs) {
  // Lấy giá trị từ các input
  const x = parseFloat(inputs.X.value);
  const y = parseFloat(inputs.Y.value);
  const z = parseFloat(inputs.Z.value);
  const brightness = parseFloat(inputs.K.value); // K là độ sáng

  // const errorMsg = validatePoint(index, x, y, z, brightness);  thay doi
  // if (errorMsg) {
  //   alert(errorMsg);
  //   return;
  // }

  // ✅ Gửi dữ liệu tới server
  fetch('/api_new_model/run_point', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      x: x,
      y: y,
      z: z,
      brightness: brightness
    })
  })
    .then(response => response.json())
    .then(data => {
      console.log("Trạng thái:",data.message)
      console.log(`✅ Đã gửi điểm ${index} đến thiết bị. Phản hồi: ${data.message}`);
    })
    .catch(error => {
      console.error('Lỗi khi gửi điểm:', error);
      alert('❌ Gửi dữ liệu thất bại.');
    });
}
