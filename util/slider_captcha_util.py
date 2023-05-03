from io import BytesIO
import os
import random
from PIL import Image
import base64


class SliderCaptchaUtil:
    def __init__(self):
        self.maskSize = 50
        self.bgWidth = 310
        self.bgHeight = 160
        self.maskPath = "./static/img/mask.png"
        self.bgList = "./static/img/background.png"

    def create(self):
        with open(self.bgList, "rb") as f:
            image_bytes = f.read()
        img = Image.open(BytesIO(image_bytes))
        print(img.size)
        self.bgWidth, self.bgHeight = img.size

        # 生成拼图位置坐标
        # 生成拼图左边x坐标，取值范围拼图左右边界到两侧最小距离20px
        imageRandX = random.randint(20, self.bgWidth - self.maskSize - 20)
        # 生成拼图上边y坐标，取值范围拼图上下边界到顶部或底部最小距离20px
        imageRandY = random.randint(20, self.bgHeight - self.maskSize - 20)

        # 设置截取的最大坐标值和最小坐标值
        minPotion = (imageRandX, imageRandY)
        maxPotion = (imageRandX + self.maskSize, imageRandY + self.maskSize)

        # 处理背景图像，截取拼图
        img_crop = img.crop((minPotion[0], minPotion[1], maxPotion[0], maxPotion[1]))
        img_data = self.get_base64_from_image(img_crop)

        # 处理遮罩图像
        mask_file = open(self.maskPath, "rb")
        mask_bytes = mask_file.read()
        mask_file.close()
        mask_img = Image.open(BytesIO(mask_bytes))

        # 获取遮罩图像的base64编码
        bg_data = self.get_base64_from_image_with_mask(img, mask_img, minPotion)

        return img_data, bg_data, imageRandX, imageRandY

    def get_base64_from_image(self, img):
        empty_buff = BytesIO()
        img.save(empty_buff, format="PNG")
        return base64.b64encode(empty_buff.getvalue()).decode()

    def get_base64_from_image_with_mask(self, img, mask, minPotion):
        # 将遮罩图像粘贴到背景图像上
        img.paste(mask, minPotion, mask)
        empty_buff = BytesIO()
        img.save(empty_buff, format="PNG")
        return base64.b64encode(empty_buff.getvalue()).decode()


if __name__ == "__main__":
    captcha = SliderCaptchaUtil()
    img_data, bg_data, imageRandX, imageRandY = captcha.create()
    print(img_data)
    print(bg_data)
    print(imageRandX)
    print(imageRandY)
