import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = 'img'
images = []
classNames = []

# Images Load karna
myList = os.listdir(path)
for cl in myList:
    curImg = face_recognition.load_image_file(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

# Encoding Function
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if len(encodes) > 0:
            encodeList.append(encodes[0])
    return encodeList

# Attendance Function (r+ ki jagah a+ use karein taaki error na aaye)
def markAttendance(name):
    with open('Attendance.csv', 'a+') as f:
        f.seek(0)
        myDataList = f.readlines()
        nameList = [line.split(',')[0] for line in myDataList]

        if name not in nameList:
            now = datetime.now()
            dateString = now.strftime('%d-%m-%Y') # Example: 21-03-2026
            dtString = now.strftime('%H:%M:%S')
            f.write(f'\n{name},{dtString},{dateString}')
            print(f"✅ {name} ki attendance lag gayi!")

encodeListKnown = findEncodings(images)
print("✅ Encoding Complete") 

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success: break

    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    imgS = np.ascontiguousarray(imgS, dtype=np.uint8)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex] and faceDis[matchIndex] < 0.6:
            name = classNames[matchIndex].upper()
            # 🔥 YAHAN CALL HO RAHA HAI AB
            markAttendance(name) 
        else:
            name = "UNKNOWN"

        # Drawing Part
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
        cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
        cv2.putText(img, name, (x1+6,y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)

    # Window dikhane ke liye loop ke andar hona chahiye
    cv2.imshow('Webcam', img)
    
    # 'q' dabane par exit hoga
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()