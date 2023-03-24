import cv2
import mediapipe as mp
     
mp_drawning = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
     
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)     
     
with mp_hands.Hands(
    static_image_mode = False,
    max_num_hands = 2,
) as hands:
    
    while(True):      
    
        ret, frame = cap.read()
        if(ret == False):
            break
        
        height,width,_ = frame.shape
        frame=cv2.flip(frame,1)
        frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        
        
        results = hands.process(frame_rgb)
        
        if(results.multi_hand_landmarks is not None):
            for hand_landmark in results.multi_hand_landmarks:
                mp_drawning.draw_landmarks(frame,hand_landmark,mp_hands.HAND_CONNECTIONS)
                
               
            
        cv2.imshow('mask',frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
   
        
cap.release()     
cv2.destroyAllWindows()
  