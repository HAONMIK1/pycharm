import cv2
import numpy as np
import math

def calculate_rotation_angle(current_angle, target_angle):
    """
    현재 각도와 쳐다봐야 할 각도가 주어졌을 때, 회전해야 하는 각도를 계산하는 함수

    Args:
        current_angle (float): 현재 각도 (단위: 도)
        target_angle (float): 쳐다봐야 할 각도 (단위: 도)

    Returns:
        float: 회전해야 하는 각도 (단위: 도)
    """
    # 각도의 범위를 0도부터 360도까지로 조정
    current_angle = current_angle % 360
    target_angle = target_angle % 360

    # 회전해야 하는 각도 계산
    rotation_angle = target_angle - current_angle

    # 180도를 넘어가는 경우 반대 방향으로 회전하는 각도로 조정
    if rotation_angle > 180:
        rotation_angle -= 360
    elif rotation_angle < -180:
        rotation_angle += 360

    return rotation_angle


def get_angle(start_x, start_y, target_x, target_y):
    """ 시작점과 목표점의 좌표를 이용하여 방위각을 구하는 함수 """
    dx = target_x - start_x
    dy = target_y - start_y
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    # atan2의 결과는 -pi부터 pi 사이의 값이므로, 각도를 0부터 360도 사이의 값으로 변환
    angle_deg = (angle_deg + 360) % 360
    # 0도가 북쪽이라고 가정하므로, 동쪽일 경우 90도로 변환
    angle_deg = (angle_deg + 90) % 360

    return angle_deg

