import cv2

image = cv2.imread("./giphy.gif")
#image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
image = cv2.bitwise_not(image)
cv2.imshow("This is processed image",image)

cv2.waitKey(0)
cv2.destroyAllWindows()
