import ddddocr
import cv2

det = ddddocr.DdddOcr(det=True)

# 验证码图片
with open("./verification_code_3.png", 'rb') as f:
    image = f.read()

poses = det.detection(image)
print(poses)

# 验证码图片
im = cv2.imread("verification_code_3.png")

for box in poses:
    x1, y1, x2, y2 = box
    im = cv2.rectangle(im, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)


# 结果图片
cv2.imwrite("result.jpg", im)
