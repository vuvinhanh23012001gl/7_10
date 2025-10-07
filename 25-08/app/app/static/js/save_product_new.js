  const fileInput = document.getElementById("file_upload");
  const fileInfo = document.getElementById("fileInfo");
  const previewImg = document.getElementById("previewImg");
  const form = document.getElementById("productForm");
  const close = document.getElementById("close");
  let selectedFile = null;
  window.addEventListener("popstate", function(event) {
    // Khi người dùng nhấn Back
    window.location.href = "/";
});
  // --- Khi chọn ảnh thì preview offline trước ---
  fileInput.addEventListener("change", function() {
    let file = this.files[0];
    if (file) {
      selectedFile = file;
      fileInfo.textContent = "Đã chọn: " + file.name;

      if (file.type.startsWith("image/")) {
        let reader = new FileReader();
        reader.onload = function(e) {
          previewImg.src = e.target.result;
          previewImg.style.display = "block";
        }
        reader.readAsDataURL(file);
      } else {
        previewImg.style.display = "none";
      }
    } else {
      fileInfo.textContent = "Chưa chọn file nào";
      previewImg.style.display = "none";
      selectedFile = null;
    }
  });

  // --- Xử lý submit form ---
  form.addEventListener("submit", function(e) {
    e.preventDefault(); // chặn submit mặc định (reload trang)
    let formData = new FormData(form); // lấy toàn bộ dữ liệu form
    let product_id = cleanVietnameseToAscii(String(formData.get("product_id")));
    let product_name = String(formData.get("product_name"));
    let limit_x = formData.get("limit_x");
    let limit_y = formData.get("limit_y");
    let limit_z = formData.get("limit_z");
    
    formData.set("product_id", product_id);
    formData.set("product_name", product_name);
    // Kiểm tra rỗng
    if (!product_id || !product_name || !limit_x || !limit_y || !limit_z ) {
        alert("Vui lòng nhập đầy đủ thông tin và chọn file!");
        return; // dừng lại, không gửi fetch
    }
    
    if (limit_x < 0 || limit_y < 0 || limit_z < 0 ) {
        alert("Vui lòng nhập giá trị lớn hơn 0");
        return; // dừng lại, không gửi fetch
    }

    console.log(formData);
    fetch(form.action, {
      method: "POST",
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      if (data.success == true) {
        alert("Lưu thành công!");
      }   
      else{
          if (data?.ErrorDataIncorect) {
              alert(data.ErrorDataIncorect);   
          }

          else if (data?.ErrorNotSendFile) {
              alert(data.ErrorNotSendFile);
          }

          else if (data?.ErroHasExitsed) {
              alert(data.ErroHasExitsed);
          }

          else if (data?.ErroNotFileImg) {
              alert(data.ErroNotFileImg);
          }
      }
    })
    .catch(err => {
      console.error(err);
      alert("Lỗi kết nối server!");
    });
  });
  function cleanVietnameseToAscii(str) {
  if (!str) return "";
  str = String(str).trim().replace(/\s+/g, "");
  str = str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  return str;
}
const logSocket = io("/log");
logSocket.on("log_message", function (data) {
    console.log(data)
    const logBox = document.getElementById("log-entry");
    if (logBox) {
          const log = data.log_create_product;
          let html = `<table border="1" cellspacing="0" cellpadding="5" style="border-collapse: collapse; width:100%;">`;
          html += `<tr><th>STT</th><th>ID</th><th>Tên sản phẩm</th><th>Max X</th><th>Max Y</th><th>Max Z</th></tr>`;
          log.list_id.forEach((id,idx) => {
              const name = log.list_name[idx] || "";
              const X = log.xyz[idx][0] || "";
              const Y = log.xyz[idx][1] || "";
              const Z = log.xyz[idx][2] || "";
              html += `<tr>
                        <td>${idx+1}</td>
                        <td>${id}</td>
                        <td>${name}</td>
                        <td>${X}</td>
                        <td>${Y}</td>
                        <td>${Z}</td>
                      </tr>`;
          });
          html += `</table>`;
          logBox.innerHTML = html;
    } else {
        console.warn("Không tìm thấy log box");
    }
});
close.addEventListener("click",function(){
    window.location.href = "/";
})