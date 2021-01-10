import cv2
import numpy as np
import face_recognition
import os

class Face(object):
    def __init__(self, location, encoding, screenshotIndex):
        self.location = location
        self.encoding = encoding
        self.screenshotIndex = screenshotIndex

    def add_name(self, name):
        self.name = name

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
            self.studentNames.append(os.path.splitext(student)[0].upper())

    def encode(self):
        for image in self.studentIDImages:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            encodedImage = face_recognition.face_encodings(image)[0]
            self.studentIDsEncoded.append(encodedImage)

        print('All encoding finished')

class ZoomRecognize(object):
    def __init__(self, screenshotPath):
        self.screenshotPath = screenshotPath
        self.screenshotImages = []
        self.screenshotFileNames = os.listdir(screenshotPath)

        for screenshot in self.screenshotFileNames:
            currentImage = cv2.imread(f'{screenshotPath}/{screenshot}')
            currentImage = cv2.cvtColor(currentImage, cv2.COLOR_BGR2RGB)
            self.screenshotImages.append(currentImage)
        print('Screenshot images: ' + str(self.screenshotFileNames))
  
    def recognize(self, students : SIDRecognize):
        faces = [] # Array of faces

        # For each zoom screenshot, add the faces into Faces
        for i in range(0, len(self.screenshotImages)):

            faceLocationsInScreenshot = face_recognition.face_locations(self.screenshotImages[i])
            encodedFacesInScreenshot = face_recognition.face_encodings(self.screenshotImages[i], faceLocationsInScreenshot)

            if len(faceLocationsInScreenshot) != len(encodedFacesInScreenshot):
                print('Something is very very wrong')
                return []

            for j in range(0, len(faceLocationsInScreenshot)):
                currentFace = Face(faceLocationsInScreenshot[j], encodedFacesInScreenshot[j], i)
                faces.append(currentFace)

        presentStudentNames = []
        for face in faces:
            correctMatches = face_recognition.compare_faces(students.studentIDsEncoded, face.encoding)
            faceDistance = face_recognition.face_distance(students.studentIDsEncoded, face.encoding)
            matchIndex = np.argmin(faceDistance)

            if correctMatches[matchIndex]:
                name = students.studentNames[matchIndex].upper()
                print('Detected student: ' + name)
                presentStudentNames.append(name)
                face.add_name(name)
                self.drawFace(face)

        return presentStudentNames

    def drawFace(self, face):
        # draw rectangle around face
        rgb = (90, 20, 20)  # colour of label background and box around face
        cv2.rectangle(self.screenshotImages[face.screenshotIndex],
                      (face.location[3], face.location[0]), (face.location[1], face.location[2]),
                      rgb, 2)

        # font settings for label
        fontface = cv2.FONT_HERSHEY_SIMPLEX
        fontscale = (face.location[1] - face.location[3]) * 0.0075
        fontthickness = 2

        # draw background box for label
        labelSize = cv2.getTextSize(face.name, fontface, fontscale, fontthickness)
        _x1 = face.location[3] - 15
        _y1 = face.location[2] + 50
        _x2 = _x1 + labelSize[0][0] + 5
        _y2 = face.location[2] + 30 - int(labelSize[0][1])
        cv2.rectangle(self.screenshotImages[face.screenshotIndex],
                      (_x1, _y1), (_x2, _y2), rgb, cv2.FILLED)

        # draw text in label
        cv2.putText(self.screenshotImages[face.screenshotIndex], face.name,
                    (face.location[3] - 10, face.location[2] + 40), fontface, fontscale,
                    (255, 255, 255), fontthickness)

    def showImages(self):
        # display the images
        for i in range(0, len(self.screenshotImages)):
            image = cv2.cvtColor(self.screenshotImages[i], cv2.COLOR_RGB2BGR)
            cv2.imshow(f'Image {i}', image)

        cv2.waitKey()


if __name__ == "__main__":
    students = SIDRecognize("ImagesAttendance")
    zoomScreenshots = ZoomRecognize("ZoomImages")
    students.encode()
    zoomScreenshots.recognize(students)