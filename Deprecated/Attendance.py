import cv2
import numpy as np
import face_recognition
import os

# retrieve images from ImagesAttendance folder
path = '../ImagesAttendance'
images = []
classNames = []
presentStudents = os.listdir(path)

# retrieves names of students present from retrieved files
for student in presentStudents:
    currentImage = cv2.imread(f'{path}/{student}')
    images.append(currentImage)
    classNames.append(os.path.splitext(student)[0])
print(classNames)

# Encodes list of all images
def findEncodings(images):
    encodedStudentList = []
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encodedImage = face_recognition.face_encodings(image)[0]
        encodedStudentList.append(encodedImage)
    return encodedStudentList

encodeListKnown = findEncodings(images)
print('Encoding finished')

cap = cv2.VideoCapture(0)

while True:
    success, image = cap.read()
    imageReducedSize = cv2.resize(image,(0,0), None, 0.25, 0.25)
    imageReducedSize = cv2.cvtColor(imageReducedSize, cv2.COLOR_BGR2RGB)

    facesInCurrentFrame = face_recognition.face_locations(imageReducedSize)
    encodedCurrentFrame = face_recognition.face_encodings(imageReducedSize, facesInCurrentFrame)

    for encodedFace, faceLocation in zip(encodedCurrentFrame, facesInCurrentFrame):
        correctMatches = face_recognition.compare_faces(encodeListKnown, encodedFace)
        faceDistance = face_recognition.face_distance(encodeListKnown, encodedFace)
        print(faceDistance)
        matchIndex = np.argmin(faceDistance)

        if correctMatches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)

    cv2.imshow('Webcam', image)
    cv2.waitKey(1)

# # identify and mark corners of face
#
# faceLocation = face_recognition.face_locations(imageSanta)[0]
# encodeSanta = face_recognition.face_encodings(imageSanta)[0]
# cv2.rectangle(imageSanta,(faceLocation[3],faceLocation[0]),(faceLocation[1],faceLocation[2]), (255,0,255),2)
#
# faceLocationTest = face_recognition.face_locations(imageSantaTest)[0]
# encodeSantaTest = face_recognition.face_encodings(imageSantaTest)[0]
# cv2.rectangle(imageSantaTest,(faceLocationTest[3],faceLocationTest[0]),(faceLocationTest[1],faceLocationTest[2]), (255,0,255),2)
#
# results = face_recognition.compare_faces([encodeSanta],encodeSantaTest)
#
# faceDistance = face_recognition.face_distance([encodeSanta],encodeSantaTest)