import ddddocr
import cv2


slide = ddddocr.DdddOcr(det=False, ocr=False)

# 滑块缝合的图片
with open('./verification_code_2-2.png', 'rb') as f:
    target_bytes = f.read()

# 有缺口的图片
with open('./verification_code_2-1.png', 'rb') as f:
    background_bytes = f.read()

# 滑块缝合的图片
img = cv2.imread("./verification_code_2-2.png")

res = slide.slide_comparison(target_bytes, background_bytes)

print(res)
