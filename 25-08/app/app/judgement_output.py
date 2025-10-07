class Judgement_Output:
    def __init__(self):
        #lớp này không phán xét oke hay NG mà là để lưu dữ liệu 
        self.number_of_detection_point_frame = None    #số điểm phát hiện 
        self.number_of_points_within_the_frame = None   # số điểm nằm trong
        self.number_of_points_outside_the_frame = None  # số điểm nằm ngoài
        self.number_of_points_on_the_frame = None       # số điểm nằm trên
    
    # Getter & Setter cho number_of_detection_point_frame
    def get_number_of_detection_point_frame(self):
        return self._number_of_detection_point_frame

    def set_number_of_detection_point_frame(self, value):
        self._number_of_detection_point_frame = value

    # Getter & Setter cho number_of_points_within_the_frame
    def get_number_of_points_within_the_frame(self):
        return self._number_of_points_within_the_frame

    def set_number_of_points_within_the_frame(self, value):
        self._number_of_points_within_the_frame = value

    # Getter & Setter cho number_of_points_outside_the_frame
    def get_number_of_points_outside_the_frame(self):
        return self._number_of_points_outside_the_frame

    def set_number_of_points_outside_the_frame(self, value):
        self._number_of_points_outside_the_frame = value

    # Getter & Setter cho number_of_points_on_the_frame
    def get_number_of_points_on_the_frame(self):
        return self._number_of_points_on_the_frame

    def set_number_of_points_on_the_frame(self, value):
        self._number_of_points_on_the_frame = value

class JudgementManager:
    def __init__(self):
        self._outputs = []  # danh sách các Judgement_Output

    def add_output(self, output: Judgement_Output):
        """Thêm một đối tượng Judgement_Output vào danh sách"""
        self._outputs.append(output)

    def get_all_outputs(self):
        """Trả về toàn bộ danh sách outputs"""
        return self._outputs

    def get_summary(self):
        """Tính tổng hợp dữ liệu từ tất cả outputs"""
        summary = {
            "total_detection_points": 0,
            "total_within_frame": 0,
            "total_outside_frame": 0,
            "total_on_frame": 0,
        }
        for o in self._outputs:
            summary["total_detection_points"] += o.get_number_of_detection_point_frame() or 0
            summary["total_within_frame"] += o.get_number_of_points_within_the_frame() or 0
            summary["total_outside_frame"] += o.get_number_of_points_outside_the_frame() or 0
            summary["total_on_frame"] += o.get_number_of_points_on_the_frame() or 0
        return summary