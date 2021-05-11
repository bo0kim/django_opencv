from django.conf import settings
import numpy as np
import cv2


def cv_detect_face(path): # path parameter를 통해 파일 경로를 받아들이게 됩니다.
   img = cv2.imread(path, 1)
   if (type(img) is np.ndarray):
       print(img.shape) # 세로, 가로, 채널

       resize_needed = False
       if img.shape[1] > 640: # ex) 가로(img.shape[1])가 1280일 경우,
           resize_needed = True
           new_w = img.shape[1] * (640.0 / img.shape[1]) # 1280 * (640/1280) = 1280 * 0.5
           new_h = img.shape[0] * (640.0 / img.shape[1]) # 기존 세로 * (640/1280) = 기존 세로 * 0.5
       elif img.shape[0] > 480: # ex) 세로(img.shape[0])가 960일 경우,
           resize_needed = True
           new_w = img.shape[1] * (480.0 / img.shape[0]) # 기존 가로 * (480/960) = 기존 가로 * 0.5
           new_h = img.shape[0] * (480.0 / img.shape[0]) # 960 * (480/960) = 960 * 0.5
       if resize_needed == True:
           img = cv2.resize(img, (int(new_w), int(new_h)))

       # Haar-based Cascade Classifier : AdaBoost 기반 머신러닝 물체 인식 모델
       # 이미지에서 눈, 얼굴 등의 부위를 찾는데 주로 이용
       # 이미 학습된 모델을 OpenCV 에서 제공 (http://j.mp/2qIxrxX)
       baseUrl = settings.MEDIA_ROOT_URL + settings.MEDIA_URL
       face_cascade = cv2.CascadeClassifier(baseUrl+'haarcascade_frontalface_default.xml')
       eye_cascade = cv2.CascadeClassifier(baseUrl+'haarcascade_eye.xml')
       gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# detectMultiScale(Original img, ScaleFactor, minNeighbor) : further info. @ http://j.mp/2SxjtKR
       faces = face_cascade.detectMultiScale(gray, 1.3, 5)
       for (x, y, w, h) in faces:
           cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
           roi_gray = gray[y:y+h, x:x+w]
           roi_color = img[y:y+h, x:x+w]
           eyes = eye_cascade.detectMultiScale(roi_gray)
           for (ex, ey, ew, eh) in eyes:
               cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
       cv2.imwrite(path, img)
   else:
       print('Error occurred within cv_detect_face!')
       print(path)
