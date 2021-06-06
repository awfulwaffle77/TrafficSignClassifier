from PIL import Image

img = Image.open("flower1")
rgb = img.convert("RGB")
rgb.save("flower.jpg")
print(img)