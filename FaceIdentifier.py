import cv2
import numpy as np
import face_recognition
import os
from RecognizeFaces import SIDRecognize, ZoomRecognize

class FaceIdentifier(object):
    def __init__(self, studentImagesPath, screenshotImagesPath):
        self.studentImagesPath = studentImagesPath
        self.screenshotImagesPath = screenshotImagesPath
        self.images = []
        self.studentNames = []
        self.presentStudents = os.listdir(self.studentImagesPath)

        self.retrieve_names()
        #self.upload_screenshots()

    def retrieve_names(self):
        for student in self.presentStudents:
            currentImage = cv2.imread(f'{self.studentImagesPath}/{student}')
            self.images.append(currentImage)
            self.studentNames.append(os.path.splitext(student)[0])
        print('Students in class:' + str(self.studentNames))

    # TODO: unfinished
    def upload_screenshots(self):
        # In the console, make sure the user includes the file type
        # Also have some return in the UI if the user does not type an existing file
        print('What is the name of your screenshot image file? Type \'Done\' if you are done.')
        response = str(input())

        while response != 'Done':
            imageToConvert = self.screenshotImagesPath + '/' + response

            try:
                classImage = face_recognition.load_image_file(imageToConvert)
            except IOError:
                print('File location was not valid. ' +
                      'Make sure that your file was typed correctly, including the file extension.')

            print('What is the name of your screenshot image file? Type \'Done\' if you are done.')
            response = str(input())

    def recognize_faces(self):
        students = SIDRecognize(self.studentImagesPath)
        zoomScreenshots = ZoomRecognize(self.screenshotImagesPath)
        students.encode()
        zoomScreenshots.recognize(students)

if __name__ == "__main__":
    faceIdentifier = FaceIdentifier('ImagesAttendance', 'ClassScreenshot')
    faceIdentifier.recognize_faces()
"""
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

# changed cap
# retrieve images from ImagesAttendance folder

# In the console, make sure the user includes the file type
# Also have some return in the UI if the user does not type an existing file
print('What is the name of your screenshot image file?')
imageToConvert = 'ClassScreenshot/'
imageToConvert += str(input())

try:
    classImage = face_recognition.load_image_file(imageToConvert)
except IOError:
    print('File location was not valid. Make sure that your file was type correctly, including the file type.')

classImage = cv2.cvtColor(classImage, cv2.COLOR_BGR2RGB)

while True:
    # try:
    success, image = classImage.read()
    # except IOError:
    #     print('File location was not valid. Make sure that your file was type correctly, including the file type.')
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
"""