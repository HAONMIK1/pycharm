from module import *
def go(lo,gak):
    # 마우스 클릭 이벤트 핸들러 함수
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print('Mouse clicked at: ', x, y)
        # 두 점의 좌표값 차이 계산 및 출력
            diff_x = x - int(dst_x)
            diff_y = y - int(dst_y)

        # 각도 예시 입력값
            current_angle = gak
            target_angle = get_angle(int(dst_x), int(dst_y), x, y)
            print("목표점의 각도:", target_angle, "도")
            angle_rad = math.radians(current_angle)
            pt2 = (int(dst_x + 50 * math.sin(angle_rad)),
                   int(dst_y - 50 * math.cos(angle_rad)))

        # 회전해야 하는 각도 계산
            rotation_angle = calculate_rotation_angle(current_angle, target_angle)
            print("회전해야 하는 각도:", rotation_angle, "도")

        # 클릭한 좌표에 원과 텍스트 그리기
            cv2.circle(img1, (x, y), 5, (0, 0, 255), -1)
            cv2.putText(img1, f'({x}, {y})', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            cv2.arrowedLine(img1, pt1, pt2, (0, 255, 0), thickness=2, tipLength=0.3)
        # 거리 구하기
            distans = math.sqrt(diff_x ** 2 + diff_y ** 2) * pixel_length

        # 좌표 사이에 선 그리기
            cv2.arrowedLine(img1, (int(dst_x), int(dst_y)), (x, y), (0, 255, 0), 2)
            cv2.putText(img1, f'({int(distans)}M)', (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 100, 0), 2)
            cv2.putText(img1, f'({int(target_angle)}C)', (x, y - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 100, 100), 2)

        # 창 새로고침
            cv2.imshow('map with center', img1)


# 이미지 읽어오기

    img1 = cv2.imread('map.jpg')
    img2 = cv2.imread(lo)

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
    pt1 = (int(dst_x), int(dst_y))

# 가운데 좌표값을 지도 이미지에 표시
    cv2.circle(img1, (int(dst_x), int(dst_y)), 10, (0, 0, 255), -1)

# 좌표값도 함께 출력
    cv2.putText(img1, f"({int(dst_x)}, {int(dst_y)})", (int(dst_x), int(dst_y) - 20), cv2.FONT_HERSHEY_SIMPLEX, 1,
            (0, 0, 255), 2)

# 종료
    cv2.imshow('result', result)
    key = cv2.waitKey()
    if key == 27:
        cv2.imshow('map with center', img1)
        cv2.setMouseCallback('map with center', mouse_callback, img1)
        cv2.waitKey()

