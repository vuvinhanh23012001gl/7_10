//Phan nay se bat lai sau khi hoan thanh
let Limit_x = 0;
let Limit_y = 0;
let Limit_z = 0;
let Limit_k = 0;

const videoSocket = io("/video");
videoSocket.on("camera_frame", function (data) {
    document.getElementById("cam_feed").src = "data:image/jpeg;base64," + data.image;
});

window.addEventListener('beforeunload', function() {
    navigator.sendBeacon('/api_new_model/stop-video'); 
});

const logSocket = io("/log");
logSocket.on("log_message", function (data) {
    const logBox = document.getElementById("summaryBox");
    if (logBox) {
        logBox.value += data.log_training + "\n";
        logBox.scrollTop = logBox.scrollHeight;
    } else {
        console.warn("Không tìm thấy textarea log");
    }
});
logSocket.on("log_message_product", function (data) {
    const textarea = document.getElementById('infoBox');  
    console.log(data);
    if (textarea) {
        let output = "";
        data = data.manage_product_type;  // ⬅️ Đúng
        for (const key in data) {
            const type = data[key];
            output += `🔹 ID Loại: ${type.type_id}\n`;
            output += `📦 Tên loại: ${type.type_name}\n`;
            output += `📌 Số điểm kiểm tra: ${type.point_check.length}\n`;
            type.point_check.forEach((point, idx) => {
                output += `   ▶️ Điểm ${idx + 1}: x=${point.x}, y=${point.y}, z=${point.z}, brightness=${point.brightness}\n`;
            });
            output += '\n'; 
        }
        textarea.value = output;
        textarea.scrollTop = textarea.scrollHeight;
    } else {
        console.warn("Không tìm thấy textarea log");
    }
});

let isReadonly = null; // trạng thái hiện tại
document.getElementById("btn_save_limit").addEventListener("click", function (event) {
    event.preventDefault();
    let inputs = document.querySelectorAll("#box-limmit input");

    if (!isReadonly) {
        // Chế độ Lưu → kiểm tra có nhập chưa
        let valid = true;
        inputs.forEach(input => {
            if (input.value.trim() === "") {
                valid = false;
                input.style.border = "2px solid red";
            } else {
                input.style.border = "";
            }
        });

        if (!valid) {
            alert("⚠️ Vui lòng nhập đủ giới hạn X, Y, Z,K!");
            return;
        }

        // Nếu hợp lệ thì set readonly
        inputs.forEach(input => input.readOnly = true);
        this.innerText = "Chỉnh sửa giới hạn"; // đổi tên nút
        isReadonly = true;
        // Lấy giá trị để xử lý
        let limit_x = document.querySelector("input[name=limit_x]").value;
        let limit_y = document.querySelector("input[name=limit_y]").value;
        let limit_z = document.querySelector("input[name=limit_z]").value;
        let limit_k = document.querySelector("input[name=limit_k]").value;
        if (limit_x < 0  ||  limit_y< 0 || limit_z < 0 || limit_k < 0)
        {   
            document.querySelector("input[name=limit_x]").value = 0;
            document.querySelector("input[name=limit_y]").value = 0;
            document.querySelector("input[name=limit_z]").value = 0;
            document.querySelector("input[name=limit_k]").value = 0;
            alert("⚠️ Không được cài giới hạn x,y,z,k nhỏ hơn 0");
            return;
        }
          Limit_x = limit_x;
          Limit_y = limit_y;
          Limit_z = limit_z;
          Limit_k = limit_k;
          console.log("đã thay đổi Limit");
          console.log("Đã lưu:", limit_x, limit_y, limit_z,limit_k);
    } else {
        // Chế độ Chỉnh sửa → bỏ readonly
        inputs.forEach(input => input.readOnly = false);
        this.innerText = "Lưu giới hạn";
        isReadonly = false;
    }
});


let selectedPointInputs = null;
let selectedPointIndex = null;
document.querySelector('form').addEventListener('submit', function(event) {
  event.preventDefault();  // Ngăn reload

  const form = event.target;
  const deviceIdInput = form.querySelector('input[name="deviceId"]');   
  const deviceNameInput = form.querySelector('input[name="deviceName"]');
  const numberTrainningInput = form.querySelector('input[name="number_trainings"]');   
  const shifXInput = form.querySelector('input[name="shif_x"]');
  const shifYInput = form.querySelector('input[name="shif_y"]');
  const shifZInput = form.querySelector('input[name="shif_z"]');

  const deviceId = parseInt(deviceIdInput.value, 10);
  const deviceName = deviceNameInput.value.trim();
  const Training = parseInt(numberTrainningInput.value,10);
  const shifX = parseFloat(shifXInput.value);
  const shifY = parseFloat(shifYInput.value);
  const shifZ = parseFloat(shifZInput.value);
  
  if (isNaN(deviceId) || deviceId < 0) {
    alert('❌ ID thiết bị phải là số lớn hơn hoặc bằng 0');
    deviceIdInput.focus();
    return;
  }
  if (isNaN(Training) || Training < 1) {
    alert('❌ Số lần training phải là số lớn hơn hoặc bằng 1');
    numberTrainningInput.focus();
    return;
  }

  if (/\s/.test(deviceName) || deviceName === '') {
    alert('❌ Tên thiết bị không được chứa khoảng trắng và không được để trống');
    deviceNameInput.focus();
    return;
  }

  const shifts = [
    {value: shifX, name: 'Di chuyển theo trục x', input: shifXInput},
    {value: shifY, name: 'Di chuyển theo trục y', input: shifYInput},
    {value: shifZ, name: 'Di chuyển theo trục z', input: shifZInput},
  ];

  for (const shift of shifts) {
    if (isNaN(shift.value) || shift.value <= 0 || shift.value >= 10) {
      alert(`❌ Giá trị ${shift.name} phải lớn hơn 0 và nhỏ hơn 10`);
      shift.input.focus();
      return;
    }
  }

  const pointsContainer = document.getElementById('pointsContainer');
  const pointGroups = pointsContainer.querySelectorAll('.point-group');

  for (let i = 0; i < pointGroups.length; i++) {
    const group = pointGroups[i];
    const idx = i + 1;

    const inputX = group.querySelector('input[name="point_x[]"]');
    const inputY = group.querySelector('input[name="point_y[]"]');
    const inputZ = group.querySelector('input[name="point_z[]"]');
    const inputK = group.querySelector('input[name="point_k[]"]');

    if (!inputX || !inputY || !inputZ || !inputK) {
      alert(`❌ Điểm dầu ${idx} thiếu trường dữ liệu`);
      return;
    }

    const x = parseFloat(inputX.value);
    const y = parseFloat(inputY.value);
    const z = parseFloat(inputZ.value);
    const k = parseFloat(inputK.value);

    const errorMsg = validatePoint(idx, x, y, z, k);
    if (errorMsg) {
      alert(errorMsg);
      inputX.focus();
      return;
    }
  }

  // ✅ Nếu mọi thứ đều OK → gửi form bằng fetch
  const formData = new FormData(form);

  fetch('/api_new_model/submit', {
    method: 'POST',
    body: formData
  })
  .then(res => res.text())
  .then(data => {
    console.log("✅ Server trả về:", data);
    console.log("✅ Gửi form thành công!");
    // form.reset(); // Nếu muốn xóa dữ liệu form sau khi gửi
  })
  .catch(err => {
    console.error("❌ Lỗi khi gửi form:", err);
    alert("❌ Gửi form thất bại.");
  });
   // tao ra nut nhan replay
  const replay_run = document.getElementById("replay-run");
  replay_run.style.display = "block";

});

function addPoint() {
  if (isReadonly == null){
    alert("Hãy nhập giới hạn x y z k");
    return;
  }
  console.log("Giới hạn x y z k ",Limit_x,Limit_y,Limit_z,Limit_k);
  const container = document.getElementById('pointsContainer');
  const currentCount = container.querySelectorAll('.point-group').length + 1;

  const group = document.createElement('div');
  group.classList.add('point-group');

  const labelLine = document.createElement('div');
  labelLine.classList.add('point-label');
  labelLine.textContent = `Điểm dầu ${currentCount}`;
  group.appendChild(labelLine);

  const inputsRow = document.createElement('div');
  inputsRow.classList.add('inputs-row');

  const inputs = {}; // lưu input theo tên

  ['X', 'Y', 'Z', 'K'].forEach(letter => {
    const label = document.createElement('label');
    label.textContent = letter;

    const input = document.createElement('input');
    input.type = 'number'; // Chỉ cho nhập số
    input.required = true; // Bắt buộc nhập
    input.min = 0; // Giá trị nhỏ nhất
    input.name = `point_${letter.toLowerCase()}[]`;

    inputs[letter] = input;

    label.appendChild(input);
    inputsRow.appendChild(label);
  });

  // Tạo 3 nút — GIỮ NGUYÊN CLASS bạn đã dùng
  const btnStart = document.createElement('button');
  btnStart.type = 'button';
  btnStart.textContent = 'Start';
  btnStart.classList.add('btn', 'btn-sm', 'btn-primary');
  btnStart.style.marginLeft = '15px';
  btnStart.addEventListener('click', () => handleStart(currentCount, inputs));

  const btnSelect = document.createElement('button');
  btnSelect.type = 'button';
  btnSelect.textContent = 'Chọn';
  btnSelect.classList.add('btn', 'btn-sm', 'btn-primary');
  btnSelect.style.marginLeft = '10px';
  btnSelect.addEventListener('click', () => handleSelect(currentCount, inputs));

  const btnSave = document.createElement('button');
  btnSave.type = 'button';
  btnSave.textContent = 'Save';
  btnSave.classList.add('btn', 'btn-sm', 'btn-primary');
  btnSave.style.marginLeft = '10px';
  btnSave.addEventListener('click', () => handleSave(currentCount, inputs, btnSave));

  const btnErase = document.createElement('button');
  btnErase.type = 'button';
  btnErase.textContent = 'Xóa';
  btnErase.classList.add('btn', 'btn-sm', 'btn-primary','btn-erase');
  btnErase.style.marginLeft = '10px';
  btnErase.addEventListener('click', () => handleErase(group));

  // Thêm nút vào dòng
  inputsRow.appendChild(btnStart);
  inputsRow.appendChild(btnSelect);
  inputsRow.appendChild(btnSave);
  inputsRow.appendChild(btnErase);
  group.appendChild(inputsRow);
  container.appendChild(group);
}
function handleErase(group) {
  if (group && group.parentNode) {
    group.remove();
    // Sau khi xóa, cập nhật lại số thứ tự các label
    const groups = document.querySelectorAll('#pointsContainer .point-group');
    groups.forEach((g, i) => {
      const label = g.querySelector('.point-label');
      if (label) {
        label.textContent = `Điểm dầu ${i + 1}`;
      }
    });

    console.log('🗑️ Đã xóa group và cập nhật lại thứ tự.');
  }
}
function handleStart(index, inputs) {
  // Lấy giá trị từ các input
  const x = parseFloat(inputs.X.value);
  const y = parseFloat(inputs.Y.value);
  const z = parseFloat(inputs.Z.value);
  const brightness = parseFloat(inputs.K.value); // K là độ sáng

  const errorMsg = validatePoint(index, x, y, z, brightness);
  if (errorMsg) {
    alert(errorMsg);
    return;
  }

  // ✅ Gửi dữ liệu tới server
  fetch('/api_new_model/run_point', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      x: x,
      y: y,
      z: z,
      brightness: brightness
    })
  })
    .then(response => response.json())
    .then(data => {
      console.log("Trạng thái:",data.message)
      console.log(`✅ Đã gửi điểm ${index} đến thiết bị. Phản hồi: ${data.message}`);
    })
    .catch(error => {
      console.error('Lỗi khi gửi điểm:', error);
      alert('❌ Gửi dữ liệu thất bại.');
    });
}

function handleSelect(pointIndex, inputs) {
  console.log(`✔ Chọn tọa độ điểm dầu #${pointIndex}`);
  selectedPointInputs = inputs;
  selectedPointIndex = pointIndex;
  alert(`🎯 Đã chọn điểm dầu #${pointIndex} để điều chỉnh`);
}

function handleSave(index, inputs, btnSave) {
  const x = parseFloat(inputs.X.value);
  const y = parseFloat(inputs.Y.value);
  const z = parseFloat(inputs.Z.value);
  const brightness = parseFloat(inputs.K.value);

  const errorMsg = validatePoint(index, x, y, z, brightness);
  if (errorMsg) {
    alert(errorMsg);
    return; // dừng xử lý nếu lỗi
  }

  const isReadOnly = inputs.X.readOnly;

  if (!isReadOnly) {
    // Khóa readonly, đổi nút thành "Hủy"
    inputs.X.readOnly = true;
    inputs.Y.readOnly = true;
    inputs.Z.readOnly = true;
    inputs.K.readOnly = true;

    btnSave.textContent = 'Hủy';
    btnSave.classList.remove('btn-primary');
    btnSave.classList.add('btn-danger');

    console.log(`🔒 Đã khóa chỉnh sửa cho điểm dầu #${index}`);
  } else {
    // Mở khóa, đổi nút về "Save"
    inputs.X.readOnly = false;
    inputs.Y.readOnly = false;
    inputs.Z.readOnly = false;
    inputs.K.readOnly = false;

    btnSave.textContent = 'Save';
    btnSave.classList.remove('btn-danger');
    btnSave.classList.add('btn-primary');

    console.log(`✏️ Cho phép chỉnh sửa lại điểm dầu #${index}`);
  }
}

function validatePoint(index, x, y, z, brightness) {
  if (isNaN(x) || isNaN(y) || isNaN(z) || isNaN(brightness)) {
    return `❌ Điểm dầu ${index}: Các giá trị X, Y, Z, K phải là số hợp lệ và không được để trống`;
  }
  if (x < 0 || y < 0 || z < 0 || brightness < 0) {
    return `❌ Điểm dầu ${index}: Giá trị X, Y, Z, K phải lớn hơn hoặc bằng 0`;
  }
  if (x > Limit_x) {
    return `❌ Điểm dầu ${index}: Giá trị X phải nhỏ hơn hoặc bằng ${Limit_x}`;
  }
  if (y > Limit_y) {
    return `❌ Điểm dầu ${index}: Giá trị Y phải nhỏ hơn hoặc bằng ${Limit_y}`;
  }
  if (z > Limit_z) {
    return `❌ Điểm dầu ${index}: Giá trị Z phải nhỏ hơn hoặc bằng ${Limit_z}`;
  }
  if (brightness > Limit_k) {
    return `❌ Điểm dầu ${index}: Giá trị ánh sáng (K) phải nhỏ hơn hoặc bằng ${Limit_k}`;
  }
  return null; // không lỗi
}
document.querySelector('.btn_inc_dec').addEventListener('click', function (e) {
  if (e.target.id === "case_specail") return;
  if (!e.target.matches('button')) return;
  if (e.target.id === "replay-run"){
      fetch('/api_new_model/replay')
      .then(response => response.json())
      .then(data => {
        console.log('📥 Server trả về:', data);
      })
      .catch(err => {
        console.error('❌ Lỗi khi gửi GET:', err);
      });
    return;
  }
  if (!selectedPointInputs) {
    alert('❗ Vui lòng chọn một điểm dầu trước');
    return;
  }

  const getInt = (input) => parseInt(input.value) || 0;

  const updateAndSend = () => {
    const x = getInt(selectedPointInputs.X);
    const y = getInt(selectedPointInputs.Y);
    const z = getInt(selectedPointInputs.Z);
    const k = parseFloat(selectedPointInputs.K.value) || 0;

    const error = validatePoint(selectedPointIndex, x, y, z, k);
    if (error) {
      alert(error);
      return;
    }

    fetch('/api_new_model/run_point', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        x: x,
        y: y,
        z: z,
        brightness: k
      })
    })
      .then(res => res.json())
      .then(data => {
         console.log("Trạng thái:",data.message)
         console.log(`✅ Đã gửi điểm ${selectedPointIndex} đến thiết bị. Phản hồi: ${data.message}`);
      })
  };

  const action = e.target.textContent;

  if (action.includes('Tăng X')) {
    const newVal = getInt(selectedPointInputs.X) + 1;
    if (newVal >= 0 && newVal <= Limit_x) {
      selectedPointInputs.X.value = newVal;
      updateAndSend();
    } else {
      alert(`Giá trị X phải >= 0 và <= ${Limit_x}`);
    }
  } else if (action.includes('Giảm X')) {
    const newVal = getInt(selectedPointInputs.X) - 1;
    if (newVal >= 0 && newVal <= Limit_x) {
      selectedPointInputs.X.value = newVal;
      updateAndSend();
    } else {
      alert(`Giá trị X phải >= 0 và <= ${Limit_x}`);
    }
  } else if (action.includes('Tăng Y')) {
    const newVal = getInt(selectedPointInputs.Y) + 1;
    if (newVal >= 0 && newVal <= Limit_y) {
      selectedPointInputs.Y.value = newVal;
      updateAndSend();
    } else {
      alert(`Giá trị Y phải >= 0 và <= ${Limit_y}`);
    }
  } else if (action.includes('Giảm Y')) {
    const newVal = getInt(selectedPointInputs.Y) - 1;
    if (newVal >= 0 && newVal <= Limit_y) {
      selectedPointInputs.Y.value = newVal;
      updateAndSend();
    } else {
      alert(`Giá trị Y phải >= 0 và <= ${Limit_y}`);
    }
  } else if (action.includes('Tăng Z')) {
    const newVal = getInt(selectedPointInputs.Z) + 1;
    if (newVal >= 0 && newVal <= Limit_z) {
      selectedPointInputs.Z.value = newVal;
      updateAndSend();
    } else {
      alert(`Giá trị Z phải >= 0 và <=${Limit_z}`);
    }
  } else if (action.includes('Giảm Z')) {
    const newVal = getInt(selectedPointInputs.Z) - 1;
    if (newVal >= 0 && newVal <= Limit_z) {
      selectedPointInputs.Z.value = newVal;
      updateAndSend();
    } else {
      alert(`Giá trị Z phải >= 0 và <= ${Limit_z}`);
    }
  } 
  else if (action.includes('Giảm K')) {
    const newVal = getInt(selectedPointInputs.K) - 1;
    if (newVal >= 0 && newVal <= Limit_k) {
      selectedPointInputs.K.value = newVal;
      updateAndSend();
    } else {
      alert(`Giá trị K phải >= 0 và <= ${Limit_k}`);
    }
  } 
  else if (action.includes('Tăng K')) {
    const newVal = getInt(selectedPointInputs.K) + 1;
    if (newVal >= 0 && newVal <= Limit_k) {
      selectedPointInputs.K.value = newVal;
      updateAndSend();
    } else {
      alert(`Giá trị K phải >= 0 và <= ${Limit_k}`);
    }
  } 
});
        // Get product infomation  --------------------------------------------

function sendAllPoints() {
  const container = document.getElementById('pointsContainer');
  const groups = container.querySelectorAll('.point-group');

  const points = [];

  for (let group of groups) {
   const x = parseFloat(group.querySelector('input[name="point_x[]"]').value);
   const y = parseFloat(group.querySelector('input[name="point_y[]"]').value);
   const z = parseFloat(group.querySelector('input[name="point_z[]"]').value);
   const k = parseFloat(group.querySelector('input[name="point_k[]"]').value);

    points.push({ x, y, z, k });
  }

  fetch('/api_new_model/run_all_points', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ points })
  })
  .then(res => res.json())
  .then(data => {
    console.log("✅ Gửi thành công: " + data.message);
  })
  .catch(err => {
    console.error('Lỗi khi gửi điểm dầu:', err);
  });
}
//check connect --------------------------------------------
function isConect(isconect){
    const ob_status_connect = document.getElementById("header-show-status");
    const ob_cir_status_connect = document.getElementById("header-show-circle");  
    if (isconect) {
        ob_cir_status_connect.classList.remove("disconnect");
        ob_cir_status_connect.classList.add("connecting");
        ob_status_connect.innerText = "";
        ob_status_connect.innerText = "Đang kết nối";
        } else {
        ob_cir_status_connect.classList.add("disconnect");
        ob_cir_status_connect.classList.remove("connecting");
        ob_status_connect.innerText = "";
        ob_status_connect.innerText = "Mất kết nối";
    }
}
// //ham nay se bat lai sau khi hoan thien
// function fetchStatusConect() {
//     fetch('/api_new_model/get_status?param1=status_connect')
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok: ' + response.statusText);
//             }
//             return response.text(); 
//         })
//         .then(data => {
//             const statusCode = parseInt(data.trim()); 
//             console.log('Status received:', statusCode);

//             // Xử lý tùy theo giá trị trả về
//             switch (statusCode) {
//                 case 0:
//                     isConect(0);
//                     break;
//                 case 1:
//                     isConect(1);
//                     break;
//                 default:
//                     console.log('Trạng thái không xác định');
//             }
//         })
//         .catch(error => {
//             console.error('Fetch error:', error);
//         });
// }
// fetchStatusConect();
// setInterval(fetchStatusConect, 1000);
//--------------------------------------------
  function showExitModal() {
    const modal = document.getElementById('exit-modal');
    if (modal) modal.style.display = 'flex';
  }

  function hideExitModal() {
    const modal = document.getElementById('exit-modal');
    if (modal) modal.style.display = 'none';
  }

function confirmExit() {
       fetch('/api_new_model/exit-training')
      .then(response => {
          if (response.redirected) {
              // Nếu Flask redirect trực tiếp
              window.location.href = response.url;
          } else {
              // Nếu Flask trả về JSON (nếu bạn thay đổi API)
              response.json().then(data => {
                  window.location.href = data.redirect_url;
              });
          }
      });
}
