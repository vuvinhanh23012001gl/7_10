
import {
  chooseProductBtn,
  headerMasterTake,
  btn_close,
  add_product,
  out_app,
  coordinate,
  scroll_content,
  scroll_container,
  btn_left,
  btn_right,
  log,
  table_write_data,
  part_table_log,
  btn_square,
  btn_circle,
  btn_undo,
  btn_erase,
  btn_check,
  select_min,
  btn_accept_and_send,
  postData,
  current_panner,
  setCurrentPanner,
  index_img_current,
  set_index_img_current,
  set_Z_index_canvas_show,canvas_img_show,ctx,canvas_img_show_oke,ctx_oke,logSocket
} from "./show_main_status.js";
//logSocket se nhan tin hieu server nhận dữ liệu thành công hiển thị lên log
// CONSTANT    
const SCROLL_STEP = 300;
let index_point_current = 0
let flag_index_choose_last = 1 //giup gan gia tri lan dau cho index_choose_last
let index_choose_last = null ; //
let number_img_receive =  0
let hoveredRectIndex = -1;
let rotateStartMouseAngle = 0;
let currentRotation = 0;
let isRotating = false;
let is_hover_circle = false;
let hoveredCircleIndex = -1;
let isDraggingCircle = false;
let dragOffsetX = 0;
let dragOffsetY = 0;
let isDraggingRectWithRightClick = false;
let dragRectOffsetX = 0;
let dragRectOffsetY = 0;
let draggingRectIndex = -1;
let is_hover_square = false;
let check_select = null;
let check_Select_shape = null;
let check_no_Select_shape_1 = 0;
let check_no_Select_shape_2 = 0;
let check_no_Select_shape_3 = 0;
let is_square_active = false;
let is_circle_active = false;
let is_pentagon_active = false;
let shapes_all = {};
let shapes = [];
let mode = null;
let startX = 0, startY = 0, endX = 0, endY = 0;
let isDrawing = false;
let is_screen_frame_load_data = true;

canvas_img_show.addEventListener("mousedown", handleMouseDown);
canvas_img_show.addEventListener("mousemove", handleMouseMove);
canvas_img_show.addEventListener("mouseup", handleMouseUp);
canvas_img_show.addEventListener("contextmenu", e => e.preventDefault());

// ==========================
// 3. Utility Functions
// ==========================

logSocket.on("log_take_master",(data)=>{
    let data_log  = data?.log;
    if (data_log){
        log.innerHTML  = `${data_log}<br>`;
    }
});






function check_no_select_shape(c1, c2, c3) {
  return c1 === 0 && c2 === 0 && c3 === 0;
}


function deactivateAllButtons() {
  is_square_active = false;
  is_circle_active = false;
  is_pentagon_active = false;
  check_no_Select_shape_1 = 0;
  check_no_Select_shape_2 = 0;
  check_no_Select_shape_3 = 0;
  btn_square.style.backgroundColor = "";
  btn_square.style.scale = "";
  btn_circle.style.backgroundColor = "";
  btn_circle.style.scale = "";
  mode = null;
  select_min.classList.remove("active");
}


// ==========================
// 4. Event Handlers
// ==========================

// window.addEventListener("beforeunload", function (e) {
//       e.preventDefault();  
// });
function normalizeShapes(data, width, height) {
  // clone để không làm thay đổi data gốc
  const result = JSON.parse(JSON.stringify(data));

  for (const key in data) {
    const item = result[key];
    if (!item.shapes) continue; // bỏ qua nếu không có shapes

    item.shapes.forEach(shape => {
      if (shape.type === "rect") {
        // chuẩn hóa x1, x2, y1, y2
        shape.x1 = shape.x1 / width;
        shape.x2 = shape.x2 / width;
        shape.y1 = shape.y1 / height;
        shape.y2 = shape.y2 / height;

        // nếu có corners thì normalize từng điểm
        if (shape.corners) {
          shape.corners = shape.corners.map(c => ({
            x: c.x / width,
            y: c.y / height
          }));
        }
      } else if (shape.type === "circle") {
        shape.cx = shape.cx / width;
        shape.cy = shape.cy / height;
        // scale bán kính theo width (nếu muốn chính xác hơn có thể dùng (width+height)/2)
        shape.r = shape.r / width;
      }
    });
  }

  return result;
}


btn_accept_and_send.addEventListener("click",()=>{
    // console.log("shapes_all_la",shapes_all);
    let is_oke = true;
    let copy = shapes
    if(flag_index_choose_last==1){
        index_choose_last = index_point_current;  //cai dat index lan dau
        flag_index_choose_last = 0;
    }
    // console.log("btn_accept_and_send" + index_point_current);   // index dem tu so 0
    next_page_img(index_point_current,index_choose_last);
    index_choose_last = index_point_current;
    reredrawAll(copy);
    let status_oke = true;
    log.innerText = "";
    for(let i = 0;i<number_img_receive;i++){
        let check_data = shapes_all[`${i}`]?.shapes || [];
        // console.log("check_data.shapes.length",check_data.length);
        if (check_data.length  == 0){
          log.innerText +=`❌Chưa vẽ master thứ ${i}\n`;
          // console.log(`❌Chưa vẽ master thứ ${i}\n`);
          status_oke = false;
          is_oke = false;
        }
    }
    if (!status_oke) {
    log.innerText +=`✍️Tiến hành vẽ bổ sung các quy ước hình còn thiếu`;
    is_oke = false;
  }
  //  console.log("--------------------------------------");
  //  console.log("Kiểm tra tên quy ước hình nhập ");
  // phan nay se  huy comment sau khi chay ode kia oke
    for(let j = 0; j<number_img_receive;j++){
      let  dulieu = shapes_all?.[`${j}`]?.shapes;   // danh sach diem dau cua 1 hinh anh
      if (dulieu  == null){continue;}
      console.log("du lieu la",dulieu);
      for (let i of dulieu){
        console.log("doi tuong kla",i);
        let ten_max = i?.ten_khung_max||"";
        let ten_min = i?.ten_hinh_min ||"";
        if(ten_max === "" && ten_min === ""){
          // console.log(`Phát hiện master thứ ${j} không đặt tên`);
          log.innerText =`❌Phát hiện Master thứ ${j} không đặt tên`;
         is_oke = false;
        }
      }
    
    }
    for(let j = 0; j<number_img_receive;j++){
          let  arr_data = shapes_all?.[`${j}`]?.shapes||[]; 
          let  length_arr_data = arr_data.length;
          if (length_arr_data != 0){
          console.log (`-------------------------------Du lieu master ${j} ---------`);
          console.log("Danh sách các điểm dữ liệu của các hình",arr_data)
          for(let shape of arr_data ){
              if(shape.mode == "max"){
                if(length_arr_data - 1 < shape.so_diem_dau){
                    // console.log(`✖️Kiểm tra lại master ${j}\n✖️Số điểm dầu trong bảng nhiều hơn số điểm dầu vẽ`);
                    log.textContent = `✖️Kiểm tra lại master ${j}\n✖️Số điểm dầu trong bảng nhiều hơn số điểm dầu vẽ`;
                  
                }
                else if(length_arr_data - 1 > shape.so_diem_dau){
                  // console.log(`✖️Kiểm tra lại master ${j}\n ✖️Số điểm dầu trong bảng ít hơn số điểm dầu vẽ`);
                   log.textContent = `✖️Kiểm tra lại master ${j}\n✖️Số điểm dầu trong bảng ít hơn số điểm dầu vẽ`;
                } 
              }
          }
        }
    }
    if(is_oke ===false){
      return;
    }
    else{
        //  console.log("Dữ liệu Shape là :",shapes_all);
          log.textContent = `☑️Dữ liệu quy định master hợp lệ`;
          let normalizeShape  = normalizeShapes(shapes_all,1328, 830) 
         postData("/api_take_master/config_master",normalizeShape);
    }
});
function Event_press_left_right() {
    const scroll_width = scroll_content.scrollWidth;
    const scroll_client = scroll_container.clientWidth;
    const scroll_left = scroll_container.scrollLeft;
    if (scroll_width > scroll_client) {
      btn_left.style.display = scroll_left > 0 ? "block" : "none";
      btn_right.style.display = (scroll_left + scroll_client) < scroll_width ? "block" : "none";
    } else {
      btn_left.style.display = "none";
      btn_right.style.display = "none";
    }
}

function handleSquareBtnClick() {
  if (is_square_active) {
    deactivateAllButtons();
    check_select = null;
    return;
  }
  if (is_circle_active || is_pentagon_active) {
    log.innerText = "Lỗi: Chỉ được chọn một hình để vẽ tại một thời điểm";
    return;
  }
  deactivateAllButtons();
  is_square_active = true;
  check_no_Select_shape_1 = 1;
  btn_square.style.backgroundColor = "#43d9f3";
  btn_square.style.scale = "1.3";
  check_select = 1;
  check_Select_shape = 1;
}

function handleCircleBtnClick() {
  if (is_circle_active) {
    deactivateAllButtons();
    check_select = null;
    return;
  }
  if (is_square_active || is_pentagon_active) {
    log.innerText = "Lỗi: Chỉ được chọn một hình để vẽ tại một thời điểm";
    return;
  }
  deactivateAllButtons();
  is_circle_active = true;
  check_no_Select_shape_2 = 1;
  btn_circle.style.backgroundColor = "#43d9f3";
  btn_circle.style.scale = "1.3";
  check_select = 1;
  check_Select_shape = 1;
}

function handleSelectMinClick() {
  mode = "min";
  if (check_select == 0) {
    log.innerText = "Hãy chọn biên dạng phù hợp";
    return;
  }
  log.innerText = "Tiến hành vẽ đường bao điểm dầu \n";
  select_min.classList.add("active");
}



function handleCanvasDoubleClick(event) {
  log.innerHTML = "✍️ Nhập thông tin\n❌Tên quy ước không được trùng với tên đã có trong hình";
  console.log(shapes);
  const { x, y } = getMousePositionInCanvas(event, canvas_img_show);
  table_write_data.style.display = "block";
  table_write_data.innerHTML = ""; 
  // Xóa nút cũ nếu có
  const oldBtnContainer = part_table_log.querySelector(".btn-container");
  if (oldBtnContainer) {
    part_table_log.removeChild(oldBtnContainer);
  }
  let foundShape = null;
  for (let i = 0; i < shapes.length; i++) {
    const shape = shapes[i];
    if (shape.type === "rect" && isMouseNearRectBorder(x, y, shape)) {
      foundShape = shape;
      console.log(`Double click vào hình chữ nhật: index ${i}`, shape);

      let labels = [];

      if (shape.mode === "max") {
        labels = ["Tên khung max", "Số điểm dầu quy định"];
      } else if (shape.mode === "min") {
        labels = ["Tên hình", "Số điểm dầu quy định","Kích thước điểm dầu nhỏ nhất","Kích thước điểm dầu lớn nhất"];
      }

      // Tạo bảng
      labels.forEach((label,index)=> {
        const add_tr = document.createElement("tr");
        const add_th = document.createElement("th");
        const add_td = document.createElement("td");
        const add_input = document.createElement("input");

        add_th.innerText = label;
        
        if (index == 0) {
            add_input.type = "text";
        }
        else {
           add_input.type = "number";
        }
        add_input.placeholder = "Nhập ... ";
        add_input.className = "input-field"; 

        // 🔥 load value nếu shape đã có data
        const labelToKey = {
          "Tên khung max": "ten_khung_max",
          "Số điểm dầu quy định": "so_diem_dau",
          "Tên hình": "ten_hinh_min",
          "Kích thước điểm dầu nhỏ nhất": "kich_thuoc_min",
          "Kích thước điểm dầu lớn nhất": "kich_thuoc_max"
        };
        const key = labelToKey[label];
        if (key && shape[key] !== undefined) {
          add_input.value = shape[key]; // <-- load sẵn data
        }

        add_td.appendChild(add_input);
        add_tr.appendChild(add_th);
        add_tr.appendChild(add_td);
        table_write_data.appendChild(add_tr);
      });
    }

    if (shape.type === "circle" && isMouseNearCircleBorder(x, y, shape)) {
      let labels = [];
      foundShape = shape;
      if (shape.mode === "max") {
        labels = ["Tên khung max", "Số điểm dầu quy định"];
      } else if (shape.mode === "min") {
        labels = ["Tên hình", "Số điểm dầu quy định","Kích thước điểm dầu nhỏ nhất","Kích thước điểm dầu lớn nhất"];
      }

      // Tạo bảng
      labels.forEach((label,index) => {
        const add_tr = document.createElement("tr");
        const add_th = document.createElement("th");
        const add_td = document.createElement("td");
        const add_input = document.createElement("input");

        add_th.innerText = label;
        add_input.type = "text";
        if (index == 0) {
            add_input.type = "text";
        }
        else {
           add_input.type = "number";
        }
        add_input.placeholder = "Nhập ... ";
        add_input.className = "input-field"; 

        // 🔥 load value nếu shape đã có data
        const labelToKey = {
          "Tên khung max": "ten_khung_max",
          "Số điểm dầu quy định": "so_diem_dau",
          "Tên hình": "ten_hinh_min",
          "Kích thước điểm dầu nhỏ nhất": "kich_thuoc_min",
          "Kích thước điểm dầu lớn nhất": "kich_thuoc_max"
        };
        const key = labelToKey[label];
        if (key && shape[key] !== undefined) {
          add_input.value = shape[key]; // <-- load sẵn data
        }

        add_td.appendChild(add_input);
        add_tr.appendChild(add_th);
        add_tr.appendChild(add_td);
        table_write_data.appendChild(add_tr);
      });

      console.log(`Double click vào hình tròn: index ${i}`, shape);
    }
  }

  // Tạo nút ngoài vòng for, chỉ 1 lần
  const btn_accept = document.createElement("button");
  const btn_erase_string = document.createElement("button");
  btn_erase_string.innerText = "Xóa hết";
  btn_accept.innerText = "Chấp nhận";
  btn_accept.className = "btn";
  btn_erase_string.className = "btn";
  btn_erase_string.addEventListener("click", () => {
    const inputs = table_write_data.querySelectorAll("input");
    inputs.forEach(input => input.value = "");
  });

  btn_accept.addEventListener("click", () => {
    const labelToKey = {
      "Tên khung max": "ten_khung_max",
      "Số điểm dầu quy định": "so_diem_dau",
      "Tên hình": "ten_hinh_min",
      "Kích thước điểm dầu nhỏ nhất": "kich_thuoc_min",
      "Kích thước điểm dầu lớn nhất": "kich_thuoc_max"
    };

    // Chỉ các key này mới phải là số nguyên
    const integerKeys = [
      "so_diem_dau",
      "kich_thuoc_min",
      "kich_thuoc_max"
    ];

    const rows = table_write_data.querySelectorAll("tr");
    const data = {};
    let valid = true;
    let valid_repeat = true;
    rows.forEach(row => {
      const label = row.querySelector("th").innerText;
      const input = row.querySelector("input");
      const value = input.value.trim();
      const key = labelToKey[label] || label;

      // Check trùng tên hình min
      if (key == "ten_hinh_min") {
        const existing = shapes.find(shape =>
          ((shape?.ten_hinh_min) ?? '').trim() === (value ?? '').trim()
        );
        if (existing && existing !== foundShape) {
          valid_repeat = false;
        }
      }

      // Check trùng tên khung max
      if (key == "ten_khung_max") {
        const existing = shapes.find(shape =>
          ((shape?.ten_khung_max) ?? '').trim() === (value ?? '').trim()
        );
        if (existing && existing !== foundShape) {
          valid_repeat = false;
        }
      }

      // Các trường số nguyên
      if (integerKeys.includes(key)) {
        if (!/^-?\d+$/.test(value)) {
          // Không phải số nguyên
          input.style.border = "1px solid red";
          valid = false;
          return;
        } else {
          const numberValue = parseInt(value, 10);
          if (numberValue < 0) {
            // Số nguyên nhưng không hợp lệ (<= 0)
            input.style.border = "1px solid red";
            input.value = 0;
            valid = false;
            return;
          }
          // Hợp lệ
          input.style.border = "";
          data[key] = numberValue;
          return;
        }
      }

      // Các trường khác (string)
      input.style.border = "";
      data[key] = value;
    });

    // Sau khi duyệt xong tất cả row
    if (!valid) {
      alert("Bạn cần nhập số nguyên dương (> 0) ở các ô bị đánh dấu đỏ!");
      return;
    }
    if (!valid_repeat) {
      undo_shapes();
      hidden_table_and_button(table_write_data, part_table_log);
      alert("Tên hình/khung đã tồn tại! Hãy vẽ lại hình và đặt tên khác");
      return;
    }
    const text = data.ten_khung_max || data.ten_hinh_min || "Không có nội dung";
    writeLabelWitdthGet(foundShape, text, foundShape.x1, foundShape.y1);

    for(let j of shapes){
      if(foundShape == j){
        if (text == data.ten_khung_max){
          j["ten_khung_max"] = text;
          j["so_diem_dau"] = data.so_diem_dau; 
        }
        if(text == data.ten_hinh_min){
          j["ten_hinh_min"] = data.ten_hinh_min;
          j["so_diem_dau"] = data.so_diem_dau;
          j["kich_thuoc_min"] = data.kich_thuoc_min;
          j["kich_thuoc_max"] = data.kich_thuoc_max;
        }
      }
    }

    log.innerHTML = `✔️ Tạo quy ước thành điểm thành công \n👆Nhấn giữ chuột trái để xoay hình\n👆Nhấn giữ chuột phải để di chuyển hình\n--👉Chọn vẽ đường bao điểm`;
    redrawAll();
    hidden_table_and_button(table_write_data,part_table_log);
  });

  const div = document.createElement("div");
  div.className = "btn-container";
  div.style.display = "flex";
  div.style.justifyContent = "center";
  div.style.gap = "10px";

  div.appendChild(btn_erase_string);
  div.appendChild(btn_accept);
  part_table_log.appendChild(div);
}

function hidden_table_and_button(table_write_data,part_table_log){
    table_write_data.innerHTML = "";
    table_write_data.style.display = "none";
    const btnContainer = part_table_log.querySelector(".btn-container");
    if (btnContainer) {
      part_table_log.removeChild(btnContainer);
  }
}
function writeLabelWitdthGet(shape, string, coordinate_x, coordinate_y) {
  ctx.font = "18px Arial";

  ctx.fillStyle = shape.mode === "min" ? "blue" : "red";

  if (shape.type === "rect") {
    if (shape.corners && typeof shape.rotation === "number") {
    

      const angle = shape.rotation; 
      const pivot = shape.corners[0]; 
      
      ctx.save(); 
      ctx.translate(pivot.x, pivot.y);
      ctx.rotate(angle);
      ctx.fillText(string, 0, -10); 
      ctx.restore(); 
    } else {
      ctx.fillText(string, coordinate_x, coordinate_y - 10);
      // shapes.push({"text":`${string}`,"color":ctx.fillStyle,"x":shape.x1,"y":shape.x2)
    }
  }   else if (shape.type === "circle") {
    const x = shape.cx || coordinate_x;
    const y = shape.cy || coordinate_y;
    ctx.fillText(string, x, y - (shape.r || 10) - 10); // đặt text phía trên hình tròn
  }
}

// ==========================
// 5. Event Listeners
// ==========================
btn_close.addEventListener("click",function(){
   postData("api_take_master/master_close", { "status": "on" }).then(data => {
    console.log("Master close :" + data);
    window.location.href = "/";
  });
});
chooseProductBtn.addEventListener("click", () => {
  window.location.href = "/api_choose_master/chose_product";
  history.replaceState(null, "", "/api_choose_master/chose_product");
});


function split_data_shapes(data){
   console.log("master_shapes_data----------------------------",data)
   shapes_all = {};
   shapes_all = data;
   shapes_all = denormalizeShapes(shapes_all,1328,830)
   is_screen_frame_load_data = true;
   console.log("Shape khi nhan vao nut take master",shapes_all);
}
function denormalizeShapes(data, width, height) {
  // clone để không thay đổi data gốc
  const result = JSON.parse(JSON.stringify(data));

  for (const key in result) {
    const item = result[key];
    if (!item.shapes) continue;

    item.shapes.forEach(shape => {
      if (shape.type === "rect") {
        shape.x1 = shape.x1 * width;
        shape.x2 = shape.x2 * width;
        shape.y1 = shape.y1 * height;
        shape.y2 = shape.y2 * height;

        if (shape.corners) {
          shape.corners = shape.corners.map(c => ({
            x: c.x * width,
            y: c.y * height
          }));
        }
      } else if (shape.type === "circle") {
        shape.cx = shape.cx * width;
        shape.cy = shape.cy * height;
        // bán kính nhân lại với width (hoặc (width+height)/2 nếu normalize kiểu khác)
        shape.r = shape.r * width;
      }
    });
  }

  return result;
}

headerMasterTake.addEventListener("click", () => {
    shapes_all = {};
    set_Z_index_canvas_show(-1);
    const take_master = document.getElementById("paner-take-master");
    if (current_panner === take_master) return;
    current_panner.classList.remove("active");
    current_panner.style.zIndex = 1;
    take_master.classList.add("active");
    take_master.style.zIndex = 2;
    setCurrentPanner(take_master);
    console.log("current_panner",current_panner);
    postData("api_take_master/master_take", { "status": "on" }).then(data => {
            console.log("Master Take :" + data);
            let master_shapes_data = {};
            master_shapes_data = data?.Shapes;  
            split_data_shapes(master_shapes_data)
            number_img_receive = 0;
            const imgList = data.path_arr_img; 
            scroll_content.innerHTML = ""; // Xóa hết ảnh cũ trước khi thêm mới
            console.log("Danh sách ảnh:", imgList);
            imgList.forEach((imgPath, index) => {
                index_point_current =  index; 
                number_img_receive++; 

                const div_create = document.createElement("div");
                div_create.className = "div-index-img-mater";
                const h_create = document.createElement("p");
                h_create.innerText = `Ảnh master ${index}`;
                h_create.className = "p-index-img-master";

                const img = document.createElement("img");
                img.src = imgPath;
                img.alt = "Ảnh sản phẩm";
                img.style.width = "200px";
                img.style.margin = "10px";

                div_create.appendChild(img);
                div_create.appendChild(h_create);
                scroll_content.appendChild(div_create);
                div_create.addEventListener("click", () => {
                    set_index_img_current(index);
                    log.textContent = "";
                    hidden_table_and_button(table_write_data,part_table_log);
                    console.log("number_img_receive",number_img_receive);
                    document.querySelectorAll(".div-index-img-mater").forEach(d => {
                      d.style.border = "none";
                    });
                    div_create.style.border ="5px solid green";
                    if(flag_index_choose_last==1){
                      index_choose_last = index;  //cai dat index lan dau
                      flag_index_choose_last = 0;
                    }
                    console.log("btn_accept_and_send" + index_point_current);   // index dem tu so 0
                    console.log("Bạn đã nhấn vào index thứ " + index);   // index dem tu so 0
                    console.log("index dang nhan la",index,"index truoc khi nhan la",index_choose_last)
                    next_page_img(index,index_choose_last);
                    index_choose_last = index;
                    canvas_img_show.width = 1328;
                    canvas_img_show.height = 830;
                    canvas_img_show_oke.width = 1328;
                    canvas_img_show_oke.height = 830;
                    const show_img = new Image();
                    show_img.src = imgPath;
                    show_img.onload = () => {
                      ctx_oke.drawImage(show_img, 0, 0, 1328, 830);
                    };
                    redrawAll();
                });
          });
      });
});

btn_left.addEventListener("click", () => {
  scroll_content.scrollBy({ left: -SCROLL_STEP, behavior: "smooth" });
});
btn_right.addEventListener("click", () => {
  scroll_content.scrollBy({ left: SCROLL_STEP, behavior: "smooth" });
});
scroll_container.addEventListener("scroll", Event_press_left_right);

btn_square.addEventListener("click", handleSquareBtnClick);
btn_circle.addEventListener("click", handleCircleBtnClick);
select_min.addEventListener("click", handleSelectMinClick);
canvas_img_show.addEventListener("dblclick", handleCanvasDoubleClick);

// ==========================
// 6. Init (DOMContentLoaded)
// ==========================

// document.addEventListener("DOMContentLoaded", () => {
//   const dataImg = scroll_content.dataset.img;
//   const imgList = JSON.parse(dataImg);
//   console.log("Danh sách ảnh:", imgList);

//   imgList.forEach((imgPath, index) => {
//     index_point_current =  index; 
//     number_img_receive = number_img_receive + 1;
//     const div_create = document.createElement("div");
//     div_create.className = "div-index-img-mater";

//     const h_create = document.createElement("p");
//     h_create.innerText = `Ảnh master ${index}`;
//     h_create.className = "p-index-img-master";

//     const img = document.createElement("img");
//     img.src = imgPath;
//     img.alt = "Ảnh sản phẩm";
//     img.style.width = "200px";
//     img.style.margin = "10px";

//     div_create.appendChild(img);
//     div_create.appendChild(h_create);
//     scroll_content.appendChild(div_create);
//     div_create.addEventListener("click", () => {
//       set_index_img_current(index);
//       log.textContent = "";
//       hidden_table_and_button(table_write_data,part_table_log);
//       console.log("number_img_receive",number_img_receive);
//       document.querySelectorAll(".div-index-img-mater").forEach(d => {
//         d.style.border = "none";
//       });
//       div_create.style.border ="5px solid green";
//       if(flag_index_choose_last==1){
//         index_choose_last = index;  //cai dat index lan dau
//         flag_index_choose_last = 0;
//       }
//        console.log("btn_accept_and_send" + index_point_current);   // index dem tu so 0
//       console.log("Bạn đã nhấn vào index thứ " + index);   // index dem tu so 0
//       next_page_img(index,index_choose_last);
//       index_choose_last = index;
//       canvas_img_show.width = 1328;
//       canvas_img_show.height = 830;
//       canvas_img_show_oke.width = 1328;
//       canvas_img_show_oke.height = 830;
//       const show_img = new Image();
//       show_img.src = imgPath;
//       show_img.onload = () => {
//         ctx_oke.drawImage(show_img, 0, 0, 1328, 830);
//       };
//       redrawAll();
//     });
//   });
// });
function delete_page_img(index) {
    if (shapes_all.hasOwnProperty(`${index}`)) {
        delete shapes_all[`${index}`]; // Xóa key trong dict
        console.log(`Đã xóa trang ${index}`, shapes_all);
    } else {
        console.log(`Trang ${index} không tồn tại`);
    }
}
function delete_shape_on_page(index, shape_idx) {
    if (shapes_all.hasOwnProperty(`${index}`)) {
        let shapes_page = shapes_all[`${index}`].shapes;
        if (shape_idx >= 0 && shape_idx < shapes_page.length) {
            shapes_page.splice(shape_idx, 1);  // Xóa shape tại vị trí
            console.log(`Đã xóa shape ${shape_idx} tại trang ${index}`);
        } else {
            console.log("Chỉ số shape không hợp lệ");
        }
    } else {
        console.log(`Trang ${index} không tồn tại`);
    }
}

function next_page_img(index,index_choose_last){
    
    let dict_data = {}
    dict_data.shapes = shapes;
    console.log("dict_data....",dict_data);
    if (!shapes_all) {
    shapes_all = {};   // khởi tạo object rỗng
}
if (!is_screen_frame_load_data){
shapes_all[`${index_choose_last}`] = dict_data;}
else{
  is_screen_frame_load_data =  false;
}
    console.log("Shape khi nhan vao nut chuyen hinh anh div:",shapes_all);
    if(Object.keys(shapes_all).length > 0)
    {    
        
         shapes = shapes_all[`${index}`]?.shapes || [];
          console.log("dataa cho nay nhu nay neee ::::: shapes_all",shapes_all)
         console.log("dataa cho nay nhu nay neee ::::: shapes",shapes)
         redrawAll();
    }
}



// =========================
// 2. HÀM TIỆN ÍCH (UTILITIES)
// =========================


function getRotatedRectCorners(rect) {
  const x = Math.min(rect.x1, rect.x2);
  const y = Math.min(rect.y1, rect.y2);
  const w = Math.abs(rect.x2 - rect.x1);
  const h = Math.abs(rect.y2 - rect.y1);

  const cx = x + w / 2;
  const cy = y + h / 2;
  const angle = rect.rotation || 0;

  const corners = [
    { x: -w / 2, y: -h / 2 }, // top-left
    { x: w / 2,  y: -h / 2 }, // top-right
    { x: w / 2,  y: h / 2 },  // bottom-right
    { x: -w / 2, y: h / 2 }   // bottom-left
  ];

  return corners.map(p => ({
    x: p.x * Math.cos(angle) - p.y * Math.sin(angle) + cx,
    y: p.x * Math.sin(angle) + p.y * Math.cos(angle) + cy
  }));
}

function isMouseNearCircleBorder(mouseX, mouseY, circle, threshold = 10) {
  const dx = mouseX - circle.cx;
  const dy = mouseY - circle.cy;
  const distance = Math.sqrt(dx * dx + dy * dy);
  return Math.abs(distance - circle.r) <= threshold;
}

function isMouseNearRectBorder(mouseX, mouseY, rect, threshold = 10) {
  const x = Math.min(rect.x1, rect.x2);
  const y = Math.min(rect.y1, rect.y2);
  const width = Math.abs(rect.x2 - rect.x1);
  const height = Math.abs(rect.y2 - rect.y1);

  const left = x, right = x + width;
  const top = y, bottom = y + height;

  const nearLeft   = Math.abs(mouseX - left)   <= threshold && mouseY >= top && mouseY <= bottom;
  const nearRight  = Math.abs(mouseX - right)  <= threshold && mouseY >= top && mouseY <= bottom;
  const nearTop    = Math.abs(mouseY - top)    <= threshold && mouseX >= left && mouseX <= right;
  const nearBottom = Math.abs(mouseY - bottom) <= threshold && mouseX >= left && mouseX <= right;

  return nearLeft || nearRight || nearTop || nearBottom;
}
function undo_shapes() {
  if (shapes.length > 0) {
    shapes.pop();
    redrawAll();
    log.innerText += "Quay lại thành công\n";
  } else {
    log.innerText = "Chưa có hình nào đã vẽ";
  }
  redrawAll();
}
// =========================
// 3. HÀM VẼ
// =========================
function redrawAll() {
  ctx.clearRect(0, 0, canvas_img_show.width, canvas_img_show.height);
  for (let shape of shapes) {
    ctx.lineWidth = shape.lineWidth || 3;
    ctx.strokeStyle = shape.color;

    if (shape.type === "rect") {
      const x = Math.min(shape.x1, shape.x2);
      const y = Math.min(shape.y1, shape.y2);
      const w = Math.abs(shape.x2 - shape.x1);
      const h = Math.abs(shape.y2 - shape.y1);
      const cx = x + w / 2;
      const cy = y + h / 2;
      const rotation = shape.rotation || 0;

      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(rotation);
      ctx.strokeRect(-w / 2, -h / 2, w, h);
      ctx.restore();
    }
    else if (shape.type === "circle") {
      ctx.beginPath();
      ctx.arc(shape.cx, shape.cy, shape.r, 0, 2 * Math.PI);
      ctx.stroke();
    }
    if(shape.ten_hinh_min && shape.type == "rect"){
       writeLabelWitdthGet(shape,shape.ten_hinh_min,shape.x1,shape.y1);
    }
    if(shape.ten_khung_max && shape.type == "rect"){
      writeLabelWitdthGet(shape,shape.ten_khung_max,shape.x1,shape.y1);
    }
    if(shape.ten_khung_max && shape.type == "circle"){
      writeLabelWitdthGet(shape,shape.ten_khung_max,shape.cx,shape.cy);
    }
    if(shape.ten_hinh_min && shape.type == "circle"){
      writeLabelWitdthGet(shape,shape.ten_hinh_min,shape.cx,shape.cy);
    }
  }
}
function reredrawAll(shapes) {
  ctx.clearRect(0, 0, canvas_img_show.width, canvas_img_show.height);
  for (let shape of shapes) {
    ctx.lineWidth = shape.lineWidth || 3;
    ctx.strokeStyle = shape.color;

    if (shape.type === "rect") {
      const x = Math.min(shape.x1, shape.x2);
      const y = Math.min(shape.y1, shape.y2);
      const w = Math.abs(shape.x2 - shape.x1);
      const h = Math.abs(shape.y2 - shape.y1);
      const cx = x + w / 2;
      const cy = y + h / 2;
      const rotation = shape.rotation || 0;

      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(rotation);
      ctx.strokeRect(-w / 2, -h / 2, w, h);
      ctx.restore();
    }
    else if (shape.type === "circle") {
      ctx.beginPath();
      ctx.arc(shape.cx, shape.cy, shape.r, 0, 2 * Math.PI);
      ctx.stroke();
    }
    if(shape.ten_hinh_min && shape.type == "rect"){
       writeLabelWitdthGet(shape,shape.ten_hinh_min,shape.x1,shape.y1);
    }
    if(shape.ten_khung_max && shape.type == "rect"){
      writeLabelWitdthGet(shape,shape.ten_khung_max,shape.x1,shape.y1);
    }
    if(shape.ten_khung_max && shape.type == "circle"){
      writeLabelWitdthGet(shape,shape.ten_khung_max,shape.cx,shape.cy);
    }
    if(shape.ten_hinh_min && shape.type == "circle"){
      writeLabelWitdthGet(shape,shape.ten_hinh_min,shape.cx,shape.cy);
    }
  }
}

function drawPreview() {
  let previewColor = mode === "min" ? 'rgba(0,0,255,0.5)' : 'rgba(255,0,0,0.5)';
  ctx.strokeStyle = previewColor;

  if (is_square_active) {
    const x = Math.min(startX, endX);
    const y = Math.min(startY, endY);
    const w = Math.abs(endX - startX);
    const h = Math.abs(endY - startY);
    ctx.strokeRect(x, y, w, h);
  }
  else if (is_circle_active) {
    const radius = Math.sqrt((endX - startX) ** 2 + (endY - startY) ** 2);
    ctx.beginPath();
    ctx.arc(startX, startY, radius, 0, 2 * Math.PI);
    ctx.stroke();
  }
}

// =========================
// 4. XỬ LÝ SỰ KIỆN
// =========================


function handleMouseDown(event) {
  hidden_table_and_button(table_write_data,part_table_log);
  if (event.detail >= 2) return; // Double click

  // Chuột phải -> kéo rect
  if (event.button === 2) {
    const { x, y } = getMousePositionInCanvas(event, canvas_img_show);
    for (let i = 0; i < shapes.length; i++) {
      let shape = shapes[i];
      if (shape.type === "rect" && isMouseNearRectBorder(x, y, shape)) {
        draggingRectIndex = i;
        isDraggingRectWithRightClick = true;
        dragRectOffsetX = x - shape.x1;
        dragRectOffsetY = y - shape.y1;
        event.preventDefault();
        return;
      }
    }
  }

  // Xoay rect
  if (is_hover_square && hoveredRectIndex !== -1) {
    isRotating = true;
    const rect = shapes[hoveredRectIndex];
    const cx = (rect.x1 + rect.x2) / 2;
    const cy = (rect.y1 + rect.y2) / 2;
    const { x, y } = getMousePositionInCanvas(event, canvas_img_show);
    rotateStartMouseAngle = Math.atan2(y - cy, x - cx);
    currentRotation = rect.rotation || 0;
    event.preventDefault();
    return;
  }

  // Kéo circle
  if (is_hover_circle && hoveredCircleIndex !== -1) {
    isDraggingCircle = true;
    const circle = shapes[hoveredCircleIndex];
    const { x, y } = getMousePositionInCanvas(event, canvas_img_show);
    dragOffsetX = x - circle.cx;
    dragOffsetY = y - circle.cy;
    event.preventDefault();
    return;
  }

  // Kiểm tra trạng thái trước khi vẽ
  if (check_no_select_shape(check_no_Select_shape_1, check_no_Select_shape_2, check_no_Select_shape_3)) { 
    log.innerText = "☑️Chọn biên dạng phù hợp";
    log.innerText += "\n☑️Chọn vẽ đường bao khối để khoanh vùng cần xử lý";
    log.innerText += "\n☑️Chọn vẽ đường bao điểm để khoanh vùng điểm dầu cần xử lý";
    return;
  }
  if (check_select == 1 && !mode) {
    log.innerText = "☑️Chọn vẽ đường bao khối để khoanh vùng cần xử lý";
    log.innerText += "\n☑️Chọn vẽ đường bao điểm để khoanh vùng điểm dầu cần xử lý";
    return;
  }
  if (!check_Select_shape) { 
    log.innerText = "Chọn biên dạng phù hợp";
    log.innerText += "\n☑️Chọn vẽ đường bao khối để khoanh vùng cần xử lý";
    log.innerText += "\n☑️Chọn vẽ đường bao điểm để khoanh vùng điểm dầu cần xử lý";
    return; 
  }
  if (!mode) { 
    log.innerText = "Chọn vẽ đường bao khối hoặc vẽ đường bao điểm dầu";
    return;
  }

  // Bắt đầu vẽ
  let { x, y } = getMousePositionInCanvas(event, canvas_img_show);
  startX = x;
  startY = y;
  isDrawing = true;
  log.textContent = ".... đang vẽ ....";
}
function getMousePositionInCanvas(event, canvas) {
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / rect.width;
  const scaleY = canvas.height / rect.height;
  let mouseX = Math.floor((event.clientX - rect.left) * scaleX);
  let mouseY = Math.floor((event.clientY - rect.top) * scaleY);
  return { x: Math.max(0, mouseX), y: Math.max(0, mouseY) };
}

function handleMouseMove(event) {
  const { x, y } = getMousePositionInCanvas(event, canvas_img_show);
  // Xoay rect
  if (isRotating && hoveredRectIndex !== -1) {
    const rect = shapes[hoveredRectIndex];
    const cx = (rect.x1 + rect.x2) / 2;
    const cy = (rect.y1 + rect.y2) / 2;
    const currentMouseAngle = Math.atan2(y - cy, x - cx);
    const deltaAngle = currentMouseAngle - rotateStartMouseAngle;
    rect.rotation = currentRotation + deltaAngle;
    rect.corners = getRotatedRectCorners(rect);
    redrawAll();
    event.preventDefault();
    return;
  }

  // Kéo circle
  if (isDraggingCircle && hoveredCircleIndex !== -1) {
    const circle = shapes[hoveredCircleIndex];
    circle.cx = x - dragOffsetX;
    circle.cy = y - dragOffsetY;
    redrawAll();
    event.preventDefault();
    return;
  }

  // Kéo rect bằng chuột phải
  if (isDraggingRectWithRightClick && draggingRectIndex !== -1) {
    const rect = shapes[draggingRectIndex];
    const width = rect.x2 - rect.x1;
    const height = rect.y2 - rect.y1;
    rect.x1 = x - dragRectOffsetX;
    rect.y1 = y - dragRectOffsetY;
    rect.x2 = rect.x1 + width;
    rect.y2 = rect.y1 + height;
    if (rect.rotation) rect.corners = getRotatedRectCorners(rect);
    redrawAll();
    event.preventDefault();
    return;
  }

  // Kiểm tra hover
  let cursorStyle = "crosshair";
  is_hover_square = false;
  is_hover_circle = false;
  hoveredCircleIndex = -1;

  for (let i = 0; i < shapes.length; i++) {
    const shape = shapes[i];
    if (shape.type === "rect" && isMouseNearRectBorder(x, y, shape)) {
      is_hover_square = true;
      cursorStyle = "pointer";
      hoveredRectIndex = i;
      break;
    } else if (shape.type === "circle" && isMouseNearCircleBorder(x, y, shape)) {
      is_hover_circle = true;
      cursorStyle = "pointer";
      hoveredCircleIndex = i;
      break;
    }
  }
  canvas_img_show.style.cursor = cursorStyle;

  // Hiển thị tọa độ
  coordinate.textContent = `Pixel: (${x}, ${y})`;

  // Nếu đang vẽ thì update preview
  if (isDrawing) {
    endX = x;
    endY = y;
    redrawAll();
    drawPreview();
  }
}

function handleMouseUp(event) {
  if (event.button === 2 && isDraggingRectWithRightClick) {
    isDraggingRectWithRightClick = false;
    draggingRectIndex = -1;
    event.preventDefault();
    return;
  }
  if (isRotating) {
    isRotating = false;
    hoveredRectIndex = -1;
    event.preventDefault();
    return;
  }
  if (isDraggingCircle) {
    isDraggingCircle = false;
    hoveredCircleIndex = -1;
    event.preventDefault();
    return;
  }
  if (!isDrawing) return;

  isDrawing = false;
  const color = mode === 'min' ? 'blue' : 'red';

let newShape = null;
if (is_square_active) {
  newShape = { type: "rect", x1: startX, y1: startY, x2: endX, y2: endY, mode, color };
} else if (is_circle_active) {
  const radius = Math.sqrt((endX - startX) ** 2 + (endY - startY) ** 2);
  newShape = { type: "circle", cx: startX, cy: startY, r: radius, mode, color };
}
const added = addShape(newShape);
if (newShape) {
  
  if (added) {
    const lastShape = shapes[shapes.length - 1];
    const shapeType = lastShape.type === "rect" ? "hình chữ nhật" : "hình tròn";
    log.textContent = `🖍 Đã vẽ ${shapeType}.\n🖍 Nhấn đúp chuột trái vào viền ${shapeType} để thêm thông tin`;
    
  }
  
}
  redrawAll();
  const lastShape = shapes[shapes.length - 1];
  const shapeType = lastShape.type === "rect" ? "hình chữ nhật" : "hình tròn";
  log.textContent = `🖍 Đã vẽ ${shapeType}.\n🖍 Nhấn đúp chuột trái vào viền ${shapeType} để thêm thông tin`;
  if(added === false){
    log.innerText = `❌Trong 1 hình chỉ cho phép 1 khung MAX`;
  }
}

// =========================
// 5. NÚT CHỨC NĂNG
// =========================
btn_undo.addEventListener("click", () => {
  if (shapes.length > 0) {
    let lastIndex = shapes.length - 1;
    delete_shape_on_page(lastIndex,index_img_current);
    shapes.pop();
    redrawAll();
    log.innerText = "👈Quay lại thành công\n";
  } else {
    log.innerText = "❌Chưa có hình nào đã vẽ";
  }
});

btn_erase.addEventListener("click", () => {
  delete_page_img(index_img_current);
  shapes = [];
  redrawAll();
  log.textContent = "🗑 Đã xóa tất cả hình.\n";
});

//Kiem tra so luong max co giong voi so luong min khong
//---------------------------------------------------------------
btn_check.addEventListener("click", () => {
    let  length_arr_data = shapes.length;
    console.log("Do dai shape ban sao",shapes);
    for(let j = 0; j<number_img_receive;j++){
          if (length_arr_data != 0){
          console.log (`-------------------------------Du lieu master ${j} ---------`);
          console.log("Danh sách các điểm dữ liệu của các hình",shapes)
          for(let shape of shapes ){
              if(shape.mode == "max"){
                if(length_arr_data - 1 < shape.so_diem_dau){
                    console.log(`\n✖️Số điểm dầu trong bảng nhiều hơn số điểm dầu vẽ`);
                    log.textContent = `✖️Số điểm dầu trong bảng nhiều hơn số điểm dầu vẽ\n❌Thêm hình hoặc xóa bớt số hình trong khung`;
                    return;
        
                }
                else if(length_arr_data - 1 > shape.so_diem_dau){
                  console.log(`✖️Số điểm dầu trong bảng ít hơn số điểm dầu vẽ`);
                   log.textContent = `✖️Số điểm dầu trong bảng ít hơn số điểm dầu vẽ\n❌Xóa bớt hình hoặc vẽ thêm hình trong khung`;
                    return;
                }
                
              }

          }
          }

        }
//Kiem tra dien ten hay chua 
  
     // danh sach diem dau cua 1 hinh anh
      console.log("du lieu la",shapes);
      for (let i of shapes){
        console.log("doi tuong kla",i);
        let ten_max = i?.ten_khung_max||"";
        let ten_min = i?.ten_hinh_min ||"";
        if(ten_max === "" && ten_min === ""){
          console.log(`❌Chưa đặt đầy đủ thông tin. Hãy ghi tên đầy đủ`);
          log.innerText  = "❌Chưa đặt đầy đủ tên hình,khung.\n🖍Hãy ghi tên đầy đủ"
          return;
        }
      }
    
    








  console.log(`Nhấn vào nút nhấn check hình`);
  console.log(`Số lượng hình: ${shapes.length}`);
  if (shapes.length === 0) {
    console.log("❌Chưa vẽ hình nào!\n✏ Hãy vẽ thêm!");
    log.innerText = "❌Chưa vẽ hình nào!\n✏ Hãy vẽ thêm!";
    return;
  }

  const list_min = shapes.filter(s => s.mode == "min");
  const list_max = shapes.filter(s => s.mode == "max");

  console.log("----------------------------------------------------------------");
  console.log("Danh sách MIN:", list_min);
  console.log("----------------------------------------------------------------");
  console.log("Danh sách MAX:", list_max);
  console.log("----------------------------------------------------------------");

  let all_ok = true;

  for (let i = 0; i < list_min.length; i++) {
    const min = list_min[i];
    let inside_some_max = false;
    for (let j = 0; j < list_max.length; j++) {
      const max = list_max[j];
      let contained = false;
      if (min.type === "rect" && max.type === "rect") {
        contained = isRectInRect(min, max);
      } 
      else if (min.type === "circle" && max.type === "circle") {
        contained = isCircleInCircle(min, max);
      } 
      else if (min.type === "rect" && max.type === "circle") {
        contained = isRectInCircle(min, max);
      } 
      else if (min.type === "circle" && max.type === "rect") {
        contained = isCircleInRect(min, max);
      }

      if (contained) {
        inside_some_max = true;
        console.log(`✅ Min ${min.type} #${i + 1} nằm trọn trong Max ${max.type} #${j + 1}`);
        break;
      }
    }

    if (!inside_some_max) {
      console.log(`❌ Min ${min.type} #${i + 1} KHÔNG nằm trọn trong bất kỳ Max nào!`);
      all_ok = false;
    }
  }
  if(list_max.length === 0){
    log.innerText = "✅ OK không tìm thấy lỗi";
    return;
  }
  log.innerText = all_ok
    ? "✅ OK không tìm thấy lỗi"
    : "❌Điểm dầu không được nằm ngoài phạm vi hình khối";
});


// ================== Các hàm check ==================

// ================== Các hàm check ==================

// Check điểm nằm trong polygon (corners có xoay)
function pointInPolygon(point, polygon) {
  let inside = false;
  for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
    const xi = polygon[i].x, yi = polygon[i].y;
    const xj = polygon[j].x, yj = polygon[j].y;

    const intersect = ((yi > point.y) !== (yj > point.y)) &&
      (point.x < (xj - xi) * (point.y - yi) / ((yj - yi) || 1e-6) + xi);
    if (intersect) inside = !inside;
  }
  return inside;
}

// Rect trong Rect (tự động chọn corners hoặc bounding box)
function isRectInRect(inner, outer) {
  // --- Nếu outer có xoay (corners tồn tại) ---
  if (outer.corners) {
    const innerCorners = inner.corners || [
      { x: Math.min(inner.x1, inner.x2), y: Math.min(inner.y1, inner.y2) },
      { x: Math.min(inner.x1, inner.x2), y: Math.max(inner.y1, inner.y2) },
      { x: Math.max(inner.x1, inner.x2), y: Math.min(inner.y1, inner.y2) },
      { x: Math.max(inner.x1, inner.x2), y: Math.max(inner.y1, inner.y2) }
    ];
    return innerCorners.every(corner => pointInPolygon(corner, outer.corners));
  }

  // --- Nếu outer không xoay (chỉ có x1,y1,x2,y2) ---
  const ox1 = Math.min(outer.x1, outer.x2), oy1 = Math.min(outer.y1, outer.y2);
  const ox2 = Math.max(outer.x1, outer.x2), oy2 = Math.max(outer.y1, outer.y2);

  const innerCorners = inner.corners || [
    { x: Math.min(inner.x1, inner.x2), y: Math.min(inner.y1, inner.y2) },
    { x: Math.min(inner.x1, inner.x2), y: Math.max(inner.y1, inner.y2) },
    { x: Math.max(inner.x1, inner.x2), y: Math.min(inner.y1, inner.y2) },
    { x: Math.max(inner.x1, inner.x2), y: Math.max(inner.y1, inner.y2) }
  ];

  return innerCorners.every(p => p.x >= ox1 && p.x <= ox2 && p.y >= oy1 && p.y <= oy2);
}

// Circle trong Circle
function isCircleInCircle(inner, outer) {
  const dx = inner.cx - outer.cx;
  const dy = inner.cy - outer.cy;
  const distance = Math.sqrt(dx * dx + dy * dy);
  return distance + inner.r <= outer.r;
}

// Rect trong Circle
function isRectInCircle(rect, circle) {
  const corners = rect.corners || [
    { x: Math.min(rect.x1, rect.x2), y: Math.min(rect.y1, rect.y2) },
    { x: Math.min(rect.x1, rect.x2), y: Math.max(rect.y1, rect.y2) },
    { x: Math.max(rect.x1, rect.x2), y: Math.min(rect.y1, rect.y2) },
    { x: Math.max(rect.x1, rect.x2), y: Math.max(rect.y1, rect.y2) }
  ];

  return corners.every(p => {
    const dx = p.x - circle.cx;
    const dy = p.y - circle.cy;
    return Math.sqrt(dx * dx + dy * dy) <= circle.r;
  });
}

// Circle trong Rect (cũng phân biệt xoay / không xoay)
function isCircleInRect(circle, rect) {
  if (rect.corners) {
    // Nếu rect có xoay → check 4 điểm rìa của circle trong polygon
    const testPoints = [
      { x: circle.cx - circle.r, y: circle.cy },
      { x: circle.cx + circle.r, y: circle.cy },
      { x: circle.cx, y: circle.cy - circle.r },
      { x: circle.cx, y: circle.cy + circle.r }
    ];
    return testPoints.every(p => pointInPolygon(p, rect.corners));
  }

  // Nếu rect không xoay (axis aligned)
  const rx1 = Math.min(rect.x1, rect.x2), ry1 = Math.min(rect.y1, rect.y2);
  const rx2 = Math.max(rect.x1, rect.x2), ry2 = Math.max(rect.y1, rect.y2);

  return (
    circle.cx - circle.r >= rx1 &&
    circle.cx + circle.r <= rx2 &&
    circle.cy - circle.r >= ry1 &&
    circle.cy + circle.r <= ry2
  );
}
function addShape(shape) {
  // Nếu là MAX thì không cho vẽ thêm nếu đã tồn tại MAX trong shapes
  if (shape.mode === "max") {
    const hasMax = shapes.some(s => s.mode === "max");
    if (hasMax) {
      log.innerText = `❌ Trong khung chỉ được phép có 1 hình MAX!`;
      return false;
    }
  }

  // Nếu là MIN → thêm luôn
  shapes.push(shape);
  return true;
}


out_app.addEventListener('click',()=>{
  window.close();

});
add_product.addEventListener("click",function(){
    window.location.href = "/api_new_product/add";
    history.replaceState(null, "", "/api_new_product/add");
})

