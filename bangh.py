import cv2
import math

# 내 위치 좌표와 바라보는 방향의 각도
my_location = (dst_x, dst_y)
my_direction = 90  # 동쪽을 기준으로 시계방향으로 회전한 각도

# 목적지 위치 좌표
destination = (mouse_callback.x, mouse_callback.y)


# 내 위치 좌표와 바라보는 방향 시각화
cv2.circle(img1, my_location, 5, (0, 0, 255), -1)
cv2.arrowedLine(img1, my_location, (my_location[0]+int(50*math.cos(math.radians(my_direction))),
                                        my_location[1]+int(50*math.sin(math.radians(my_direction)))),
                (0, 255, 0), thickness=2, tipLength=0.3)

# 1. 내 위치 좌표와 목적지 위치 좌표를 연결하는 벡터를 계산
dx = destination[0] - my_location[0]
dy = destination[1] - my_location[1]

# 2. 이 벡터의 방향각을 계산
angle = math.degrees(math.atan2(dy, dx))
if angle < 0:
    angle += 360

# 3. 내 위치에서 바라보는 방향과 벡터의 방향을 비교하여 회전 각도를 계산
rotate_angle = angle - my_direction
if rotate_angle > 180:
    rotate_angle -= 360
elif rotate_angle < -180:
    rotate_angle += 360

# 목적지 위치와 회전각도 시각화
cv2.circle(img1, destination, 5, (255, 0, 0), -1)
cv2.putText(img1, f'{rotate_angle:2.0f}\'C', destination, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
cv2.arrowedLine(img1, my_location, (my_location[0]+dx, my_location[1]+dy),
                (255, 0, 0), thickness=2, tipLength=0.3)
cv2.arrowedLine(img1, (my_location[0]+dx, my_location[1]+dy), destination,
                (0, 0, 255), thickness=2, tipLength=0.3)


