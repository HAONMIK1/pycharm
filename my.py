import cv2
import numpy as np

def my(image_path):
    # 이미지 읽어오기

    img1 = cv2.imread('map.jpg')
    img2 = cv2.imread(image_path)

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
    good_matches = matches[:40]

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
    dst_x = dst[:,:,0].mean()
    dst_y = dst[:,:,1].mean()

    # 가운데 좌표값을 지도 이미지에 표시
    cv2.circle(img1, (int(dst_x), int(dst_y)), 10, (0, 0, 255), -1)

    # 좌표값도 함께 출력
    cv2.putText(img1, f"({int(dst_x)}, {int(dst_y)})", (int(dst_x), int(dst_y) - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # 결과 출력
    cv2.imshow('result', result)
    key = cv2.waitKey()
    if key == 27:
        cv2.imshow('map with center', img1)
        cv2.waitKey()
