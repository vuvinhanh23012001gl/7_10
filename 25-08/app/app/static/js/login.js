

// Lấy các phần tử bằng ID
const tabLogin = document.getElementById('tab_login');
const tabSignup = document.getElementById('tab_signup');
const formLogin = document.getElementById('form_login');
const formSignup = document.getElementById('form_signup');
const closeSign = document.getElementById('btn_exit_signup');
const notifyLogin = document.getElementById('notification_login');
const overlay_login =  document.getElementById("overlay_login");

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