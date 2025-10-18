import {
   fetch_get,btn_open_camera_config
} from "./show_main_status.js";
console.log("Đã vào camera config");
const close_config_camera = document.getElementById("close-config-camera");
const overlay_config_camera = document.querySelector(".overlay_config_camera");

const cam_model = document.getElementById("cam-model");
const cam_serial = document.getElementById("cam-serial");
const cam_vendor = document.getElementById("cam-vendor");
const cam_device_class = document.getElementById("device-class");
const cam_status = document.getElementById("cam-status");
const cam_exposure = document.getElementById("cam-exposure");
const cam_resolution = document.getElementById("cam-resolution");
const cam_fps = document.getElementById("cam-fps");




btn_open_camera_config.addEventListener('click',async()=>{
    console.log("Xuất hiện khung hình config camera");
    overlay_config_camera.style.display = "flex";
    // postData("api_config_camera/get_data_show",{"com_choose":com_choose,"baudrate_choose":baudrate_choose}).then(data => {
    //       console.log("ydgqwhdgshdgsdhs",data);
    //       infor_com_connect.innerHTML = "";
    //                    infor_com_connect.innerHTML = `
    //               Đã kết nối: ${data.data.device_port}
    //               Baudrate: ${data.data.baudrate}`;
    // });
   let data_return = await fetch_get("/api_config_camera/get_data_show");
   let status_send = data_return?.status;
   if (status_send){
     let data = data_return?.data;
     console.log(data);
     if (data == false){
            console.log("Dữ liệu rỗng");
     }
     else{
           let device_class =  data?.device_class;
           let exposure = data?.exposure;
           let frame = data?.frame;
         //    let gain = data?.gain;
           let height = data?.height;
           let model = data?.model;
           let serial = data?.serial;
           let vendor = data?.vendor;
           let width = data?.width;
           // Gán vào innerHTML
            cam_model.innerHTML = model || "N/A";
            cam_serial.innerHTML = serial || "N/A";
            cam_vendor.innerHTML = vendor || "N/A";
            cam_device_class.innerHTML = device_class || "N/A";
            // Status có thể tùy theo logic (ví dụ luôn Online)
            cam_status.innerHTML = "Online";
            // Exposure
            cam_exposure.value = exposure || "N/A";
            // Resolution = width x height
            cam_resolution.value = `${width} x ${height}`;
            // FPS
            cam_fps.value = frame || "N/A";
                    
     }
     

   }

});

close_config_camera.addEventListener("click",()=>{
     fetch('/api_config_camera/exit')
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


