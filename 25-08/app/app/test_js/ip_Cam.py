# import psutil
# import socket

# def list_all_ipv4():
#     addrs = psutil.net_if_addrs()
#     result = {}
    
#     for iface_name, iface_addrs in addrs.items():
#         ipv4_list = []
#         for addr in iface_addrs:
#             if addr.family == socket.AF_INET:
#                 ip = addr.address
#                 if ip != "127.0.0.1":  # loại bỏ loopback
#                     ipv4_list.append(ip)
#         if ipv4_list:
#             result[iface_name] = ipv4_list
#     return result

# if __name__ == "__main__":
#     ipv4s = list_all_ipv4()
#     if not ipv4s:
#         print("Không tìm thấy IP nào (ngoại trừ loopback).")
#     else:
#         print("Danh sách IP LAN đang kết nối:")
#         for iface, ips in ipv4s.items():
#             print(f"{iface}: {', '.join(ips)}")

import subprocess

def set_static_ip(interface_name, ip_address, subnet_mask="255.255.255.0", gateway=None):
    """
    Thay đổi IP tĩnh cho interface trên Windows
    interface_name: tên interface như 'Ethernet 4'
    ip_address: IP tĩnh muốn đặt, ví dụ '192.168.100.2'
    subnet_mask: subnet mask, mặc định '255.255.255.0'
    gateway: nếu có, ví dụ '192.168.100.1', mặc định None
    """
    try:
        # Thay đổi IP tĩnh
        cmd = f'netsh interface ip set address name="{interface_name}" static {ip_address} {subnet_mask}'
        if gateway:
            cmd += f' {gateway} 1'
        subprocess.run(cmd, shell=True, check=True)
        print(f"Đã đặt IP {ip_address} cho {interface_name}")
    except subprocess.CalledProcessError as e:
        print("Lỗi khi đặt IP:", e)

# Ví dụ sử dụng:
if __name__ == "__main__":
    set_static_ip("Ethernet 4", "192.168.100.2", "255.255.255.0", "192.168.100.1")
