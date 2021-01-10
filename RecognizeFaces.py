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
        faceLocations = []
        encodedFaces = []
        faces = []
        # For each zoom screenshot, add the faces to the faceLocations array.

        for i in range(0, len(self.screenshotImages)):
            faceLocationsInScreenshot = face_recognition.face_locations(self.screenshotImages[i])
            faceLocations = faceLocations + faceLocationsInScreenshot

            encodedFacesInScreenshot = face_recognition.face_encodings(self.screenshotImages[i], faceLocationsInScreenshot)
            encodedFaces = encodedFaces + encodedFacesInScreenshot

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

                # draw rectangle + textbox around the face
                cv2.rectangle(self.screenshotImages[face.screenshotIndex],
                              (face.location[3], face.location[0]), (face.location[1], face.location[2]),
                              (255, 0, 255), 2)
                cv2.putText(self.screenshotImages[face.screenshotIndex],name,
                            (face.location[3]-10, face.location[2]+30), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (255,255,255), 2)

        return presentStudentNames

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