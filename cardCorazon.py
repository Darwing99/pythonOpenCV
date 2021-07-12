import cv2
import numpy as np


image = cv2.imread("images/Corazones/cinco.png")
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
template1 = cv2.imread("images/Corazones/corazon.png", 0)
def puntosTemplate(image, template):
    points = []
    threshold = 0.85

    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    candidates = np.where(res >= threshold)
    candidates = np.column_stack([candidates[1], candidates[0]])

    i = 0
    while len(candidates) > 0:
        if i == 0: points.append(candidates[0])
        else:
            to_delete = []
            for j in range(0, len(candidates)):
                diff = points[i-1] - candidates[j]
                if abs(diff[0]) < 10 and abs(diff[1]) < 10:
                    to_delete.append(j)
            candidates = np.delete(candidates, to_delete, axis=0)
            if len(candidates) == 0: break
            points.append(candidates[0])
        i += 1
    return points

points1 = puntosTemplate(image_gray, template1)
template2 = cv2.flip(template1, -1)
points2 = puntosTemplate(image_gray, template2)

points= np.concatenate((points1, points2)) if (
    len(points1) > 0 and len(points2) > 0) else [] if(
         len(points1) == 0 and len(points2) == 0) else points2 if(
             len(points1) == 0 and len(points2) > 0) else points1 if(
                 len(points1) > 0 and len(points2) == 0) else print("Elementos vacios")

for point in points:
    x1, y1 = point[0], point[1]
    x2, y2 = point[0] + template1.shape[1], point[1] + template1.shape[0]
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.putText(image, str(len(points)), (95, 35), 1, 3, (0, 255, 0), 2)
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()