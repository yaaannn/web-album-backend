import random

from PIL import Image, ImageDraw, ImageFont


def create_random_code(length: int = 6, abc: bool = True) -> str:
    """
    生成随机验证码
    """
    base_str = "0123456789abcdefghijklmnopqrstuvwxyz" if abc else "01234567890123456789"
    # return "".join([random.choice(base_str) for _ in range(length)])
    return "".join(random.choices(list(base_str), k=length))


def create_code_image(code: str, width: int = 100, height: int = 45) -> Image:
    """
    生成验证码图片
    """
    image = Image.new("RGB", (width, height), (255, 255, 255))
    font = ImageFont.truetype(font="static/font/SmileySans-Oblique.ttf", size=25)
    draw = ImageDraw.Draw(image)
    for i in range(4):
        draw.text((5 + i * 25, 5), code[i], (0, 0, 0), font)
    for i in range(100):
        draw.point(
            (random.randint(0, width), random.randint(0, height)), fill=(0, 0, 0)
        )
    return image


if __name__ == "__main__":
    code = create_random_code(4, True)
    image = create_code_image(code)
    image.save("code.png")
