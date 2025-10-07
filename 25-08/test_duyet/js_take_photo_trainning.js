        const deviceList = document.getElementById('deviceList');
        const deviceForm = document.getElementById('deviceForm');
        const pointsContainer = document.getElementById('pointsContainer');
    
        let pointIndex = 0;
        const summaryData = [];
            function addPoint() {    
            const html = `
                <p id="decsciption_${pointIndex}">Điểm dầu thứ ${pointIndex + 1} </p>
                <div class="row g-1 point-row align-items-center" data-index="${pointIndex}">
                <div id="x${pointIndex}" class="col-2"><input type="number" class="form-control" name="x_${pointIndex}" placeholder="X" min = 0 max = 110 required></div>
                <div id="y${pointIndex}" class="col-2"><input type="number" class="form-control" name="y_${pointIndex}" placeholder="Y" min = 0 max = 75 required></div>
                <div id="z${pointIndex}" class="col-2"><input type="number" class="form-control" name="z_${pointIndex}" placeholder="Z" min = 0 max = 12 required></div>
                <div id="brightness${pointIndex}" class="col-2"><input type="number" class="form-control" name="brightness_${pointIndex}" placeholder="Ánh sáng" min = 0 max = 100  required></div>
                <div class="col-4 d-flex gap-1">
                        <button type="button" class="btn btn-success btn-sm" onclick="runPoint(${pointIndex})">▶️ Chạy</button>
                        <button type="button" class="btn btn-success btn-sm" onclick="select(${pointIndex})">✅ Select</button>
                        <button type="button" class="btn btn-success btn-sm" onclick="savePoint(${pointIndex})">🎨 Save</button>
                        <button type="button" class="btn btn-danger btn-sm" onclick="removePoint(${pointIndex})">❌</button>
                </div>
                </div>`;
            pointsContainer.insertAdjacentHTML('beforeend', html); // cau lenh dung de them phan tu o duiu phan tu chi dinh o day phan tu chi dinh la pointsContainer
            pointIndex++;
        }
function savePoint(index) {
    const row = document.querySelector(`.point-row[data-index="${index}"]`);
    if (!row) return;

    const xInput = row.querySelector(`[name="x_${index}"]`);
    const yInput = row.querySelector(`[name="y_${index}"]`);
    const zInput = row.querySelector(`[name="z_${index}"]`);
    const brightnessInput = row.querySelector(`[name="brightness_${index}"]`);

    // Kiểm tra dữ liệu có rỗng không
    if (
        !xInput.value.trim() ||
        !yInput.value.trim() ||
        !zInput.value.trim()
    ) {
        alert(`❌ Vui lòng nhập đầy đủ X, Y, Z cho điểm dầu thứ ${index + 1}!`);
        return;
    }

    // (Tuỳ chọn) kiểm tra brightness nếu cần
    if (!brightnessInput.value.trim()) {
        alert(`❌ Vui lòng nhập độ sáng (brightness) cho điểm dầu thứ ${index + 1}!`);
        return;
    }

    // Nếu hợp lệ, khóa các input lại
    xInput.readOnly = true;
    yInput.readOnly = true;
    zInput.readOnly = true;
    brightnessInput.readOnly = true;

    // Disable các nút (Chạy, Lưu)
    const buttons = row.querySelectorAll("button");
    buttons.forEach(btn => btn.disabled = true);

    // Đổi màu dòng đã lưu
    row.style.backgroundColor = "#e8f5e9";  // Màu xanh nhạt

    // Thông báo
    alert(`💾 Điểm dầu ${index + 1} đã được khóa và lưu.`);
}
        function removePoint(index) {      // ham nay duoc goi khi xoa 
            const el = document.querySelector(`.point-row[data-index="${index}"]`);
            const id_decsciption = document.getElementById(`decsciption_${index}`);
            if(el || id_decsciption){
                el.remove();
                id_decsciption.remove();
            }
            pointIndex--;
        }

     function runPoint(index) {
    const row = document.querySelector(`.point-row[data-index="${index}"]`);
    if (!row) return;

    const paddingx = document.getElementById("Padding_x");
    const paddingy = document.getElementById("Padding_y");
    const paddingz = document.getElementById("Padding_z");

    // Gán mặc định nếu để trống
    if (!paddingx.value || !paddingy.value || !paddingz.value) {
        paddingx.value = 1;
        paddingy.value = 1;
        paddingz.value = 1;
    }

    // Kiểm tra padding
    if (Number(paddingx.value) > 5 || Number(paddingy.value) > 5 || Number(paddingz.value) > 5) {
        alert("❌ Gía trị padding phải nhỏ hơn hoặc bằng 5.");
        return;
    }

    const xInput = row.querySelector(`[name="x_${index}"]`);
    const yInput = row.querySelector(`[name="y_${index}"]`);
    const zInput = row.querySelector(`[name="z_${index}"]`);
    const brightnessInput = row.querySelector(`[name="brightness_${index}"]`);

    // Kiểm tra rỗng
    if (!xInput.value || !yInput.value || !zInput.value || !brightnessInput.value) {
        alert(`❌ Điểm dầu ${index + 1}: Bạn chưa nhập đủ giá trị!`);
        return;
    }

    const x = parseFloat(xInput.value);
    const y = parseFloat(yInput.value);
    const z = parseFloat(zInput.value);
    const brightness = parseFloat(brightnessInput.value);

    // Kiểm tra giới hạn
    if (x > 110) {
        alert(`❌ Điểm dầu ${index + 1}: Gía trị X phải nhỏ hơn hoặc bằng 110`);
        return;
    }
    if (y > 75) {
        alert(`❌ Điểm dầu ${index + 1}: Gía trị Y phải nhỏ hơn hoặc bằng 75`);
        return;
    }
    if (z > 12) {
        alert(`❌ Điểm dầu ${index + 1}: Gía trị Z phải nhỏ hơn hoặc bằng 12`);
        return;
    }
    if (k > 100) {
        alert(`❌ Điểm dầu ${index + 1}: Gía trị ánh sáng phải nhỏ hơn hoặc bằng 100`);
        return;
    }

    // ✅ Gửi dữ liệu tới server
    fetch('/api/run_point', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            index: index,
            x: x,
            y: y,
            z: z,
            brightness: brightness
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(`✅ Đã gửi điểm ${index + 1} đến thiết bị. Phản hồi: ${data.message}`);
    })
    .catch(error => {
        console.error('Lỗi khi gửi điểm:', error);
        alert('❌ Gửi dữ liệu thất bại.');
    });
}


 deviceForm.addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData(deviceForm);
    const deviceId = formData.get("deviceId");
    const deviceName = formData.get("deviceName");

    if (isNaN(Number(deviceId))) {
        alert("❌ ID thiết bị phải là số, không được là chữ!");
        deviceForm.reset(); 
        return;
    }

    const points = [];
    for (let i = 0; i < pointIndex; i++) {
        // Nếu có dữ liệu thì mới thêm
        if (formData.get(`x_${i}`) !== null) {
            points.push({
                x: parseFloat(formData.get(`x_${i}`)),
                y: parseFloat(formData.get(`y_${i}`)),
                z: parseFloat(formData.get(`z_${i}`)),
                brightness: parseFloat(formData.get(`brightness_${i}`))
            });
        }
    }

    const deviceObj = {
        type_id: deviceId,
        type_name: deviceName,
        point_count: points.length,
        points: points
    };

    const li = document.createElement("li");
    li.className = "list-group-item";

    let content = `<strong>📦 ${deviceId} - ${deviceName} (${points.length} điểm):</strong><ul>`;
    points.forEach((point, idx) => {
        content += `<li>🔹 Điểm ${idx + 1}: X=${point.x}, Y=${point.y}, Z=${point.z}, Sáng=${point.brightness}</li>`;
   
    });
    content += `</ul>`;

    li.innerHTML = content;
    deviceList.appendChild(li);

    summaryData.push(deviceObj);

    deviceForm.reset();
    pointsContainer.innerHTML = '';
    pointIndex = 0;
    
    alert(`✅ Thiết bị "${deviceName}" (ID: ${deviceId}) đã được lưu với ${points.length} điểm.`);
});

             


        // check connect --------------------------------------------
        function fetchStatusConect() {
        fetch('/api/get_status?param1=status_connect')
            .then(response => response.json())
            .then(data => {
            console.log(data);
            if(data == '1'){isConect(1)}
            else if(data == '0'){isConect(0)}
            })
            .catch(error => {
            console.log(data);
            });
        }
        fetchStatusConect();
        setInterval(fetchStatusConect, 2000);
        // Get product infomation  --------------------------------------------
        function fetch_inf() {
            fetch('/api/get_inf_manage_product?param1=data_manage_product')
                .then(response => response.json())
                .then(data => {
                const textarea = document.getElementById('infoBox');
        let output = "";

        for (const key in data) {
        const type = data[key];
        output += `🔹 ID Loại: ${type.type_id}\n`;
        output += `📦 Tên loại: ${type.type_name}\n`;
        output += `📌 Số điểm kiểm tra: ${type.point_check.length}\n`;

        type.point_check.forEach((point, idx) => {
            output += `   ▶️ Điểm ${idx + 1}: x=${point.x}, y=${point.y}, z=${point.z}, brightness=${point.brightness}\n`;
        });

        output += '\n'; // thêm dòng trắng giữa các loại
        }

        textarea.value = output;
                })
                .catch(error => {
                console.log(data);
                });
            }
            fetch_inf();
            setInterval(fetch_inf, 2000);
        // Get log data   --------------------------------------------
        function fetch_log() {
            fetch('/api/get_log?param1=data_get_log')
                .then(response => response.json())
                .then(data => {
                console.log(data);
                })
                .catch(error => {
                console.log(data);
                });
            }
            fetch_log();
            setInterval(fetch_log, 2000);    
        //isconect------------------------------------------------------------   
        function isConect(isconect){
                const ob_status_connect = document.getElementById("status_connect");
                const ob_cir_status_connect = document.getElementById("cir_status_connect");
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
        

 
        










































