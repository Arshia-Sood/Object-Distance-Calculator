import cv2
import numpy as np
import math

cam=cv2.VideoCapture(0)

dist_thresh=0.06912    # Pixel to cm conversion factor

# HSV range for yellow
yellow_lower=np.array([20,100,100])
yellow_upper=np.array([30,255,255])

while True:
    ret,frame=cam.read()

    if not ret:
        print("Error: Could not read from camera")
        break

    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    mask=cv2.inRange(hsv,lowerb=yellow_lower,upperb=yellow_upper)

    contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    obj_list=[]
    label=65

    for contour in contours:
        if cv2.contourArea(contour)>500:
            x,y,w,h=cv2.boundingRect(contour)
            cx=x+w//2
            cy=y+h//2
            obj_list.append((cx,cy,x,y,w,h))

            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
            cv2.circle(frame,(cx,cy),5,(0,0,255),-1)

            cv2.putText(frame,chr(label),(cx-50,cy+10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)
            label+=1

    for i in range(len(obj_list)-1):
        x1,y1=obj_list[i][0],obj_list[i][1]
        x2,y2=obj_list[i+1][0],obj_list[i+1][1]

        dist_pixels=math.sqrt((x2-x1)**2+(y2-y1)**2)
        dist_cm=dist_pixels*dist_thresh

        mid_x=(x1+x2)//2
        mid_y=(y1+y2)//2

        cv2.line(frame,(x1,y1),(x2,y2),(255,0,0),2)
        cv2.putText(frame,f"{dist_cm:.2f} cm",(mid_x,mid_y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),4)
    
    cv2.putText(frame,f"Objects: {len(obj_list)}",(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),3)
    cv2.putText(frame,"Press 'q' to quit",(10,frame.shape[0]-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(200,200,200),2)

    cv2.imshow("Mask",mask)
    cv2.imshow("Detected Objects",frame)

    if cv2.waitKey(1)&0xFF==ord("q"):
        break

cam.release()
cv2.destroyAllWindows()