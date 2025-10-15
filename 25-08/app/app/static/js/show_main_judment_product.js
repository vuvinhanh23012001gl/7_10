
import {logSocket,canvas_img_show_oke,ctx_oke,scroll_content} from "./show_main_status.js";
console.log("đã vào Hàm phán định")

const progressRow = document.getElementById('progress-row');
const productCount = document.getElementById('product-count');

const label_status_connect_com = document.getElementById("header-show-status");
const circle_status_connect_com =  document.getElementById("element-circle-status-com");
const circle_status_connect_camera =  document.getElementById("element-circle-status-camera");
const label_status_connect_camera = document.getElementById("status-connect-cam");



const time_total = document.getElementById("time-display");
const io_img_and_data = io("/img_and_data");
const table_show_point_detect = document.getElementById("table-show-point-detect");
const toggleBtn = document.getElementById("toggleBtn");
const status_judment = document.querySelector(".paner-main-status-product");
const log_judment   = document.getElementById("log_judment");
 const run_btn = document.getElementById("api-run");

let index_current_click =  0;  //Nơi lưu nhấn vào div
let imgPath_current = null;   // nơi lưu link ảnh show hiện tại

let status_view_master = true   //để xác định trạng thái nút nhấn đang ở chế độ xem master hay chế độ xem ảnh
let reset_data_table = 0;       // biến reset bắt đầu chạy quá trình mới
let data_table_browse = [];
let capturedImages = [];  // Mảng chứa nhiều ảnh
let divCreateList = []; // biến toàn cục luu mang div

logSocket.on("log_message_judment",(data)=>{
    let data_log  = data?.log_data;
    if (data_log){
        log_judment.innerHTML += `${data_log}<br>`;
    }
});
logSocket.on("status_connect_com_arm",(data)=>{
    let status_connect  = data?.status;
    isConect(status_connect,circle_status_connect_com,label_status_connect_com,"COM");
});
logSocket.on("status_connect_camera",(data)=>{
    let status_connect  = data?.status;
    isConect(status_connect,circle_status_connect_camera,label_status_connect_camera,"Camera");
});

function isConect(isconect,element_circle,element_lable,str_lable){
    if (isconect) {
        element_circle.classList.remove("off");
        element_circle.classList.add("on");
        element_lable.innerText = `${str_lable} đã kết nối`;
        } else {
        element_circle.classList.add("off");
        element_circle.classList.remove("on");
        element_lable.innerText = `${str_lable} mất kết nối`;
    }
}

run_btn.addEventListener('click',()=>{
      status_judment.innerHTML = "--"
      status_judment.classList.remove("OK");
      status_judment.classList.remove("NG");
      clearn_div(divCreateList);
       status_judment.innerHTML = "--";
      fetch('/api_run_application/run_application')
      .then(response => response.json())
      .then(data => {
        console.log("Dữ liệu nhận sau click Run"+ data);
        if(data.status  == "OK"){
          console.log("Gửi dữ liệu Run Thành công đến Server"+ data);
        }
      })
      .catch(err => {
        console.error('❌ Lỗi khi gửi Run GET:', err);
      });
});

toggleBtn.addEventListener("click",()=>{
      status_view_master = !status_view_master;
    if(status_view_master){
      toggleBtn.innerHTML = "Ảnh phán định";
      canvas_img_show_oke.width = 1328;
      canvas_img_show_oke.height = 830;
      const show_img = new Image();
      show_img.src = imgPath_current;
      show_img.onload = () => {
        ctx_oke.drawImage(show_img, 0, 0, 1328, 830);
      };
    }
    else {

      toggleBtn.innerHTML = "Ảnh master";

      canvas_img_show_oke.width = 1328;
      canvas_img_show_oke.height = 830;
      const img = new Image();                     // ⬅️ Tạo Image object
      img.onload = () => {
          ctx_oke.drawImage(img, 0, 0, 1328, 830);  // Vẽ lên canvas sau khi ảnh load xong
        };
      img.src = capturedImages[index_current_click].url;
      }
});

document.addEventListener("DOMContentLoaded", () => {
  status_view_master = true  //ban đầu cho xuất hiện ảnh chụp master
  const dataImg = scroll_content.dataset.img;
  const imgList = JSON.parse(dataImg);
  console.log("Danh sách ảnh:", imgList);
  // console.log("imgList.length",imgList.length);
  createProgressBoxes(imgList.length) //De hien thi thanh dem o duoi
  imgList.forEach((imgPath, index) => {

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
    divCreateList.push(div_create);

    div_create.addEventListener("click", () => {
      clearn_div_click(index,divCreateList)
      index_current_click = index;
      imgPath_current  = imgPath;
      let  du_lieu_bang = null;
      for (let data_img of data_table_browse){
        console.log("data_img",data_img,"tai index",data_img);
        du_lieu_bang = data_img?.[index];
        if (du_lieu_bang){
          break;
        }
      }
      if (status_view_master){
      canvas_img_show_oke.width = 1328;
      canvas_img_show_oke.height = 830;
      const show_img = new Image();
      show_img.src = imgPath;
      show_img.onload = () => {
        ctx_oke.drawImage(show_img, 0, 0, 1328, 830);
      };
    }
    else{

      canvas_img_show_oke.width = 1328;
      canvas_img_show_oke.height = 830;
      const img = new Image();                     // ⬅️ Tạo Image object
      img.onload = () => {
          ctx_oke.drawImage(img, 0, 0, 1328, 830);  // Vẽ lên canvas sau khi ảnh load xong
      };
    img.src = capturedImages[index].url;
    }
    show_table(du_lieu_bang)
    });
  });
});

function show_table(data){
      //  console.log("du_lieu_bang",data);
      table_show_point_detect.innerHTML = "";
      if (data) {
      // Duyệt qua từng Master
      Object.values(data).forEach(master=>{
          // Bảng master
          const masterTable = document.createElement("table");
          masterTable.className = "master-table";

          // Tiêu đề Master
          const headerRow = masterTable.insertRow();
          const masterCell = headerRow.insertCell();
          masterCell.className = "master-header";
          masterCell.textContent = `Tên master: ${master.name_master}`;

          const pointCell = headerRow.insertCell();
          pointCell.className = "master-header";
          pointCell.textContent = "Chi tiết điểm phát hiện";

          // Hàng thông tin Master
          const infoRow = masterTable.insertRow();
          const masterInfo = infoRow.insertCell();
          masterInfo.innerHTML = `
            Số lượng: ${master.number_point}<br>
            Max: ${master.max_point}mm <br>Min: ${master.min_point}mm
          `;
          // console.log("master.arr_pointreeqweqwewwewewq",master.arr_pointr)

          const pointInfo = infoRow.insertCell();
          pointInfo.appendChild(createPointTable(master.arr_pointr));

          table_show_point_detect.appendChild(masterTable);
      });
      // === Hàm tạo bảng con Point ===
      function createPointTable(points){
          const table = document.createElement("table");
          table.className = "point-table";

          // Header
          const head = table.insertRow();
          ["Tên","Chiều dài","Chiều cao","%Chiếm","Trạng thái"].forEach(t=>{
              const th = document.createElement("th");
              th.textContent = t;
              head.appendChild(th);
          });

          // Dữ liệu
          points.forEach(p=>{
              const row = table.insertRow();
              [
                p.name,
                p.width_reality,
                p.height_reality,
                p.inside_percent.toFixed(2),
                p.status_oil
              ].forEach(val=>{
                  const td = document.createElement("td");
                  td.textContent = val;
                  row.appendChild(td);
              });
          });
          return table;
      }
    };
  }

io_img_and_data.on("data_status", (data) => {
// console.log("whgwhghewqgewjhegwehw",data);

  let product_ok = data?.total_product_ok;
  let product_judment_total = data?.total_product_judment;
  if (product_judment_total != null && product_ok != null){
      // console.log("product_judment_total",product_judment_total,"s",product_ok);
      productCount.innerHTML = `OK: ${product_ok} | Tổng: ${product_judment_total}`;
  }
});

io_img_and_data.on("connect", () => {
            console.log("Đã kết nối server namespace /video");
});


io_img_and_data.on("photo_taken", (data) => {

    let data_show_table = data?.data
    let firstValue = Object.values(data_show_table)[0];
    // console.log("data nhan show bang 1",data);
    // console.log("data nhan show bang 2",du_lieu_bang);
    show_table(firstValue)
    data_table_browse.push(data_show_table)
    if (data_show_table?.[reset_data_table] == 0){
      data_table_browse = [];
    }
    let total_time  = data?.total_time;
    if (total_time){
        time_total.innerHTML= `Thời gian chạy: ${total_time}s`;
    }

    let  data_status = data?.status_judment;
      if (data_status == true){
          status_judment.innerHTML ="OK";
          status_judment.classList.add("OK");
          status_judment.classList.remove("NG");
      }
      else if (data_status == false){
          status_judment.innerHTML = "NG";
          status_judment.classList.remove("OK");
          status_judment.classList.add("NG");
      }

      let product_judment_total = data?.total_product;
      let product_ok = data?.total_product_ok;
      if (product_judment_total != null && product_ok != null){
          // console.log("product_judment_total",product_judment_total,"s",product_ok);
          productCount.innerHTML = `OK: ${product_ok} | Tổng: ${product_judment_total}`;
      }
    // console.log("Index:", data.index);
    // console.log("Total length:", data.length);
    if(data.index ==0){
        createProgressBoxes(data.length);
        clearn_div(divCreateList);
    }
    RunProgressBoxes(data.index,data.status_frame);
    Run_div(data.index,data.status_frame,divCreateList);
    // Nếu muốn hiện lên giao diện
    // document.getElementById("index_label").innerText = `Điểm: ${data.index}/${data.length}`;  //thay label
    // Phần xử lý ảnh giữ nguyên như trước
    let arrayBuffer;
    if (data.img instanceof ArrayBuffer) {
        arrayBuffer = data.img;
    } else if (data.img && data.img.data) {
        arrayBuffer = new Uint8Array(data.img.data).buffer;
    } else {
        console.error("Không nhận được dữ liệu ảnh hợp lệ:", data);
        return;
    }
    const blob = new Blob([arrayBuffer], { type: 'image/jpeg' });
    const imgUrl = URL.createObjectURL(blob);
    const img = new Image();
    img.onload = () => {
    canvas_img_show_oke.width = 1328;
    canvas_img_show_oke.height = 830;
    ctx_oke.drawImage(img, 0, 0, 1328, 830);

     };
    img.src = imgUrl;
    capturedImages.push({
        index: data.index,
        blob: blob,
        url: URL.createObjectURL(blob)  // link tạm để hiển thị
    });
});










//--------------------------------------------------------------------- Load process------------------------------------------------------//
// Tạo ô vuông tương ứng số ảnh của 1 sản phẩm (lặp lại cho toàn bộ sản phẩm)
function createProgressBoxes(totalImages) {
  progressRow.innerHTML = '';
  for (let i = 0; i < totalImages; i++) {
    const box = document.createElement('div');
    box.className = 'progress-box';
    progressRow.appendChild(box);
  }
}


function RunProgressBoxes(index,status_frame) {
  const boxes = document.querySelectorAll('.progress-box');
  if(status_frame){
  boxes[index].classList.add('done'); // đánh dấu ảnh đã xử lý
  }
  else{
     boxes[index].classList.add('error');
  }
}

function Run_div(index, status_frame, div_card) {
  if (!div_card || !div_card[index]) return; // tránh lỗi nếu index sai

  // Xóa class cũ (nếu có)
  div_card[index].classList.remove('ok', 'erro');

  // Thêm class tương ứng
  if (status_frame) {
    div_card[index].classList.add('ok');
  } else {
    div_card[index].classList.add('erro');
  }
}

function clearn_div(div_card) {
  if (!div_card) return;
  for (let i = 0; i < div_card.length; i++) {
    div_card[i].classList.remove('ok', 'erro');
  }
}
function clearn_div_click(index,div_card) {
  if (!div_card) return;
  for (let i = 0; i < div_card.length; i++) {
    div_card[i].classList.remove('div_click');
    if(index == i){
      div_card[i].classList.add('div_click');
    }
  }
}


//---------------------------------------------------------------------End Load process------------------------------------------------------//
