from typing import Dict,Any
import json
import os
import shutil
from pathlib import Path
class Create:

    def __init__(self,base_path: str = None):
        self.base_path = base_path
        
    def get_data_grandaugter(self,file_name:str,parent:str,grandparent:str)->Dict[str, Any]:
        """Trả về data sản phẩm hiện tại ở trong neu chua khoi tao thi se khoi tao duong dan
           Trả về rỗng nếu không có dữ liệu trong file
        """
        try: 
            current_dir = os.path.dirname(os.path.abspath(__file__))
            dir_static = os.path.join(current_dir,grandparent)
            dir_static_name_product = os.path.join(dir_static,parent)
            os.makedirs(dir_static_name_product, exist_ok=True)
            file_json = os.path.join(dir_static_name_product, file_name)
            print(f"📂 Đường dẫn JSON đầy đủ: {file_json}")
            self.path_product_list = file_json   
            if not os.path.exists(file_json):
                with open(file_json, 'w', encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False, indent=4)
                    print(f"📄 Tạo file JSON mới: {file_json}")
                    return None 
            with open(file_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.data = data
                print("✅ Đọc JSON thành công")
                return data
        except Exception as e:
            print("⚠️ File JSON rỗng hoặc sai định dạng → trả về dict rỗng")
            return {}
    def get_data_in_path(self,path:str):
         """đọc File json theo đường dẫn nếu không có trả về False nếu không có  file hoặc 
         có đường dẫn nhưng không phải file json . nếu thỏa mãn hết tất cả trả về data của đường dẫn
         """
         if path.lower().endswith(".json"):
            print("Là file Json")
         else:
             return False
         if not os.path.exists(path):
               print("Thư mục này không tồn tại")
               return False
         else :
            with open(path, 'r', encoding='utf-8') as f:
                print("Đọc File thành cônng")
                return json.load(f)

    def get_path_grandaugter(self,file_name:str,parent:str,grandparent:str)->Dict[str, Any]:
            """Giống với hàm trên nhưng trả về đường dẫn tới thu mục con
            """
            current_dir = os.path.dirname(os.path.abspath(__file__))
            dir_static = os.path.join(current_dir,grandparent)
            dir_static_name_product = os.path.join(dir_static,parent)
            os.makedirs(dir_static_name_product, exist_ok=True)
            file_json = os.path.join(dir_static_name_product, file_name)
            print(f"📂 Đường dẫn JSON đầy đủ: {file_json}")
            self.path_product_list = file_json   
            if not os.path.exists(file_json):
                with open(file_json, 'w', encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False, indent=4)
                    print(f"📄 Tạo file JSON mới: {file_json}")
            return file_json 

    def delete_folder(self,file_path):
        """
        Xóa file hoặc thư mục nếu tồn tại.
        Trả về True nếu xóa thành công, False nếu không xóa được.
        """
        if not os.path.exists(file_path):
            print(f"File/Thư mục không tồn tại: {file_path}")
            return False

        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"File đã xóa: {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f"Thư mục đã xóa: {file_path}")
            else:
                print(f"Không phải file hay thư mục: {file_path}")
                return False
            return True
        except PermissionError:
            print(f"Lỗi quyền truy cập: Không thể xóa '{file_path}'")
            return False
        except Exception as e:
            print(f"Lỗi khi xóa '{file_path}': {e}")
            return False
    def delete_file(self,file_path):
        """
        Xóa file nếu tồn tại.
        Trả về True nếu xóa thành công, False nếu thất bại.
        """
        if not os.path.exists(file_path):
            print(f"File không tồn tại: {file_path}")
            return False

        if not os.path.isfile(file_path):
            print(f"'{file_path}' không phải là file")
            return False

        try:
            os.remove(file_path)
            print(f"Đã xóa file: {file_path}")
            return True
        except PermissionError:
            print(f"Lỗi quyền truy cập: Không thể xóa '{file_path}'")
            return False
        except Exception as e:
            print(f"Lỗi khi xóa file '{file_path}': {e}")
            return False
    def find_file_in_folder(self,folder_path, filename):
        """
        Tìm file trong thư mục.
        folder_path: đường dẫn thư mục
        filename: tên file muốn tìm (exact match)
        Trả về đường dẫn đầy đủ nếu tìm thấy, None nếu không tìm thấy
        """
        if not os.path.exists(folder_path):
            print(f"Thư mục không tồn tại: {folder_path}")
            return None

        for f in os.listdir(folder_path):
            full_path = os.path.join(folder_path, f)
            if os.path.isfile(full_path) and f == filename:
                return full_path

        print(f"Không tìm thấy file '{filename}' trong '{folder_path}'")
        return None
    def create_file_in_folder(self, folder_path: str, file_name: str) -> Path | bool:
        """
        Tạo một file mới trong folder_path với tên file_name.
        - Nếu file chưa tồn tại: tạo file, trả về Path.
        - Nếu file đã tồn tại: trả về False.
        - Nếu không tạo được file: trả về false.
        """
        try:
            folder = Path(folder_path)
            folder.mkdir(parents=True, exist_ok=True)  # đảm bảo folder tồn tại

            file_path = folder / file_name
            if not file_path.exists():
                file_path.touch()  # tạo file rỗng
                print(f"Đã tạo file: {file_path}")     
                return {"return":True,"path":file_path}
            else:
                print(f"File đã tồn tại: {file_path}")
                return {"return":False,"path":file_path}
            
        except Exception as e:
            print(f"❌ Không thể tạo file: {e}")
            return False
    def create_file_in_folder_two(self,name_file: str, name_folder: str):
            """Tạo ra 1 foder nếu có rồi thì vào đó tạo ra 1 file
             trả về đường dẫn đến file nằm trong folder
            """
            current_dir = os.path.dirname(os.path.abspath(__file__))
            target_dir = os.path.join(current_dir, name_folder)
            os.makedirs(target_dir, exist_ok=True)

            file_path = os.path.join(target_dir, name_file)

            if not os.path.exists(file_path):
                print("📄 File không tồn tại, tạo mới.")
                with open(file_path, "wb") as f:   
                    print("File rỗng")
                    f.write(b"")                   
            return file_path

    def read_file_in_path(self,path):
        """
        Đọc toàn bộ nội dung file text theo đường dẫn và trả về chuỗi.
        Nếu file không tồn tại, trả về False.
        """
        import os

        if not os.path.isfile(path):
            print(f"File '{path}' không tồn tại.")
            return False

        try:
            with open(path, "r", encoding="utf-8") as f:
                noi_dung = f.read()
            return noi_dung
        except Exception as e:
            print(f"Lỗi khi đọc file: {e}")
            return False
    def get_path_same_level(self,name_find):
        """
        Tìm file 'name_find' trong cùng thư mục với file script.
        Trả về đường dẫn đầy đủ nếu tìm thấy, False nếu không tìm thấy.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        for item in os.listdir(current_dir):
            item_path = os.path.join(current_dir, item)
            if os.path.isfile(item_path) and item == name_find:
                return item_path  # trả về full path nếu tìm thấy

        return False  # không tìm thấy file
    def create_folder_peer(self,name_folder: str) -> str:
        """
        Tạo một thư mục cùng cấp với file đang chạy.
        Nếu thư mục đã tồn tại, vẫn trả về đường dẫn.
        Trả về đường dẫn tuyệt đối của thư mục.
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(script_dir, name_folder)
        
        try:
            os.makedirs(folder_path, exist_ok=True)
            print(f"✅ Thư mục đã tạo hoặc đã tồn tại: {folder_path}")
        except Exception as e:
            print(f"❌ Lỗi khi tạo folder: {e}")
            return None
        
        return folder_path   
    def create_subfolder(self,parent_path: str, child_name: str) -> str:
        """
        Tạo một thư mục con trong thư mục cha.
        Nếu đã tồn tại, không báo lỗi nhưng vẫn trả về đường dẫn.
        Trả về đường dẫn tuyệt đối của thư mục con.
        """
        # Kết hợp đường dẫn cha + con
        folder_path = os.path.join(parent_path, child_name)
        
        try:
            os.makedirs(folder_path, exist_ok=True)  # tạo nếu chưa tồn tại
        except Exception as e:
            print(f"❌ Lỗi khi tạo thư mục con: {e}")
            return None
        
        # Trả về đường dẫn tuyệt đối
        return os.path.abspath(folder_path)

    def create_folder(self,folder_path: str):
        """
        Tạo 1 folder theo đường dẫn.
        Nếu đã tồn tại thì không báo lỗi.
        """
        try:
            os.makedirs(folder_path, exist_ok=True)
            print(f"✅ Đã tạo (hoặc đã tồn tại): {folder_path}")
            return folder_path
        except Exception as e:
            print(f"❌ Lỗi khi tạo folder: {e}")
            return None
    def save_json(self,data: Dict[str, Any], filename: str) -> None:
        """
        Ghi dữ liệu vào file JSON
        :param data: dictionary cần ghi
        :param filename: tên file .json
        """
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_json(self,filename: str) -> Dict[str, Any]:
        """
        Đọc dữ liệu từ file JSON
        :param filename: tên file .json
        :return: dictionary dữ liệu đọc được
        """
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ File '{filename}' không tồn tại.")
            return {}
        except json.JSONDecodeError:
            print(f"⚠️ File '{filename}' không đúng định dạng JSON.")
            return {}
    def read_json_from_file(self, file_path: str) -> dict:
        """
        Đọc dữ liệu JSON từ file và trả về dạng dict.
        - file_path: đường dẫn tới file JSON
        """
        try:
            # Nếu file chưa tồn tại -> trả về dict rỗng
            if not os.path.exists(file_path):
                print(f"⚠️ File không tồn tại: {file_path}")
                return {}

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"✅ Đã đọc JSON từ: {file_path}")
                return data

        except json.JSONDecodeError as e:
            print(f"❌ Lỗi định dạng JSON ({file_path}): {e}")
            return {}
        except Exception as e:
            print(f"❌ Lỗi khi đọc file JSON: {e}")
            return {}
    def write_data_to_file(self, file_path: str, data: bytes, mode: str = "ab"):
        """
        Ghi dữ liệu vào file.
        - file_path: đường dẫn đến file
        - data: dữ liệu cần ghi (bytes hoặc string)
        - mode: chế độ ghi ('ab' = append binary, 'wb' = ghi đè binary)
        """
        try:
            # Đảm bảo thư mục tồn tại
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Nếu là string thì encode sang bytes
            if isinstance(data, str):
                data = data.encode("utf-8")

            with open(file_path, mode) as f:
                f.write(data)
                print(f"✅ Đã ghi {len(data)} byte vào: {file_path}")

        except Exception as e:
            print(f"❌ Lỗi khi ghi file: {e}")
    def write_json_to_file(self, file_path: str, data: dict, indent: int = 4):
        """
        Ghi dữ liệu dạng JSON vào file.
        - file_path: đường dẫn tới file json
        - data: dict hoặc list cần lưu
        - indent: số khoảng trắng khi format cho dễ đọc
        """
        try:
            # Đảm bảo thư mục tồn tại
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=indent)
                print(f"✅ Đã ghi JSON vào: {file_path}")

        except Exception as e:
            print(f"❌ Lỗi khi ghi file JSON: {e}")
    def get_or_create_json(self, name_file: str, name_folder: str) -> str:
        """
        Kiểm tra nếu file JSON đã tồn tại thì trả về đường dẫn.
        Nếu chưa có: tạo folder, tạo file và ghi {} rỗng.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        target_dir  = os.path.join(current_dir, name_folder)
        os.makedirs(target_dir, exist_ok=True)  # đảm bảo folder tồn tại

        file_path = os.path.join(target_dir, name_file)

        if not os.path.exists(file_path):
            print(f"📂 Chưa có file, tạo mới: {file_path}")
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump({}, f, ensure_ascii=False, indent=4)
                print("✅ Đã tạo file JSON rỗng {}")
            except Exception as e:
                print("❌ Lỗi khi tạo file JSON:", e)
        else:
            print(f"✅ File đã tồn tại: {file_path}")

        return file_path