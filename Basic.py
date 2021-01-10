import cv2
import numpy as np
import face_recognition

# import images and convert to rgb

imageSanta = face_recognition.load_image_file('imagesExamples/Santa.jpeg')
imageSanta = cv2.cvtColor(imageSanta, cv2.COLOR_BGR2RGB)

imageSantaTest = face_recognition.load_image_file('imagesExamples/Santa2.jpg')
imageSantaTest = cv2.cvtColor(imageSantaTest, cv2.COLOR_BGR2RGB)

# identify and mark corners of face

faceLocation = face_recognition.face_locations(imageSanta)[0]
encodeSanta = face_recognition.face_encodings(imageSanta)[0]
cv2.rectangle(imageSanta,(faceLocation[3],faceLocation[0]),(faceLocation[1],faceLocation[2]), (255,0,255),2)

faceLocationTest = face_recognition.face_locations(imageSantaTest)[0]
encodeSantaTest = face_recognition.face_encodings(imageSantaTest)[0]
cv2.rectangle(imageSantaTest,(faceLocationTest[3],faceLocationTest[0]),(faceLocationTest[1],faceLocationTest[2]), (255,0,255),2)

results = face_recognition.compare_faces([encodeSanta],encodeSantaTest)

faceDistance = face_recognition.face_distance([encodeSanta],encodeSantaTest)

print(results, faceDistance)
cv2.putText(imageSantaTest,f'{results} {round(faceDistance[0],2)}', (50,50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

# display images for user

cv2.imshow('Santa Ono',imageSanta)
cv2.imshow('Santa Ono Test',imageSantaTest)
cv2.waitKey(0)