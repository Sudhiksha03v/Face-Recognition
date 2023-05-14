#pip install cmake
#pip install face_recognition
#pip install opencv-python




import face_recognition
import cv2
import numpy
import csv
from datetime import datetime



video_capture = cv2.VideoCapture(0)


# Loading the preset images of the faces 

my_img = face_recognition.load_image_file("faces/me.jpg")
my_encoding = face_recognition.face_encodings(my_img)[0]
tony_img = face_recognition.load_image_file("faces/ton.jpeg")
tony_encoding = face_recognition.face_encodings(tony_img)[0]

known_face_encodings = [my_encoding, tony_encoding]
known_face_names = ["Me","Tony"]

#list of the individual faces
students = known_face_names.copy()

face_locations= []
face_encodings = []

#Getting the details for the date and the time

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")


#csv credentials
f = open(f"{current_date}.csv", "w+", newline="")
lnwriter = csv.writer(f)


while True:
    #Grabbing a single frame of the video
    _, frame = video_capture.read()
    #Resizing the frame of the video
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    #Converting the frame to grayscale
    rbg_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
    #Detecting the faces in the grayscale frame
    face_locations = face_recognition.face_locations(rbg_small_frame)
    face_encodings = face_recognition.face_encodings(rbg_small_frame, face_locations)
    #Looping through the faces found in the frame

    for face_encoding in face_encodings:
        #Looping through the known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distance = face_recognition.face_distance(known_face_encodings,face_encoding)

        best_match_index = numpy.argmax(face_distance)

        if(matches[best_match_index]):
            name = known_face_names[best_match_index]

        #Adding text for the present present
        if name in known_face_names:
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (10,100)
            fontScale = 1
            fontColor = (255,0,0)
            thickness = 3
            lineType = 2
            cv2.putText(frame, name + "PersonPresent", bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType) 
            
            if name in students:
                students.remove(name)
                current_time = now.strftime("%H-%M-%S")
                lnwriter.writerow([name, current_time])

            #Adding csv for the present present




        cv2.imshow("Attendance",frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video.capture.release()
cv2.destroyAllWindows()
f.close()





    





