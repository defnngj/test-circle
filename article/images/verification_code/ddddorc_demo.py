import ddddocr

ocr = ddddocr.DdddOcr(old=True)

with open("./verification_code_1.png", 'rb') as f:
    image = f.read()

res = ocr.classification(image)
print(res)
