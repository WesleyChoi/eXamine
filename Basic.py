import cv2
import numpy
import face_recognition

imageSanta = face_recognition.load_image_file('imagesExamples/Santa.jpeg')
imageSanta = cv2.cvtColor(imageSanta, cv2.COLOR_BGR2RGB)

imageTestSanta = face_recognition.load_image_file('imagesExamples/Santa2.jpg')
imageTestSanta = cv2.cvtColor(imageTestSanta, cv2.COLOR_BGR2RGB)

faceLocation = face_recognition.face_locations(imageSanta)[0]
encodeSanta = face_recognition.face_encodings(imageSanta)[0]
cv2.rectangle(imageSanta,(faceLocation[3],faceLocation[0]),(faceLocation[1],faceLocation[2]), (255,0,255),2)

cv2.imshow('Santa Ono',imageSanta)
cv2.imshow('Santa Ono Test',imageTestSanta)
cv2.waitKey(0)