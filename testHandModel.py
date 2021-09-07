import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import load_model


import UdpCommunications as U
import time
import threading

actions = ['fireball', 'thunderStorm', 'ignition', 'magicCasting', 'UICall']
seq_length = 30

model = load_model('models/model2_1.0.h5')

# MediaPipe hands model
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

# w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
# out = cv2.VideoWriter('input.mp4', fourcc, cap.get(cv2.CAP_PROP_FPS), (w, h))
# out2 = cv2.VideoWriter('output.mp4', fourcc, cap.get(cv2.CAP_PROP_FPS), (w, h))

seq = []
action_seq = []

send_action = ''
this_action = '?'

<<<<<<< Updated upstream
ismagicCasting = False
isUsedUICall = False

isSendingValid = False
=======
>>>>>>> Stashed changes

class server:

    def serverTrans(self):
        # Create UDP socket to use for sending (and receiving)
        sock = U.UdpCommunications(
            udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)

        global ismagicCasting
        global isUsedUICall
        i = 0

<<<<<<< Updated upstream
        '''
        if send_action == 'magicCasting':
            ismagicCasting = True

        if send_action == 'UICall':
            isUsedUICall = True

        if(isUsedUICall == False and ismagicCasting == True and send_action != 'magicCasting' and send_action != 'UICall'):
            print("pass magic casting!")
            print(send_action)
            sock.SendData(send_action)
            ismagicCasting = False

        if(isUsedUICall == True and ismagicCasting == False and send_action == 'UICall'):
            print("pass UI Call!")
            print(send_action)
            sock.SendData(send_action)
            isUsedUICall = False
        '''

        print(isSendingValid)
        if(send_action != 'UNKNOWN') :
            pass
            #sock.SendData(send_action)

        if(isSendingValid):
            sock.SendData(send_action)
        #sock.SendData('Sent from Python: ' + str(i)) # Send this string to other application
=======
        sock.SendData(send_action)
        # sock.SendData('Sent from Python: ' + str(i)) # Send this string to other application
>>>>>>> Stashed changes

        i += 1

        data = sock.ReadReceivedData()  # read data

        if data != None:  # if NEW data has been received since last ReadReceivedData function call
            print(data)  # print new received data

        threading.Timer(2, self.serverTrans).start()



    def serverChangeImmediately(self):
        # Create UDP socket to use for sending (and receiving)
        sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)

        global ismagicCasting
        global isUsedUICall
        i = 0
        
        if(send_action != 'UNKNOWN') :
            pass
            #sock.SendData(send_action)

        sock.SendData(send_action)
        #sock.SendData('Sent from Python: ' + str(i)) # Send this string to other application

        i += 1

        data = sock.ReadReceivedData() # read data

        if data != None: # if NEW data has been received since last ReadReceivedData function call
            print(data) # print new received data


# server making work
curS = server()
curS.serverTrans()

<<<<<<< Updated upstream

class valInitializer:

    def initializeAction(self):
        global isSendingValid 
        isSendingValid = False
        #this_action = 'NOACTION'
        threading.Timer(2.5, self.initializeAction).start()


# variable initializer making work
valInit = valInitializer()
valInit.initializeAction()


while True :
    #curS.serverTrans()
    
    while cap.isOpened():
        #curS.serverTrans()
=======
while True:
    # curS.serverTrans()

    while cap.isOpened():

        # curS.serverTrans()
>>>>>>> Stashed changes

        ret, img = cap.read()
        img0 = img.copy()

        img = cv2.flip(img, 1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if result.multi_hand_landmarks is not None:
            for res in result.multi_hand_landmarks:
                joint = np.zeros((21, 4))
                for j, lm in enumerate(res.landmark):
                    joint[j] = [lm.x, lm.y, lm.z, lm.visibility]

                # Compute angles between joints
                v1 = joint[[0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0,
                            13, 14, 15, 0, 17, 18, 19], :3]  # Parent joint
                v2 = joint[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                            13, 14, 15, 16, 17, 18, 19, 20], :3]  # Child joint
                v = v2 - v1  # [20, 3]
                # Normalize v
                v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

                # Get angle using arcos of dot product
                angle = np.arccos(np.einsum('nt,nt->n',
                                            v[[0, 1, 2, 4, 5, 6, 8, 9, 10,
                                                12, 13, 14, 16, 17, 18], :],
                                            v[[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19], :]))  # [15,]

                angle = np.degrees(angle)  # Convert radian to degree

                d = np.concatenate([joint.flatten(), angle])

                seq.append(d)

                mp_drawing.draw_landmarks(img, res, mp_hands.HAND_CONNECTIONS)

                if len(seq) < seq_length:
                    continue

                input_data = np.expand_dims(
                    np.array(seq[-seq_length:], dtype=np.float32), axis=0)

                y_pred = model.predict(input_data).squeeze()

                i_pred = int(np.argmax(y_pred))
                conf = y_pred[i_pred]

                if conf < 0.9:
                    continue

                action = actions[i_pred]
                action_seq.append(action)

                if len(action_seq) < 3:
                    continue

<<<<<<< Updated upstream
                
                #this_action = 'UNKNOWN'
=======
                #this_action = '?'
>>>>>>> Stashed changes
                send_action = this_action
                

                if action_seq[-1] == action_seq[-2] == action_seq[-3]:
                    this_action = action
                    isSendingValid = True
                    
                #print(send_action)

<<<<<<< Updated upstream
                #time.sleep(1)
                #curS.serverChangeImmediately()
                #threading.Timer(2, curS.serverChangeImmediately).start()
                
                cv2.putText(img, f'{this_action.upper()}', org=(int(res.landmark[0].x * img.shape[1]), int(res.landmark[0].y * img.shape[0] + 20)), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)
    
=======
                cv2.putText(img, f'{this_action.upper()}', org=(int(res.landmark[0].x * img.shape[1]), int(
                    res.landmark[0].y * img.shape[0] + 20)), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)

>>>>>>> Stashed changes
        # out.write(img0)
        # out2.write(img)
        cv2.imshow('img', img)
        if cv2.waitKey(1) == ord('q'):
            break
<<<<<<< Updated upstream




=======
>>>>>>> Stashed changes
