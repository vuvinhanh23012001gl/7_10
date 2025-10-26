import {
    postData,fetch_get,btn_open_software_config
} from "./show_main_status.js";

const overlay_config_software  = document.getElementById("overlay_config_software");
const close_settings_software  = document.getElementById("close-settings");
const btn_open_img_software = document.getElementById("set-sound");
const btn_open_product = document.getElementById("set-notification");//log san pham
const btn_open_sofware =  document.getElementById("set-darkmode");//log software
const save_settings = document.getElementById("save-settings");
const btn_open_cosole =  document.getElementById("set-cosole");
const set_time_save_log_img = document.getElementById("set-time-save-log-img");
const set_time_save_log_excell = document.getElementById("set-time-save-log-excell");
const set_time_save_log_software = document.getElementById("set-time-save-log-software");

const log_inf = document.getElementById("infor-log-config-software");
 

btn_open_software_config.addEventListener("click",async()=>{
      overlay_config_software.style.display = "flex";
      let data = await fetch_get("/api_config_software/config_software");
      let data_return = data?.data;
      console.log(data_return)

      let open_log_img_oil = data_return?.open_log_img_oil;
      let open_log_product = data_return?.open_log_product;
      let open_log_software = data_return?.open_log_software;
      let open_log_console = data_return?.open_log_console;
            

      let data_set_time_save_log_img = data_return?.set_time_save_log_img
      let data_set_time_save_log_excell =   data_return?.set_time_save_log_excell;
      let data_set_time_save_log_software =   data_return?.set_time_save_log_software;
    
      
      if(!data_set_time_save_log_img || !data_set_time_save_log_excell||!data_set_time_save_log_software){
            set_time_save_log_img.value = 30;
            set_time_save_log_excell.value = 30;
            set_time_save_log_software.value = 30;
      }
      else{
        set_time_save_log_img.value = data_set_time_save_log_img;
        set_time_save_log_excell.value = data_set_time_save_log_excell;
        set_time_save_log_software.value = data_set_time_save_log_software;

      }

        btn_open_cosole.checked = open_log_console;
        btn_open_img_software.checked  = open_log_img_oil;
        btn_open_product.checked =  open_log_product;
        btn_open_sofware.checked = open_log_software;
});

save_settings.addEventListener("click",async()=>{
      postData("api_config_software/change_log",{"log_img":btn_open_img_software.checked 
        ,"log_product":btn_open_product.checked
        ,"log_software":btn_open_sofware.checked
        ,"log_console":btn_open_cosole.checked
        ,"set_time_save_log_software":set_time_save_log_software.value
        ,"set_time_save_log_img": set_time_save_log_img.value 
        ,"set_time_save_log_excell":set_time_save_log_excell.value
    }).then(data => {
       console.log(data);
       let infor =  data?.status;
       log_inf.innerText = infor;
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

 