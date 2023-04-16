import cv2
import math

import numpy as np

# 사용자 위치 좌표와 바라보는 방향의 각도
user_location = (200, 200)
user_direction = 90  # 북동쪽을 기준으로 시계방향으로 회전한 각도

# map 이미지 파일 로드
map_img = cv2.imread('map.jpg')

# 사용자 위치 좌표와 바라보는 방향 시각화
cv2.circle(map_img, user_location, 5, (0, 0, 255), -1)
cv2.arrowedLine(map_img, user_location, (user_location[0]+int(50*math.cos(math.radians(user_direction))),
                                          user_location[1]+int(50*math.sin(math.radians(user_direction)))),
                (0, 255, 0), thickness=2, tipLength=0.3)

# 마우스 이벤트 콜백 함수 정의
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # 클릭한 위치 좌표
        click_location = (x, y)

        # 1. 사용자 위치 좌표와 클릭한 위치 좌표를 연결하는 벡터를 계산
        dx = click_location[0] - user_location[0]
        dy = click_location[1] - user_location[1]

        # 2. 이 벡터의 방향각을 계산
        angle = math.degrees(math.atan2(dy, dx))
        if angle < 0:
            angle += 360

        # 3. 사용자 위치에서 바라보는 방향과 벡터의 방향을 비교하여 회전 각도를 계산
        rotate_angle = angle - user_direction
        if rotate_angle > 180:
            rotate_angle -= 360
        elif rotate_angle < -180:
            rotate_angle += 360

        # 클릭한 위치와 회전각도 시각화
        cv2.circle(map_img, click_location, 5, (255, 0, 0), -1)
        cv2.putText(map_img, f'{rotate_angle:2.0f}\'C', click_location, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.arrowedLine(map_img, user_location, (user_location[0]+dx, user_location[1]+dy),
                        (255, 0, 0), thickness=2, tipLength=0.3)
        cv2.arrowedLine(map_img, (user_location[0]+dx, user_location[1]+dy), click_location,
                        (0, 0, 255), thickness=2, tipLength=0.3)

        # 결과 이미지 파일 화면에 출력
        cv2.imshow('Result', map_img)
   # 이미지 읽어오기
    img1 = cv2.imread('map.jpg')
    img2 = cv2.imread(image_path)

    # 이미지 축척
    width_m = 625.64  # 가로길이 (m)
    height_m = 352.79  # 세로길이 (m)

    # 이미지의 해상도 추출 height 세로 width 가로
    height, width = img1.shape[:2]
    pixel_length = width_m / width


    # SIFT 검출기 생성
    sift = cv2.SIFT_create()

    # 특징점 검출 및 기술자 계산
    kp1, des1 = sift.detectAndCompute(cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY), None)
    kp2, des2 = sift.detectAndCompute(cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY), None)

    # BFMatcher 객체 생성 및 매칭 수행
    bf = cv2.BFMatcher()
    matches = bf.match(des1, des2)

    # 매칭 결과를 거리 기준으로 오름차순 정렬
    matches = sorted(matches, key=lambda x: x.distance)

    # 좋은 매칭 결과만 선택
    good_matches = matches[:30]

    # 좋은 매칭 결과 시각화
    result = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None, flags=2)

    # 좋은 매칭 결과 중심 좌표 계산
    points1 = np.zeros((len(good_matches), 2), dtype=np.float32)
    points2 = np.zeros((len(good_matches), 2), dtype=np.float32)
    for i, match in enumerate(good_matches):
        points1[i, :] = kp1[match.queryIdx].pt
        points2[i, :] = kp2[match.trainIdx].pt
    M, _ = cv2.findHomography(points2, points1, cv2.RANSAC, 5.0)
    h, w, _ = img2.shape
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)
    dst_x = dst[:, :, 0].mean()
    dst_y = dst[:, :, 1].mean()

    # 가운데 좌표값을 지도 이미지에 표시
    cv2.circle(img1, (int(dst_x), int(dst_y)), 10, (0, 0, 255), -1)

    # 좌표값도 함께 출력
    cv2.putText(img1, f"({int(dst_x)}, {int(dst_y)})", (int(dst_x), int(dst_y) - 20), cv2.FONT_HERSHEY_SIMPLEX, 1,
            (0, 0, 255), 2)

    # 결과 출력
   # cv2.imshow('result', result)
   # cv2.namedWindow('map with center', cv2.WINDOW_NORMAL)
    cv2.imshow('map with center', img1)

    # 창 크기 조절
    # cv2.resizeWindow('map with center', 1800, 1200)

    # 마우스 이벤트 캡처 함수 등록
    cv2.setMouseCallback('map with center', mouse_callback, img1)

    # 종료
    key = cv2.waitKey()