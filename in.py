import cv2
import mediapipe as mp
import serial
import time
from math import dist


COM_PORT = 'COM10'          # change to your Arduino port according to Device Manager
BAUDRATE = 9600

EYE_AR_THRESH = 0.25      
EYE_AR_CONSEC_FRAMES = 90  


arduino = serial.Serial(COM_PORT, BAUDRATE, timeout=1)
time.sleep(2)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,      
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


LEFT_EYE_IDXS  = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_IDXS = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(pts):

    A = dist(pts[1], pts[5])
    B = dist(pts[2], pts[4])
    C = dist(pts[0], pts[3])
    return (A + B) / (2.0 * C)

cap = cv2.VideoCapture(1)

COUNTER = 0
drowsy = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]

        left_eye_pts = []
        right_eye_pts = []

        for idx in LEFT_EYE_IDXS:
            lm = face_landmarks.landmark[idx]
            left_eye_pts.append((lm.x * w, lm.y * h))

        for idx in RIGHT_EYE_IDXS:
            lm = face_landmarks.landmark[idx]
            right_eye_pts.append((lm.x * w, lm.y * h))

        leftEAR = eye_aspect_ratio(left_eye_pts)
        rightEAR = eye_aspect_ratio(right_eye_pts)
        ear = (leftEAR + rightEAR) / 2.0


        for (x, y) in left_eye_pts + right_eye_pts:
            cv2.circle(frame, (int(x), int(y)), 2, (0, 255, 0), -1)

        if ear < EYE_AR_THRESH:
            COUNTER += 1
            if COUNTER >= EYE_AR_CONSEC_FRAMES and not drowsy:
                drowsy = True
                arduino.write(b'a') 
        else:
            if drowsy:
                drowsy = False
                arduino.write(b'b')  
            COUNTER = 0

        cv2.putText(frame, f"EAR: {ear:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    else:
  
        if drowsy:
            drowsy = False
            arduino.write(b'b')

    status_text = "DROWSY" if drowsy else "AWAKE"
    color = (0, 0, 255) if drowsy else (0, 255, 0)
    cv2.putText(frame, status_text, (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Drowsiness Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()