import cv2
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

while True:

	mx = 0 #For tracking purposes

	my = 0

	mxd = 0

	myd = 0

	ret, frame = cap.read()

	frame = cv2.blur(frame,(10,10)) #reduce noise

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	lower = np.array([100,70,30]) #Upper and lower limits

	upper = np.array([179,255,255])

	mask = cv2.inRange(hsv, lower, upper) #Mask

	white = np.asarray(mask) #Finding white points in mask (which would be the tip of the stylus)

	coordList = np.argwhere(white == 255)

	try:
		for n in range(0, len(coordList)): #Find the position of the tip of the pen, average everything
			mxd += coordList[n][0]
			myd += coordList[n][1]
		mxd = mxd/len(coordList)
		myd = myd/len(coordList)
	except:
		pass

	ret, frame = cap.read() #Repeating the process above to get two readings, so that we can determine the motion.

	frame = cv2.blur(frame,(5,5))

	hsv1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	lower = np.array([100,70,30])

	upper = np.array([179, 255, 255])

	mask1 = cv2.inRange(hsv1, lower, upper)

	finalout = cv2.absdiff(mask1, mask)

	cv2.imshow("trackpad", mask1)

	cv2.imshow("original", frame)

	white = np.asarray(mask1)

	coordList = np.argwhere(white == 255)

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
	#motion detection, in what direction
	if mxd-mx > 3 or mxd-mx < -3:
		if mxd-mx < 120 and mxd-mx > -120:
			movex = (mxd-mx)*10 
			#pyautogui.moveRel(0, (mxd-mx))
	if myd-my > 3 or myd-my < -3:
		if myd-my < 120 and myd-my > - 120:
			movey = (myd - my)*10
			#pyautogui.moveRel((myd-my),0)

	xpos, ypos = pyautogui.position()
	pyautogui.moveTo(xpos+movey, ypos+movex) #Very rickety movement, but accurate

	#print time.time()-start_time
	#determine a click
	if mxd-mx <= 30 and mxd-mx >= -30:
		if movey >= 10 and movey <= 60:
			print "click"
			pyautogui.click()
		if movey <= -10 and movey >= -60:
			print "click"
			pyautogui.click()

	print movex, movey

	if cv2.waitKey(1) == 27:
		break

cap.release()
cv2.destroyAllWindows()
