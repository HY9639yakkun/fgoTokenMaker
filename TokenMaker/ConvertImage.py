'''
画像の取得
'''
from PIL import Image, ImageDraw, ImageFilter

import FilePath

CIRCLE_SIZE = (130,133)
CIRCLE_POSITION = (22, 20, 152, 143)

# ######################################################################
def excute(filePath):
    # 変換対象の画像を取得
    with ImageGetter(filePath) as objImageGetter:
        objSquareImage = objImageGetter.get_square_image()

    # 取得した画像を縮小
    print('リサイズ...')
    objResizeImage = objSquareImage.resize(CIRCLE_SIZE)
    objResizeImage.show()

    with ImageGenerater(objResizeImage) as objImageGenerater:
        result = objImageGenerater.combine_images()

    return result

# ######################################################################
class ImageGenerater():
    '''
    画像の編集、作成
    '''

    def __init__(self, objTargetImage):
        #合成する画像
        self.objTargetImage = objTargetImage
        self.objMaskImage = None
        self.objFrameImage = None
        self.objMargin = None

    def __enter__(self):
        self.open_images()
        return self

    def __exit__(self, ex_typr, wx_value, trace):
        self.close_images

    def open_images(self):
        self.objFrameImage = Image.open(FilePath.get_frame())
        self.objMaskImage = self.make_mask()
        self.objMargin = Image.new('RGB', 
            self.objFrameImage.size,
            (0, 0, 0))

    def close_images(self):
        self.objMaskImage.close()
        self.objFrameImage.close()
        self.objMargin.close()

    def make_mask(self):
        result = Image.new("L", self.objFrameImage.size, 0)
        draw = ImageDraw.Draw(result)
        draw.ellipse(CIRCLE_POSITION, fill=255)
        return result

    def combine_images(self):
        '''合成'''

        print('位置調整...')
        objEditedTargetImage = self.positioning()
        objEditedTargetImage.show()

        #合成
        print('合成開始...')
        result = Image.composite(
            objEditedTargetImage,
            self.objFrameImage,
            self.objMaskImage)

        objEditedTargetImage.close()
        return result

    def positioning(self):
        result = self.objMargin.copy()
        paste_positin = (
            cal_paste_position(self.objMargin.width,
                               self.objTargetImage.width),
            cal_paste_position(self.objMargin.height,
                               self.objTargetImage.height)
        )
        result.paste(self.objTargetImage, paste_positin)
        return result

def cal_paste_position(outside, inside):
    return int((outside - inside) / 2)

# ######################################################################
class ImageGetter():
    '''
    画像からの情報取得
    '''
    def __init__(self, filePath):
        self.filePath = filePath
        self.objImage = None

    def __enter__(self):
        print('画像読み取り...')
        self.objImage = Image.open(self.filePath)
        self.objImage.show()
        return self

    def __exit__(self, ex_typr, wx_value, trace):
        self.objImage.close()
        
    def get_square_image(self):
        square_Image = self.objImage.crop(make_square_size(
            self.get_width()  ,
            self.get_height()))
        return square_Image

    def get_height(self):
        return self.objImage.height

    def get_width(self):
        return self.objImage.width

def make_square_size(width, height):
    one_side_of_a_square = min(height, width)
    one_side_of_a_square_devide = one_side_of_a_square/2
    left  = width/2  - one_side_of_a_square_devide
    right = width/2  + one_side_of_a_square_devide
    upper = height/2 - one_side_of_a_square_devide
    lower = height/2 + one_side_of_a_square_devide
    return (left, upper, right, lower)

# ######################################################################
if __name__ == '__main__':
    print('PNGで動作確認 *****************************')
    im = excute(r'C:\makeTOOL\FGO\TEST.PNG')
    im.show()

    print('JPGで動作確認 *****************************')
    im = excute(r'C:\makeTOOL\FGO\TEST2.JPG')
    im.show()
    print(1)
