
import {
    postData,fetch_get,btn_open_com_config
} from "./show_main_status.js";
const infor_com_connect = document.getElementById("infor-com-connect");
const overlay_config_com = document.getElementById("overlay_config_com");
const com_close = document.getElementById("com-close");
const show_info_list_cam = document.getElementById("show_info_list_cam");
const com_select = document.getElementById("com-select");
const baud_select = document.getElementById("baud-select");
const com_open = document.getElementById("com-open");

const baudrates = [300, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600,  115200, 230400, 460800, 921600];

  
  
com_open.addEventListener("click",async()=>{
  console.log("đã nhấn vào mở cổng và lưu thông tin");
  let com_choose = com_select.value;
  let baudrate_choose = baud_select.value;
  console.log("com_choose",com_choose,"baudrate_choose",baudrate_choose);
  if (com_choose ==  null ||  baudrate_choose ==null){
    console.log("Lỗi chọn");
  }else
  {
    postData("api_config_com/open_and_save_inf",{"com_choose":com_choose,"baudrate_choose":baudrate_choose}).then(data => {
      console.log("ydgqwhdgshdgsdhs",data);
      infor_com_connect.innerHTML = "";
                   infor_com_connect.innerHTML = `
              Đã kết nối: ${data.data.device_port}
              Baudrate: ${data.data.baudrate}`;
    });
      
  }
  

  // let status_open = await fetch_request("/api_config_com/open_and_save_inf",);
  // print(status_open)



});

btn_open_com_config.addEventListener('click',async ()=>{
    console.log("Xuất hiện khung hình config camera");
    overlay_config_com.style.display = "flex";
    let data_return = await fetch_get("/api_config_com/get_list_com");
    let status_send = data_return?.status;
    if (status_send == "200OK"){
        let data = data_return?.data;
        if (data.length == 0 || data == null) {
            show_info_list_cam.innerHTML = "Hiện tại chưa có cổng COM nào đang được kết nối";
            com_select.innerHTML = ""; // Xóa các select cũ nếu có
            const option_while = document.createElement("option");
            option_while.value = ""; // giá trị rỗng để làm placeholder
            option_while.innerHTML="...";
            option_while.selected = true; // chọn mặc định
            com_select.appendChild(option_while);

            
            baud_select.innerHTML = ""; // Xóa các select cũ nếu có
            const option = document.createElement("option");
            option.value = ""; // giá trị rỗng để làm placeholder
            option.innerHTML="...";
            option.selected = true; // chọn mặc định
            baud_select.appendChild(option);

            console.log("Hiện tại chưa có cổng kết nối");
        }  
        else if (data.length != 0 ){
              com_select.innerHTML = ""; // Xóa các select cũ nếu có
              show_info_list_cam.innerHTML  = "";
              for (let i of data){
                let gate = i?.gate;
                let description =  i?.description;
                if(gate == null || description == null){
                  console.log("Mảng data gửi bị thiếu thông tin ")
                }
                 show_info_list_cam.innerHTML += `[Cổng ${gate}] Thông tin:${description}<br>`;

                const option = document.createElement("option");
                option.value = ""; // giá trị rỗng để làm placeholder
                option.value = gate; 
                option.innerHTML= String(gate);
                com_select.appendChild(option);
                }
               
               for (let i of baudrates){ 
                const option = document.createElement("option");
                option.value = ""; // giá trị rỗng để làm placeholder
                option.value = i; 
                option.innerHTML= String(i);
                baud_select.appendChild(option);
               }
            
     

        }
        let show_com_connected  = data_return?.data_connected;
        infor_com_connect.innerHTML ="";
        if (show_com_connected){
              // console.log("Baudrate:", show_com_connected.baudrate);
              // console.log("Bytesize:", show_com_connected.bytesize);
              // console.log("Device port:", show_com_connected.device_port);
              // console.log("Parity:", show_com_connected.parity);
              // console.log("Reconnect interval:", show_com_connected.reconnect_interval);
              // console.log("Stopbits:", show_com_connected.stopbits);
              // console.log("Timeout:", show_com_connected.timeout);
              infor_com_connect.innerHTML = `
              Đang kết nối: ${show_com_connected.device_port}
              Baudrate: ${show_com_connected.baudrate}`;
              // baud_select.value = parseInt(show_com_connected.parity);
              com_select.value = String(show_com_connected.device_port);
              baud_select.value = parseInt(show_com_connected.baudrate);
              // Bytesize: ${show_com_connected.bytesize}
              // Parity: ${show_com_connected.parity}
              // Stopbits: ${show_com_connected.stopbits}
              // Timeout: ${show_com_connected.timeout}
              // Reconnect interval: ${show_com_connected.reconnect_interval} 
         
          }
        else{
          infor_com_connect.innerHTML = "Chưa kết nối với cổng nào";
        }

    }
    // else{
    //   print("Nhận dữ liệu không đúng nha")
    //   data.
    //   show_info_list_cam = 
    // }

});


com_close.addEventListener("click",()=>{
     fetch('/api_config_com/exit')
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


