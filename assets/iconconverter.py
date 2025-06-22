from PIL import Image

img = Image.open("pme_icon.png")  # アップロードしてくれたPNGを指定
img.save("pme.ico", format="ICO", sizes=[
    (16, 16), (32, 32), (48, 48),
    (64, 64), (128, 128), (256, 256)
])