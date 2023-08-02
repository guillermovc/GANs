import base64
import cv2
import matplotlib.pyplot as plt
import numpy as np

img = r"C:\respaldo\Proyectos\GANs\dataset_celeb\celeba\img_align_celeba\000001.jpg"

img = plt.imread(img)

img = np.random.rand(30,30,3)

plt.imshow(img)
plt.imsave("ejemplo.jpg", img)

img_bytes = img.tobytes()
image_base64 = base64.b64encode(img_bytes)
with open("archivo_base64_decode.jpg", "wb") as file:
    file.write(image_base64)

import requests
import json


# url = "https://salsas-castillo.edesarrollos.info/proceso/imagen"

# payload = {}
# headers = {
# 'Authorization': 'Bearer KMo3-t89oOIoGzAdDvC1C5lA8NOR3G94'
# }

# response = requests.request("GET", url, headers=headers, data=payload)

# response.json()

# url = "https://salsas-castillo.edesarrollos.info/proceso/imagen"
# with open("ejemplo.jpg", "rb") as f:
#     im_bytes = f.read()  
# result = {
#     'id': 'adb139c8-d3ef-4e9c-bf49-0951669c1080',
#     "prueba_jpg64": base64.b64encode(im_bytes).decode("utf8")
# }
# payload = json.dumps(result)
# headers = {
# 'Content-Type': 'application/json',
# 'Authorization': 'Bearer KMo3-t89oOIoGzAdDvC1C5lA8NOR3G94',
# }
# response = requests.request("POST", url, headers=headers, data=payload)

# response.text