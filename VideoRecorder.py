import datetime
import enum
import os
import cv2 as cv


class State(enum.Enum):
    neutral = 0
    start = 1
    pause = 2
    Continue = 3
    stop = 4


if __name__ == '__main__':
    cam = cv.VideoCapture(0)

    frame_width = int(cam.get(3))
    frame_height = int(cam.get(4))
    frames = []
    resolution = (frame_width, frame_height)

    fourcc = cv.VideoWriter_fourcc(*'MJPG')
    current_state = State.neutral
    print('Ready to record...')
    cv.namedWindow('Recorder')
    file_name = None

    while cam.isOpened():
        key = cv.waitKey(1) & 0xFF
        ret, frame = cam.read()
        if not ret:
            break

        if key == 27 or not cv.getWindowProperty('Recorder', cv.WND_PROP_VISIBLE):
            break
        elif current_state == State.neutral and file_name is None:
            current_time = datetime.datetime.now()
            file_name = current_time.strftime(
                f'Recording %Y-%m-%d 0{current_time.hour * 3600 + current_time.minute * 60 + current_time.second}.avi')
        elif current_state == State.neutral and key == ord('s'):
            current_state = State.start
            print('Recording started...')
        elif (current_state == State.start or current_state == State.Continue) and key == ord('p'):
            current_state = State.pause
            print('Recording paused...')
        elif (current_state == State.start or current_state == State.Continue or current_state == State.pause) and key == ord('e'):
            current_state = State.stop
            print('Recording stopped...')
        elif current_state == State.pause and key == ord('c'):
            current_state = State.Continue
            print('Recording continued...')
        elif current_state == State.start or current_state == State.Continue:
            frames.append(frame)
        elif current_state == State.stop:
            os.makedirs('Recordings', exist_ok=True)
            file = cv.VideoWriter(f'Recordings/{file_name}', fourcc, 30.0, resolution)

            for frame in frames:
                file.write(frame)
            frames.clear()
            file.release()
            file_name = None

            current_state = State.neutral
            print('Ready to record...')

        cv.imshow('Recorder', frame)

    cam.release()
    cv.destroyAllWindows()
