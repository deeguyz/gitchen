import cv2 
import numpy
from clarifai import rest
from clarifai.rest import ClarifaiApp
import json
import base64

app = ClarifaiApp("QhN2u5hmNHNCDvEvae-EfCzVmX9V-Fb8aoZylGl3", "PEQwDG5VhLFpnH_sQfYS3XCm2xMkwfK4QYtroxqH")
model = app.models.get("food-items-v1.0")

FILTERS = ["vegetable", "fruit", "vegetables", "fruits", "citrus", "alcohol", "sweet",
		   "sour", "tart", "dairy product", "bread", "meat", "oil", "juice", "dough",
		   "salad", "fat", "chocolate", "pasture"]

def detect_labels(file_str):
	labels = []
	# return ['apple']
	b = numpy.fromstring(file_str, numpy.uint8)
	image = cv2.imdecode(b, cv2.IMREAD_COLOR)

	edged = cv2.Canny(image, 10, 250)
	_, cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	idx = 0
	for c in cnts:
		x,y,w,h = cv2.boundingRect(c)
		if w>100 and h>100:
			idx+=1
			dim = max(w, h)
			new_img=image[y:y+dim,x:x+dim]
			filename = "crops/" + str(idx) + '.jpg'
			cv2.imwrite(filename, new_img)
			labels.extend(detect_labels_from_img(filename))
	return list(set(labels))

def detect_labels_from_img(img):

    payload = model.predict_by_filename(img)
    outputs = payload.get("outputs")
    if outputs is None:
    	return []
    else:
    	data = outputs[0]["data"]
    	return [item["name"] for item in data["concepts"] if item["value"] > 0.95 and item["name"] not in FILTERS]


# crop_image(open("fridge.jpg", "r").read())
# print detect_labels_from_img("crops/8.jpg")

# cv2.imshow("im",image)
# cv2.waitKey(0)