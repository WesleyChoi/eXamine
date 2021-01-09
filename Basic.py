import cv2
import numpy
import face_recognition

imageSanta = face_recognition.load_image_file('imagesExamples/Santa.jpeg')
imageSanta = cv2.cvtColor(imageSanta, cv2.COLOR_BGR2RGB)

imageTestSanta = face_recognition.load_image_file('imagesExamples/Santa2.jpg')
imageTestSanta = cv2.cvtColor(imageTestSanta, cv2.COLOR_BGR2RGB)

cv2.imshow('Santa Ono',imageSanta)
cv2.imshow('Santa Ono Test',imageTestSanta)
cv2.waitKey(0)