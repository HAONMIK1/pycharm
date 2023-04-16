import my
import guri
import cv2
#1.전산관
image_path = "lo1.jpg"

my.my(image_path)

if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()

guri.go(image_path)


# #2.도사관
# image_path = "lo2.jpg"
#
# ex1.my(image_path)
#
# if cv2.waitKey(0) & 0xFF == ord('q'):
#     cv2.destroyAllWindows()
#
# guri.go(image_path)
#
# #3.분수대
# image_path = "lo4.jpg"
#
# ex1.my(image_path)
#
# if cv2.waitKey(0) & 0xFF == ord('q'):
#     cv2.destroyAllWindows()
#
# guri.go(image_path)
#
#
