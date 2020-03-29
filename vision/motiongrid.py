from vision.boundingbox import BoundingBox
import functools


class MotionCheckResult:

    def __init__(self, motion_results):
        if len(motion_results) != 3:
            raise ValueError(f"Motion result must have 3 rows")

        for row in motion_results:
            if len(row) != 3:
                raise ValueError(f"All motion result rows must have 3 values")

        self.motion_results = motion_results


    def motion_on_left(self):
        return self.motion_in_column(0)


    def motion_on_right(self):
        return self.motion_in_column(2)


    def motion_in_middle(self):
        return self.motion_in_column(1)
        

    def motion_in_column(self, column_index):
        for row in self.motion_results:
            if row[column_index]:
                return True

        return False


    def motion_everywhere(self):
        for row in self.motion_results:
            for cell in row:
                if not cell:
                    return False

        return True


    def has_motion(self):
        for row in self.motion_results:
            for cell in row:
                if cell:
                    return True

        return False

        
    def __str__(self):
        result = ""
        for row in self.motion_results:
            for cell in row:
                result += "X " if cell else "0 "
            result += "\n"

        return result  


class MotionDetectionGrid:

    def __init__(self, image_dimensions):
        self.GRID_SIZE = 3
        if image_dimensions[0] < self.GRID_SIZE * 2 or image_dimensions[1] < self.GRID_SIZE * 2:
            raise ValueError(f"Grid dimensions must exceed {self.GRID_SIZE * 2}")

        column_size = image_dimensions[0] / self.GRID_SIZE
        row_size = image_dimensions[1] / self.GRID_SIZE
        self.grid = [[ self._build_cell(row_size, column_size, row, col) for col in range(self.GRID_SIZE)] for row in range(self.GRID_SIZE)] 
        

    def _build_cell(self, row_size, column_size, row, column): 
        x_min = column_size * column
        y_min = row_size * row
        x_max = column_size * (column + 1)
        y_max = row_size * (row + 1)
        return _MotionDetectionCell(BoundingBox(x_min, y_min, x_max, y_max))

    
    def check_motion(self, motion_bounding_boxes):
        motion_results = [ [ cell.has_motion(motion_bounding_boxes) for cell in row ] for row in self.grid]
        #motion_results = [map(lambda cell : cell.has_motion(motion_bounding_boxes), row) for row in self.grid]
        return MotionCheckResult(motion_results)


class _MotionDetectionCell:

    def __init__(self, bounding_box):
        self.bounding_box = bounding_box


    def has_motion(self, motion_bounds):
        for motion_bound in motion_bounds:
            if not self.bounding_box.intersection(motion_bound).empty():
                return True
            
        return False  
            

if __name__ == '__main__':

    test2d = [["1","2","3"], ["4","5","6"], ["7", "8", "9"]]

    results = [list(map(lambda c : c * 10, row)) for row in test2d]
    print(results)

    results = [ [ cell * 10 for cell in row ] for row in test2d]
    print(results)


    grid = MotionDetectionGrid((600, 300))
    bounds = [BoundingBox(0, 10, 10, 20), BoundingBox(300, 100, 450, 250)]
    checkResult = grid.check_motion(bounds)
    print(checkResult)

    checkResult = MotionCheckResult([[True, False, False], [False, True, False], [False, False, True]])

    print(checkResult.motion_on_left())
    print(checkResult.motion_in_middle())
    print(checkResult.motion_on_right())

    checkResult = MotionCheckResult([[False, False, False], [False, True, False], [False, False, False]])

    print(checkResult.motion_on_left())
    print(checkResult.motion_in_middle())
    print(checkResult.motion_on_right())

    checkResult = MotionCheckResult([[False, False, True], [False, False, False], [True, False, False]])

    print(checkResult.motion_on_left())
    print(checkResult.motion_in_middle())
    print(checkResult.motion_on_right())