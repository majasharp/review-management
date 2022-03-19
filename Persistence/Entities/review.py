from operator import length_hint


class Review:
    def __init__(self, length):
        self.length = length

    def get_length(self):
        return self.length

    def set_length(self, length):
        self.length = length
    
    def get_area(self):
        return self.length * self.length
    
    def get_perimeter(self):
        return self.length * 4

    