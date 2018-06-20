import cv2
from multiprocessing import Process
import numpy as np
import pyautogui
pyautogui.FAILSAFE = False


cap = cv2.VideoCapture(0)


mx = 0

my = 0

mxd = 0

myd = 0

x = 0

y = 0

clcount = 0


while True:

	area = 0

	area1 = 0

	mx = 0

	my = 0

	mxd = 0

	myd = 0

	ret, frame = cap.read()

	frame = cv2.blur(frame,(10,10))

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	lower = np.array([100,70,30])

	upper = np.array([140,185,185])

	mask = cv2.inRange(hsv, lower, upper)

	white = np.asarray(mask)

	coordList = np.argwhere(white == 255)

	area = len(coordList)

	try:
		for n in range(0, len(coordList)):
			mxd += coordList[n][0]
			myd += coordList[n][1]
		mxd = mxd/len(coordList)
		myd = myd/len(coordList)
	except:
		pass

	ret, frame = cap.read()

	frame = cv2.blur(frame,(5,5))

	hsv1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	lower = np.array([100,70,30])

	upper = np.array([140, 185, 185])

	mask1 = cv2.inRange(hsv1, lower, upper)

	finalout = cv2.absdiff(mask1, mask)

	cv2.imshow("trackpad", mask1)

	cv2.imshow("original", frame)

	white = np.asarray(mask1)

	coordList = np.argwhere(white == 255)

	area1 = len(coordList)

	try:
		for n in range(0, len(coordList)):
			mx += coordList[n][0]
			my += coordList[n][1]
		mx = mx/len(coordList)
		my = my/len(coordList)

	except:

		pass

	#print (mxd - mx), (myd - my)

	movex = 0

	movey = 0

	clcount = 0
	#print time.time()-start_time

	if abs(area-area1) > 210:
		if clcount < 1:
			print "click"
			pyautogui.click()
		clcount += 1

	if clcount < 1:

		if mxd-mx > 3 or mxd-mx < -3:
			if mxd-mx < 120 and mxd-mx > -120:
				movex = (mxd-mx)*5
				#pyautogui.moveRel(0, (mxd-mx))
		if myd-my > 3 or myd-my < -3:
			if myd-my < 120 and myd-my > - 120:
				movey = (myd - my)*5
				#pyautogui.moveRel((myd-my),0)

	xpos, ypos = pyautogui.position()

	#for i in range(0,4):

	pyautogui.moveRel(movey, movex,0.025)

	print movex, movey, area-area1

	if cv2.waitKey(1) == 27:
		break

cap.release()
cv2.destroyAllWindows()




