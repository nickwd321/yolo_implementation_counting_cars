from ultralytics import YOLO
import cv2
import numpy as np

polyg = []
mobiles = {} #follows the convention { id1 : [pos1,pos2,pos3],.....}
video_path = '7 minutes cars driving past on road (1) (1).mp4'
class MOBILE(): #this should contain infomation about the objects passing by the screen and calcuate there pixels per second as a speed
    def __init__(self,id,pos):
        self.id = id
        self.pos = pos

    pass

def numberinpoly(x,num):
    if (x == 1):
        num = num + 1


    return num
def polygon(frame,color):
    global polyg
    polygnp = np.asarray(polyg)
   # print(f'polylines  :{polygnp}')
 #   tst = np.array([[150,150],[600,600],[200,200],[10,10]])
    cv2.polylines(frame, [polygnp], True, (255, 150, 0), 4,lineType=cv2.LINE_4)

def pixpersec(x,y):
    pass
def collisioncheck(xp,yp,id):
    #xp = 15
    #yp = 250

    cnt = 0
    global polyg
    polygnp = np.asarray(polyg)
   # testpoly = [[176,180],[420,200],[414,280],[128,295]]
   # testpoly = np.asarray(testpoly)
    for i in range(len(polygnp / 2)):
        # i need to pull out pairs of points from polyg
        x1 , y1 = polygnp[i - 1]
        x2, y2 = polygnp[i]

       # (x1,y1),(x2,y2) = edge
        if (yp < y1) != (yp < y2) and xp < x1 + ((yp - y1)/(y2 - y1)*(x2-x1)):
            cnt += 1
    #print(f'ID: {id} :number of ray cast contacts: {cnt}  :count')
    return cnt%2 == 1


    pass

def click_event(event, x , y , flags, params):

    if event == cv2.EVENT_LBUTTONDOWN:
        global polyg
        polyg.append([])
        polyg[len(polyg) - 1].append(x)
        polyg[len(polyg) - 1].append(y)
        return(x,y)
    if event == cv2.EVENT_RBUTTONDOWN:
        polyg.clear()
        return

def search(values, searchFor):
    for k in values:
        for v in values[k]:
            if searchFor == v:
                return True
    return False

#step 1 load model
model = YOLO('yolov8n.pt')  # Load an official Segment model

#step 2 load video

cap = cv2.VideoCapture(video_path)

#####################################################################
#main loop
ret = True
#read frames
while ret:
    ret, frame = cap.read()
    if ret:
##################################################################################
        #detect objects
        #track objects
        results = model.track(frame,persist=True,conf=0.44,)#
        boxes = results[0].boxes.xyxy
        id = results[0].boxes.id
#########################################################################################
      #gathering bounding box info
        try:
          #  boxes= boxes[0]
            boxes = boxes.numpy()
            boxes = np.int0(boxes)
        except:
            boxes = np.array([])
######################################################################################
      #seprating out bounding box info and drawing mid points
        num = 0
        for i in range(boxes.size // 4):

            boxestemp =boxes[i]
            idtemp = id[i]
            ###DRAW CIRCLE at the center of the rectangel
            midx , midy = ((boxestemp[0]+boxestemp[2])//2,((boxestemp[1]+boxestemp[3])//2)-20)
            cv2.circle(frame, center=(midx, midy), radius=5, color=(0, 255, 250), thickness=3, lineType=cv2.LINE_4, shift=0)

            checkc = collisioncheck(midx,midy,idtemp)
            num = numberinpoly(checkc,num)


########################################################################################
        cv2.putText(frame,f'number of objects in sector:  {num}',(25,25),fontFace=cv2.FONT_HERSHEY_DUPLEX,fontScale=0.5,color = (255,0,255),thickness=1)
#############################################################################################
      #plotting bounding boxes and drawing the line
        frame_ = results[0].plot()
######################################################################################
        try:
            polygon(frame_, 255)
        except:
            pass
########################################################################################
      #showing the frame
    #visulize
        cv2.imshow('frame',frame_)
############################################################################################
            # gathring mouse clickinfo
            # showing the line on screen

        mousepossition = cv2.setMouseCallback('frame', click_event)
##########################################################################################

      #allowing frame by fram of vedio
        if cv2.waitKey(1) & 0xFF == ord('q'): #gives a 1ms window to exit the code by pressing q
            break
     #   if cv2.waitKey(10000) & 0xFF == ord('l'):  # gives a 1ms window to exit the code by pressing q
     #    pass


