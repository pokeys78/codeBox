
import cv2
import numpy as np

cap = cv2.VideoCapture(0)  # 카메라 사용

goal_line_position = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 화면의 중앙을 골라인으로 설정
    if goal_line_position is None:
        height, width = frame.shape[:2]
        goal_line_position = width // 2

    # BGR에서 HSV로 컬러스페이스 변환
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 파란색의 HSV 범위 정의
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])

    # 파란색 범위 내의 픽셀에 대한 마스크 생성
    blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)

    # 객체의 윤곽 찾기
    contours, _ = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # 간단한 크기 필터링
        if cv2.contourArea(contour) > 1000:
            x, y, w, h = cv2.boundingRect(contour)

            # 객체가 골라인 오른쪽에 위치하는지 확인
            if x > goal_line_position:
                print("골!")
            else:
                print("    ")

            break  # 하나의 객체만 판단

    # 골라인 그리기 (흰색, 두께 30)
    cv2.line(frame, (goal_line_position, 0), (goal_line_position, height), (255, 255, 255), 30)

    # 결과 표시
    cv2.imshow("Frame", frame)
    cv2.imshow("Blue Mask", blue_mask)

    key = cv2.waitKey(1)
    if key == 27:  # ESC 키를 누르면 종료
        break

cap.release()
cv2.destroyAllWindows()

