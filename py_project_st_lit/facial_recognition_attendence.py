import face_recognition
import cv2
import numpy as np 
import csv
import os 
from datetime import datetime
import sys
import os


Video_capture = cv2.VideoCapture(0)

# 1. FIXED: Corrected load_image_file and face_encodings methods
thomas_edison = face_recognition.load_image_file("/Users/shyamalkar/Desktop/Python_project/py_project_st_lit/history001.jpg")
thomas_edison_encode = face_recognition.face_encodings(thomas_edison)[0]

ratan_tata = face_recognition.load_image_file("/Users/shyamalkar/Desktop/Python_project/py_project_st_lit/images-1.jpg")
ratan_tata_encode = face_recognition.face_encodings(ratan_tata)[0]

bejamin_nitenyahu = face_recognition.load_image_file("/Users/shyamalkar/Desktop/Python_project/py_project_st_lit/images-2.jpg")
bejamin_nitenyahu_encode = face_recognition.face_encodings(bejamin_nitenyahu)[0]

benjamin_franklin = face_recognition.load_image_file("/Users/shyamalkar/Desktop/Python_project/py_project_st_lit/images-3.jpg")
benjamin_franklin_encode = face_recognition.face_encodings(benjamin_franklin)[0]

nikola_tesla = face_recognition.load_image_file("/Users/shyamalkar/Desktop/Python_project/py_project_st_lit/images-4.jpg")
nikola_tesla_encode = face_recognition.face_encodings(nikola_tesla)[0]

rabindranath_tagore = face_recognition.load_image_file("/Users/shyamalkar/Desktop/Python_project/py_project_st_lit/images-5.jpg")
rabindranath_tagore_encode = face_recognition.face_encodings(rabindranath_tagore)[0]

vagat_singh = face_recognition.load_image_file("/Users/shyamalkar/Desktop/Python_project/py_project_st_lit/images-6.jpg")
vagat_singh_encode = face_recognition.face_encodings(vagat_singh)[0]

sukdeb = face_recognition.load_image_file("/Users/shyamalkar/Desktop/Python_project/py_project_st_lit/images-7.jpg")
sukdeb_encode = face_recognition.face_encodings(sukdeb)[0]

rani_lakhshmi = face_recognition.load_image_file("/Users/shyamalkar/Desktop/Python_project/py_project_st_lit/images-8.jpg")
rani_lakhshmi_encode = face_recognition.face_encodings(rani_lakhshmi)[0]

swami_viveka = face_recognition.load_image_file("/Users/shyamalkar/Desktop/Python_project/py_project_st_lit/images-9.jpg")
swami_viveka_encode = face_recognition.face_encodings(swami_viveka)[0]

OSHO = face_recognition.load_image_file("/Users/shyamalkar/Desktop/Python_project/py_project_st_lit/images-10.jpg")
OSHO_encode = face_recognition.face_encodings(OSHO)[0]

elon_musk = face_recognition.load_image_file("/Users/shyamalkar/Desktop/Python_project/py_project_st_lit/images-11.jpg")
elon_musk_encode = face_recognition.face_encodings(elon_musk)[0]

rakesh_sharma = face_recognition.load_image_file("/Users/shyamalkar/Desktop/Python_project/py_project_st_lit/images-12.jpg")
rakesh_sharma_encode = face_recognition.face_encodings(rakesh_sharma)[0]


known_face_encoding = [
    thomas_edison_encode, 
    ratan_tata_encode,
    benjamin_franklin_encode,
    nikola_tesla_encode,
    rabindranath_tagore_encode,
    vagat_singh_encode,
    sukdeb_encode,
    rani_lakhshmi_encode,
    swami_viveka_encode,
    OSHO_encode,
    elon_musk_encode,
    rakesh_sharma_encode
]

# 2. FIXED: Added the missing commas between list strings
known_face_name = [
    "thomas edison",
    "ratan tata",
    "benjamin franklin",
    "nikola tesla",
    "rabindranath tagore",
    "vagat singh",
    "sukdeb",
    "rani lakshmi",
    "swami viveka",
    "OSHO",
    "elon musk",
    "rakesh sharma"
]

students = known_face_name.copy()

face_locations = []
face_encodings = []
face_names = []
s = True 

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(current_date + '.csv', "w+", newline='')
inwriter = csv.writer(f)

while True: 
    _, frame = Video_capture.read()

    small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    if s: 
        face_locations = face_recognition.face_locations(rgb_small_frame)
        # 3. FIXED: Passed 'face_locations' (plural) correctly here
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
            name = "Unknown"
            
            face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
            # 4. FIXED: Changed np.margin to np.argmin
            best_match_index = np.argmin(face_distance)
            
            if matches[best_match_index]:
                name = known_face_name[best_match_index]

            face_names.append(name)
            if name in known_face_name:
                if name in students:
                    students.remove(name)
                    print(students)
                    current_time = datetime.now().strftime("%H-%M-%S") # Updates time per log
                    inwriter.writerow([name, current_time])

    cv2.imshow('attendance system', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

Video_capture.release()
cv2.destroyAllWindows()
f.close()
