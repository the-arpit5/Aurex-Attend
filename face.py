import cv2
import face_recognition
import numpy as np

# =========================
# STEP 1: Load Images
# =========================
img1 = face_recognition.load_image_file('img/Henry Cavill.jpg')
img2 = face_recognition.load_image_file('img/Henry Cavill2.jpg')

# =========================
# STEP 2: Resize (IMPORTANT)
# =========================
img1 = cv2.resize(img1, (500, 500))
img2 = cv2.resize(img2, (500, 500))

# =========================
# STEP 3: Convert RGB -> BGR (for display)
# =========================
img1_display = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
img2_display = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)

# =========================
# STEP 4: Face Detection + Encoding
# =========================
faceLoc1 = face_recognition.face_locations(img1)[0]
encode1 = face_recognition.face_encodings(img1)[0]

faceLoc2 = face_recognition.face_locations(img2)[0]
encode2 = face_recognition.face_encodings(img2)[0]

# =========================
# STEP 5: Draw Rectangle
# =========================
cv2.rectangle(img1_display,
              (faceLoc1[3], faceLoc1[0]),
              (faceLoc1[1], faceLoc1[2]),
              (255, 0, 255), 2)

cv2.rectangle(img2_display,
              (faceLoc2[3], faceLoc2[0]),
              (faceLoc2[1], faceLoc2[2]),
              (255, 0, 255), 2)

# =========================
# STEP 6: Compare Faces
# =========================
results = face_recognition.compare_faces([encode1], encode2)
distance = face_recognition.face_distance([encode1], encode2)

print("Match Result:", results)
print("Face Distance:", distance)

# =========================
# STEP 7: Show Result Text
# =========================
text = f"Match: {results[0]} | Dist: {round(distance[0], 2)}"

cv2.putText(img2_display, text, (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# =========================
# STEP 8: Show Images
# =========================
cv2.imshow("Image 1", img1_display)
cv2.imshow("Image 2", img2_display)

cv2.waitKey(0)
cv2.destroyAllWindows()


# import cv2
# import face_recognition
# import numpy as np

# # Load images
# imgbest = face_recognition.load_image_file('img/Henry Cavill.jpg')
# #imgbest = cv2.cvtColor(imgbest, cv2.COLOR_BGR2RGB)

# imgdone = face_recognition.load_image_file('img/Henry Cavill2.jpg')
# #imgdone = cv2.cvtColor(imgdone, cv2.COLOR_BGR2RGB)

# # Find face location
# faceLoc = face_recognition.face_locations(imgbest)[0]
# encodebest = face_recognition.face_encodings(imgbest)[0]
# cv2.rectangle(imgbest,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)

# ##imgIron = cv2.cvtColor(imgIron, cv2.COLOR_RGB2BGR)
# # Show images
# cv2.imshow('Henry Cavill',imgbest)
# cv2.imshow('Henry Cavill2', imgdone)

# cv2.waitKey(0)
# #cv2.destroyAllWindows()