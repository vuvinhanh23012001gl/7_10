import {
    postData,fetch_get
} from "./show_main_status.js";
const btn_open_software_config = document.getElementById("btn-open-software-config");
const overlay_config_software  = document.getElementById("overlay_config_software");
const close_settings_software  = document.getElementById("close-settings");
const sw_name = document.getElementById("sw-name");
const sw_version = document.getElementById("sw-version");
const sw_author = document.getElementById("sw-author");
const path_oil = document.getElementById("path-oil");
const path_product = document.getElementById("path-product");
const path_software = document.getElementById("path-software");
const btn_open_img_software = document.getElementById("set-sound");
const btn_open_product = document.getElementById("set-notification");//log san pham
const btn_open_sofware =  document.getElementById("set-darkmode");//log software
const save_settings = document.getElementById("save-settings");



btn_open_software_config.addEventListener("click",async()=>{
      overlay_config_software.style.display = "flex";
      let data = await fetch_get("/api_config_software/config_software");
      let data_return = data?.data;
      console.log(data_return)
      let name = data_return?.name;
      let version =  data_return?.version;
      let author = data_return?.author;
      let path_log_img_oil = data_return?.path_log_img_oil;
      let path_log_product = data_return?.path_log_product;
      let path_log_software = data_return?.path_log_software;

      let open_log_img_oil = data_return?.open_log_img_oil;
      let open_log_product = data_return?.open_log_product;
      let open_log_software = data_return?.open_log_software;
        console.log("=== THÔNG TIN PHẦN MỀM ===");
        console.log("Tên phần mềm:", name);
        console.log("Phiên bản:", version);
        console.log("Tác giả:", author);
        console.log("=== LOG PATH & TRẠNG THÁI ===");
        console.log("Log ảnh dầu:", open_log_img_oil ? "Mở" : "Đóng", "| Path:", path_log_img_oil);
        console.log("Log sản phẩm:", open_log_product ? "Mở" : "Đóng", "| Path:", path_log_product);
        console.log("Log phần mềm:", open_log_software ? "Mở" : "Đóng", "| Path:", path_log_software);

        sw_name.innerHTML = name;
        sw_version.innerHTML =version;
        sw_author.innerHTML = author;
        path_oil.innerHTML = path_log_img_oil;
        path_product.innerHTML = path_log_product;
        path_software.innerHTML = path_log_software;

        btn_open_img_software.checked  = open_log_img_oil;
        btn_open_product.checked =  open_log_product;
        btn_open_sofware.checked = open_log_software;
});

save_settings.addEventListener("click",async()=>{
      postData("api_config_software/change_log",{"log_img":btn_open_img_software.checked ,"log_product":btn_open_product.checked,"log_software":btn_open_sofware.checked}).then(data => {
       console.log(data);
    });

});


close_settings_software.addEventListener("click",()=>{
     fetch('/api_config_software/exit')
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

 