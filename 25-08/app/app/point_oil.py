class PointOil:
    def __init__(self, x, y, z, brightness):
        self.x = x
        self.y = y
        self.z = z
        self.brightness = brightness

    def __str__(self):
        return f"(X={self.x}, Y={self.y}, Z={self.z}, Brightness={self.brightness})"
    def dict_point_oil(self):
        return { "x": self.x,
            "y": self.y,
            "z": self.z,
            "brightness": self.brightness,  
        }
    def show(self):
        print(f"Tọa độ dầu: {self}")
    # --- Getter ---
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_z(self):
        return self.z
    
    def get_brightness(self):
        return self.brightness

    # --- Setter ---
    def set_x(self, value: int):
        self.x = value

    def set_y(self, value: int):
        self.y = value

    def set_z(self, value: int):
        self.z = value

    def set_brightness(self, value: int):
        self.brightness = value