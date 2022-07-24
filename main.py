#!/bin/python3

####### Libs #######

# cv2 for open webcam, read images.
import cv2

# mediapipe for hand landmarks connection , draw 3d hand.
import mediapipe as mp

# time for Frames per sec.
import time 

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
"""
#for static image:

# must be .png / .jpg only
IMAGE_FILES = ["Images\image3.jpg"] # put path of image
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5) as hands:
    for idx, file in enumerate(IMAGE_FILES):
       
        # Read an image, flip it around y-axis for correct handedness output (see above).
        image = cv2.flip(cv2.imread(file), 1)
        
        # Convert the BGR image to RGB before processing.
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Print handedness and draw hand landmarks on the image.
        print('Handedness:', results.multi_handedness)
        
        if not results.multi_hand_landmarks:
            continue

        image_height, image_width, _ = image.shape
        annotated_image = image.copy()
        for hand_landmarks in results.multi_hand_landmarks:
            print(
                'hand_landmarks:',
                hand_landmarks
                )
            print(
                f'Index finger tip coordinates: (',
                f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
                f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
                )
        mp_drawing.draw_landmarks(
            annotated_image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
        cv2.imwrite(
            '/tmp/annotated_image' + str(idx) + '.png',
            cv2.flip(annotated_image, 1))
        
        # Draw hand world landmarks.
        if not results.multi_hand_world_landmarks:
            continue
        for hand_world_landmarks in results.multi_hand_world_landmarks:
            mp_drawing.plot_landmarks(
            hand_world_landmarks,
            mp_hands.HAND_CONNECTIONS,
            azimuth=5)
"""


# for webcam input:
pTime = 0 
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of  'continue'.
            continue

        # to improve performance, optionally mark the image as not writeable to pass reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annontations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )
            
            # Draw hand world landmarks.
                    
        """
        if not results.multi_hand_world_landmarks:
            continue
        for hand_world_landmarks in results.multi_hand_world_landmarks:
            mp_drawing.plot_landmarks(
            hand_world_landmarks,
            mp_hands.HAND_CONNECTIONS,
            azimuth=5)
        """
        

        # for fps
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (50, 50)
        fontScale = 1
        color = (0, 0, 0)
        thickness = 2
            
        image = cv2.putText(
                image, 
                f'FPS: {int(fps)}',
                org,
                font,
                fontScale,
                color,
                thickness,
                cv2.LINE_AA
            )

        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('Hydra-Team', image)
        if cv2.waitKey(1) & 0Xff == 27:
            break
cap.release()
