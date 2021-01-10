import cv2
import numpy as np
import face_recognition
import os

class SIDRecognize(object):
    def __init__(self, studentIDPath):
        # retrieve images from ImagesAttendance folder
        self.studentIDPath = studentIDPath
        self.studentIDImages = []
        self.studentNames = []
        self.studentIDFileNames = os.listdir(studentIDPath)
        self.studentIDsEncoded = []
        
        # retrieves names of students present from retrieved files
        for student in self.studentIDFileNames:
            currentImage = cv2.imread(f'{studentIDPath}/{student}')
            self.studentIDImages.append(currentImage)
            self.studentNames.append(os.path.splitext(student)[0])

        print(self.studentNames)

    def encode(self):
        for image in self.studentIDImages:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            encodedImage = face_recognition.face_encodings(image)[0]
            self.studentIDsEncoded.append(encodedImage)
            print('Encoding finished')

class ZoomRecognize(object):
    def __init__(self, screenshotPath):
        self.screenshotPath = screenshotPath
        self.screenshotImages = []
        self.screenshotFileNames = os.listdir(screenshotPath)

        for screenshot in self.screenshotFileNames:
            currentImage = cv2.imread(f'{screenshotPath}/{screenshot}')
            currentImage = cv2.cvtColor(currentImage, cv2.COLOR_BGR2RGB)
            self.screenshotImages.append(currentImage)
        print(self.screenshotFileNames)
  
    def recognize(self, students : SIDRecognize):
        facesInScreenshot = []
        screenshotEncodedFaces = []
        # For each zoom screenshot, add the faces to the facesInScreenshot array.
        for image in self.screenshotImages:
            facesInScreenshot = facesInScreenshot + face_recognition.face_locations(image)
            screenshotEncodedFaces = screenshotEncodedFaces + face_recognition.face_encodings(image, facesInScreenshot)

        for encodedFace in screenshotEncodedFaces:
            correctMatches = face_recognition.compare_faces(students.studentIDsEncoded, encodedFace)
            faceDistance = face_recognition.face_distance(students.studentIDsEncoded, encodedFace)
            matchIndex = np.argmin(faceDistance)

            if correctMatches[matchIndex]:
                name = students.studentNames[matchIndex].upper()
                print(name)


if __name__ == "__main__":
    students = SIDRecognize("ImagesAttendance")
    zoomScreenshots = ZoomRecognize("ZoomImages")
    students.encode()
    zoomScreenshots.recognize(students)