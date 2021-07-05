##160，160，400，400
from PIL import Image
from PIL import ImageDraw
img = Image.new('RGB', (512, 512), (255, 255, 255))
# img.show()
# img.save('test.png')

a = ImageDraw.ImageDraw(img)  # 用a来表示右侧这段

a.rectangle((160, 160, 400, 400), fill='black', outline='black', width=0)  # 在100，1
img.show()
img.save('test.png')
