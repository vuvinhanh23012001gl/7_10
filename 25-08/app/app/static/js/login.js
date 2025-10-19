
import {
  overlay_login,setAcceptPowerByUser,enableButtons,disableButtons
} from "./show_main_status.js";   
 import { set_user_or_admin } from "/static/js/user_role.js";
// Lấy các phần tử bằng ID
const tabLogin = document.getElementById('tab_login');
const tabSignup = document.getElementById('tab_signup');
const formLogin = document.getElementById('form_login');
const formSignup = document.getElementById('form_signup');
const closeSign = document.getElementById('btn_exit_signup');
const notifyLogin = document.getElementById('notification_login');
const user_register_an_account = document.getElementById('signup_user');
const pass_register_an_account = document.getElementById('signup_pass');
const confirm_pass_register_an_account = document.getElementById('signup_pass_confirm');
const notification_signup = document.getElementById("notification_signup");

const signup_first_name = document.getElementById("signup_first_name");
const signup_last_name = document.getElementById("signup_last_name");
const signup_factory = document.getElementById("signup_factory");
const signup_line = document.getElementById("signup_line");

// login.addEventListener("click",()=>{
//        overlay_login.style.display = "flex";
// });
// Hàm reset trạng thái active

function resetActive() {
  tabLogin.classList.remove('active');
  tabSignup.classList.remove('active');
  formLogin.classList.remove('active');
  formSignup.classList.remove('active');
}

// Khi click vào "Đăng nhập"
tabLogin.addEventListener('click', () => {
  resetActive();
  tabLogin.classList.add('active');
  formLogin.classList.add('active');
});

// Khi click vào "Đăng ký"
tabSignup.addEventListener('click', () => {
  resetActive();
  tabSignup.classList.add('active');
  formSignup.classList.add('active');
});

// Khi nhấn "Thoát" trong form Đăng ký
closeSign.addEventListener('click', () => {
  resetActive();
  tabLogin.classList.add('active');
  formLogin.classList.add('active');
});


formSignup.addEventListener('submit', async (e) => {
  e.preventDefault(); // Ngăn form reload trang
    let data_user_register_an_account = user_register_an_account.value.trim();
    let data_pass_register_an_account = pass_register_an_account.value.trim();
    let data_confirm_pass_register_an_account= confirm_pass_register_an_account.value.trim();
    let data_signup_first_name = signup_first_name.value.trim();
    let data_signup_last_name = signup_last_name.value.trim();
    let data_signup_factory = signup_factory.value.trim();
    let data_signup_line = signup_line.value.trim();
    
     if (/\s/.test(data_user_register_an_account) || /\s/.test(data_pass_register_an_account)|| /\s/.test(data_confirm_pass_register_an_account)) {
     showError_singup("❌ Tài khoản và mật khẩu không được chứa khoảng trắng!");
     return;
     }

     // Kiểm tra ký tự hợp lệ: a–z, A–Z, 0–9
     const regex = /^[A-Za-z0-9]+$/;
     if (!regex.test(data_pass_register_an_account) || !regex.test(data_user_register_an_account)|| !regex.test(data_confirm_pass_register_an_account)) {
     showError_singup("❌ Tài khoản và mật khẩu không được chứa ký tự đặc biệt hoặc dấu tiếng Việt!");
     return;
     }
     if (data_pass_register_an_account !== data_confirm_pass_register_an_account) {
      showError_singup("❌ Xác nhận mật khẩu không khớp. Nhập lại mật khẩu");
     return;
     }
      showMessage_singup("✅ Đang kiểm tra thông tin...");
    try {
      const res = await fetch('/api_login_software/register_an_account', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({first_name:data_signup_first_name,last_name:data_signup_last_name,
            factory:data_signup_factory,line:data_signup_line,
            user:data_user_register_an_account,pass:data_pass_register_an_account
         })
      });

      const data = await res.json();
      if (data.success) {
        
        notification_signup.textContent = data.message;
        notification_signup.style.color = '#10c060';
        // console.log("Đăng kí thành công!");
      } else {
        notification_signup.textContent = data.message;
        notification_signup.style.color = '#ff6060';
        // console.log("Đăng thất bại!");
      }
    } catch (err) {
      notification_signup.textContent = 'Lỗi kết nối tới server!';
      notification_signup.style.color = '#ff6060';
    }
});




















formLogin.addEventListener('submit', async (e) => {
  e.preventDefault(); // Ngăn form reload trang
  const user = document.getElementById('login_user').value.trim();
  const pass = document.getElementById('login_pass').value.trim();
     if (!user || !pass) {
     showError("⚠️ Vui lòng nhập đầy đủ tài khoản và mật khẩu!");
     return;
     }

     // Kiểm tra khoảng trắng
     if (/\s/.test(user) || /\s/.test(pass)) {
     showError("❌ Tài khoản và mật khẩu không được chứa khoảng trắng!");
     return;
     }

     // Kiểm tra ký tự hợp lệ: a–z, A–Z, 0–9
     const regex = /^[A-Za-z0-9]+$/;
     if (!regex.test(user) || !regex.test(pass)) {
     showError("❌ Không được chứa ký tự đặc biệt hoặc dấu tiếng Việt!");
     return;
     }

     // Kiểm tra độ dài
     if (user.length == 0) {
     showError("❌ Tài khoản phải có ít nhất 1 ký tự!");
     return;
     }

     if (pass.length == 0) {
     showError("❌ Mật khẩu phải có ít nhất 1 ký tự!");
     return;
     }

  // Nếu hợp lệ → gọi hàm gửi dữ liệu
     showMessage ("✅ Đang kiểm tra thông tin...");
  try {
    const res = await fetch('/api_login_software/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: user, password: pass })
    });
    const data = await res.json();
    if (data.success) {
      notifyLogin.textContent = 'Đăng nhập thành công!';
      notifyLogin.style.color = '#10c060';
      overlay_login.style.display = "none";
      console.log("Đăng nhập thành công!");
      setAcceptPowerByUser(true);
      let type_user = data?.type;
      console.log("type_user",type_user);
      if (type_user == true){
          console.log("Bạn vưa đăng nhập với tài khoản Admin")
          set_user_or_admin(true); //admin
          enableButtons();
          //thuc hien mot so quyen moi admin   
      }   
      else if (type_user == false){
          console.log("Bạn vưa đăng nhập với tài khoản User")
          //thuc hien mot so quyen moi user
          set_user_or_admin(false);  //user
          disableButtons();
      }
      else{
           notifyLogin.textContent = 'Lỗi kết nối tới server!';
           notifyLogin.style.color = '#ff6060';
      }
    } else {
      notifyLogin.textContent = data.message || 'Sai tài khoản hoặc mật khẩu!';
      notifyLogin.style.color = '#ff6060';
      overlay_login.style.display = "flex";
    }
  } catch (err) {
    notifyLogin.textContent = 'Lỗi kết nối tới server!';
    notifyLogin.style.color = '#ff6060';
  }
});

function showError(msg) {
  notifyLogin.textContent = msg;
  notifyLogin.style.color = "red";
}
function showMessage(msg) {
  notifyLogin.textContent = msg;
  notifyLogin.style.color = "lightgreen";
}


function showError_singup(msg) {
  notification_signup.textContent = msg;
  notification_signup.style.color = "red";
}
function showMessage_singup(msg) {
  notification_signup.textContent = msg;
  notification_signup.style.color = "lightgreen";
}