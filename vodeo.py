import cv2


def play_video(start_time, end_time):
    cap = cv2.VideoCapture("video.mp4")
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    start_frame = int(start_time * frame_rate)
    end_frame = int(end_time * frame_rate)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            if current_frame > end_frame:
                break
            cv2.imshow('Video', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()



