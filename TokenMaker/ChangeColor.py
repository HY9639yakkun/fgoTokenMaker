'''
色の変更
'''
from PIL import Image, ImageChops, ImageFilter, ImageOps

import FilePath

class changeToGolden():
    '''
    金色に変更
    '''
    def __init__(self, objTargetImage):
        self.objTargetImage = objTargetImage
        self.image_size = self.objTargetImage.size

    def chage_color(self):
        '''
        色変更処理
        '''
        #輪郭ははっきりさせる,グレースケールへの変更
        result = self.outlining(self.objTargetImage)
        result = self.change_to_gray(result)
        result.show()

        #金色と重ねる
        result = self.color_mask(result)
        result.show()

        #効果
        result = self.effect_mask(result)
        result.show()

        return result
    
    @staticmethod
    def outlining(im):
        #輪郭をはっきりさせる
        return im.filter(ImageFilter.MinFilter).filter(ImageFilter.EDGE_ENHANCE_MORE)

    @staticmethod
    def change_to_gray(im):
        #グレーに変更
        return im.convert('L').convert('RGB')

    def color_mask(self, base_image):
        #色を重ねる
        color_image = Image.new("RGB", self.image_size, (230, 200, 100))
        mask = Image.new("L", self.image_size, 127)
        result = Image.composite(
            base_image,
            color_image,
            mask)
        return result

    def effect_mask(self, base_image):
        #エフェクト(光沢)追加
        with Image.open(FilePath.get_gradation()) as effect_img:
            effect_img_resize = effect_img.resize(self.image_size)
        result = ImageChops.subtract(base_image,
            effect_img_resize.convert('RGB'))
        result = ImageOps.posterize(result,5)#色の単純化
        return result

if __name__ == '__main__':
    objImage = Image.open(r'C:\makeTOOL\FGO\TEST2.JPG')
    obj = changeToGolden(objImage)
    obj.chage_color()
