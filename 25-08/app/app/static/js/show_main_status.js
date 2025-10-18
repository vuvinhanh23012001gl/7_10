
export const chooseProductBtn = document.getElementById("choose-product");
export const current_panner_default = document.getElementById("paner-main");
export const headerMasterTake = document.getElementById("header-ul-li-master-take");  //chuyển hướng

export const btn_open_software_config = document.getElementById("btn-open-software-config");
export const btn_open_com_config = document.getElementById("btn-open-com-config");
export const btn_open_camera_config = document.getElementById("btn-open-camera-config");    
export const btn_close = document.getElementById("btn-close");


export const add_product = document.getElementById("add-product");
export const out_app = document.getElementById("out-app");

export const coordinate = document.getElementById("coordinate");
export const scroll_content = document.getElementById("scroll-content");
export const scroll_container = document.querySelector(".scroll-container");
export const btn_left = document.querySelector(".scroll-up");
export const btn_right = document.querySelector(".scroll-down");
export const log = document.querySelector(".log");
export const table_write_data = document.getElementById("table");
export const part_table_log = document.getElementById("part-table-log");

export const btn_square = document.getElementById("btn-square");
export const btn_circle = document.getElementById("btn-circle");
export const btn_undo = document.getElementById("btn-undo");
export const btn_erase = document.getElementById("btn-erase");
export const btn_check = document.getElementById("btn-check");

export const select_min = document.getElementById("btn-select-min");

export const btn_accept_and_send = document.getElementById("btn-accept-and-send-server"); // Nút nhấn chấp nhận kết nối
export const headerMasterAdd = document.getElementById("header-ul-li-add-take");

export let current_panner = current_panner_default;
export let index_img_current  = 0 ;

export let accept_power_by_user = false  //Bien nay khi dang nhap thanh cong o file login thi se bat thanh True
export const overlay_login =  document.getElementById("overlay_login");


export const canvas_img_show = document.getElementById("canvas-img-preview");
export const ctx = canvas_img_show.getContext("2d");
export const canvas_img_show_oke = document.getElementById("canvas-img");
export const ctx_oke = canvas_img_show_oke.getContext("2d");

export const logSocket = io("/log");

export const canvas_show = document.getElementById("canvas-img-show-add-master");
export const ctx_show = canvas_show.getContext("2d");
export function set_Z_index_canvas_show(z_Index) {
  canvas_show.style.zIndex = z_Index;
   canvas_img_show_oke.width = 0;
   canvas_img_show_oke.height = 0;
   ctx_oke.width = 0;
   ctx_oke.height = 0;
}
export function disableButtons() {
  [
    add_product,
    headerMasterAdd,
    headerMasterTake,
    btn_open_camera_config,
    btn_open_com_config,
    btn_open_software_config
  ].forEach(btn => {
    if (!btn) return;
    btn.style.pointerEvents = "none"; // ❌ chặn click chuột
    btn.style.cursor = "not-allowed"; // đổi con trỏ chuột
  });
}


export function enableButtons() {
  [
    add_product,
    headerMasterAdd,
    headerMasterTake,
    btn_open_camera_config,
    btn_open_com_config,
    btn_open_software_config
  ].forEach(btn => {
    if (!btn) return;
    btn.style.pointerEvents = "auto"; // ✅ cho phép click lại
    btn.style.opacity = "1";
    btn.style.cursor = "pointer";
  });
}

export function setAcceptPowerByUser(value) {
  sessionStorage.setItem("accept_power_by_user", value ? "true" : "false");
}

export function getAcceptPowerByUser() {
  // Nếu chưa có trong sessionStorage thì gán mặc định là "false"
  if (sessionStorage.getItem("accept_power_by_user") === null) {
    sessionStorage.setItem("accept_power_by_user", "false");
  }
  
  // Trả về true/false đúng kiểu boolean
  return sessionStorage.getItem("accept_power_by_user") === "true";
}





export function setCurrentPanner(panner) {
  current_panner = panner;
}
export function set_index_img_current(index) {
  index_img_current = index;      
}


export async function postData(url = "", data = {}) {
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error("Lỗi khi POST:", error);
    return null;
  }
}
export async function fetch_get(domanin_str) {
  // domanin_str = "/hello"
  try {
    const response = await fetch(domanin_str, {
      method: "GET",
      headers: { "Accept": "application/json" }
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    return data;                          // Trả về dữ liệu cho nơi gọi
  } catch (err) {
    console.error("Fetch thất bại:", err);
    return { error: err.message };         // Trả về thông báo lỗi
  }
}

