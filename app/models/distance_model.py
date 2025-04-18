
class distance_model:
    def __init__(self):
    
        self.known_distance=30
        self.real_width=15

    def cal_focal(self,box_width):
        return (box_width*self.known_distance)/self.real_width
       
    def find_distance(self,box_width):
        return (self.real_width*self.cal_focal(box_width))/box_width
    
