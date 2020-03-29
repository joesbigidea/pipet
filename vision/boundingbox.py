class BoundingBox:

    def __init__(self, x_min, y_min, x_max, y_max):
        self.bounds = (x_min, y_min, x_max, y_max)
        if self[0] > self[2] or self[1] > self[3]:
            raise ValueError(f"Invalid bounding box: {self}")


    def intersection(self, other):
        x_min = max(self[0], other[0])
        y_min = max(self[1], other[1])
        x_max = min(self[2], other[2])
        y_max = min(self[3], other[3])
        if x_min > x_max or y_min > y_max: return BoundingBox(0, 0, 0, 0)
        return BoundingBox(x_min, y_min, x_max, y_max)


    def __getitem__(self, key):
        return self.bounds[key]
    

    def empty(self):
        return self[0] >= self[2] or self[1] >= self[3]


    def __eq__(self, other):
        return self.bounds == other.bounds


    def __ne__(self, other):
        return self.bounds != other.bounds


    def __str__(self):
        return f"Rectangle: {self.bounds}"

    def __repr__(self):
        return repr(self.bounds)

