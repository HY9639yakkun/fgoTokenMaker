from PIL import Image, ImageDraw, ImageFilter
import numpy as np

def make_base_image():
    LIGHT_VALUE = 200
    DARK_VALUE = 0
    MIDDLE = 50
    image_array_row_light = np.linspace(LIGHT_VALUE, LIGHT_VALUE, 5)
    image_array_row_dark = np.linspace(DARK_VALUE, DARK_VALUE, 30)

    image_array_row1 = np.linspace(LIGHT_VALUE, MIDDLE, 400)
    image_array_row2 = np.linspace(MIDDLE, DARK_VALUE, 150)

    image_array_row3 = np.linspace(DARK_VALUE, MIDDLE, 150)
    image_array_row4 = np.linspace(MIDDLE, LIGHT_VALUE, 400)

    image_array_row = np.hstack((
        image_array_row_light,
        image_array_row1, image_array_row2,
        image_array_row_dark,
        image_array_row3, image_array_row4,
        image_array_row_light))
    return image_array_row


class GradationMaker():
    def __init__(self, image_array_row):
        self.image_array_row = image_array_row

        self.array_size = np.size(image_array_row)
        self.image_array = np.uint8(
            np.tile(self.image_array_row, (self.array_size, 1)))

    #スライド
    def slide(self):
        def get_slide_array(image_array_row):
            return lambda slide_num: np.roll(image_array_row, (slide_num+500))
        func_slide_array = get_slide_array(self.image_array_row)

        new_image_array = np.zeros((self.array_size, self.array_size))
        for i in range(self.array_size-1):
            new_image_array[:, i] = func_slide_array(i)
        self.image_array = np.uint8(new_image_array)
        self.image_array_row = self.image_array[1,:]

    #トリミング
    def trimming(self, v1, v2):
        self.image_array_row = self.image_array_row[v1:v2]
        self.image_array = self.image_array[v1:v2, v1:v2]
        self.array_size = len(self.image_array_row)
        
    def return_image_object(self):
        return Image.fromarray(self.image_array)

if __name__ == '__main__':
    obj = GradationMaker(make_base_image())
    obj.slide()
    obj.trimming(100,500)
    im = obj.return_image_object()
    im.show()
    im.save(r'C:\Users\mnkkb\Desktop\/gradation.png', quality=95)
