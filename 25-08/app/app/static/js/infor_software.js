
import {
    fetch_get
} from "./show_main_status.js";
const overlay_inforsoftware = document.getElementById("overlay_inforsoftware");  
const btn_infor_software = document.getElementById("get_infor_software");
const sw_name = document.getElementById("sw-name");
const sw_version = document.getElementById("sw-version");
const sw_author = document.getElementById("sw-author");
const path_oil = document.getElementById("path-oil");
const path_product = document.getElementById("path-product");
const path_software = document.getElementById("path-software");
const btn_exit_infor_software = document.getElementById("btn_exit_infor_software");

btn_infor_software.addEventListener("click",async()=>{
overlay_inforsoftware.style.display = "flex";
        let data = await fetch_get("/api_inf_software/data_infor_software");
        let data_return = data?.data;
        let name = data_return?.name;
        let version =  data_return?.version;
        let author = data_return?.author;
        let path_log_img_oil = data_return?.path_log_img_oil;
        let path_log_product = data_return?.path_log_product;
        let path_log_software = data_return?.path_log_software;
        console.log("=== THÔNG TIN PHẦN MỀM ===");
        console.log("Tên phần mềm:", name);
        console.log("Phiên bản:", version);
        console.log("Tác giả:", author);
        console.log("=== LOG PATH & TRẠNG THÁI ===");
        console.log("Path:", path_log_img_oil);
        console.log("Path:", path_log_product);
        console.log("Path:", path_log_software);
        sw_name.innerHTML = name;
        sw_version.innerHTML =version;
        sw_author.innerHTML = author;
        path_oil.innerHTML = path_log_img_oil;
        path_product.innerHTML = path_log_product;
        path_software.innerHTML = path_log_software;

});
btn_exit_infor_software.addEventListener("click",()=>{
    overlay_inforsoftware.style.display = "none";
});