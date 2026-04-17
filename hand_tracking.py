import cv2
import mediapipe as mp

class HandTracking:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.mp_draw = mp.solutions.drawing_utils

    def get_data(self):
        success, img = self.cap.read()
        if not success:
            return None, 0

        img = cv2.flip(img, 1)  # mirror cho dễ điều khiển
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = self.hands.process(imgRGB)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            h, w, _ = img.shape

            # ===== LẤY VỊ TRÍ NGÓN TRỎ =====
            x = int(hand.landmark[8].x * w)
            y = int(hand.landmark[8].y * h)

            # ===== ĐẾM NGÓN =====
            fingers = 0

            # 4 ngón (trừ ngón cái)
            tips = [8, 12, 16, 20]

            for tip in tips:
                if hand.landmark[tip].y < hand.landmark[tip - 2].y:
                    fingers += 1

            # ngón cái (x-axis)
            if hand.landmark[4].x > hand.landmark[3].x:
                fingers += 1

            # ===== DEBUG (vẽ tay) =====
            self.mp_draw.draw_landmarks(img, hand, self.mp_hands.HAND_CONNECTIONS)

            # hiển thị camera (debug)
            cv2.imshow("Hand Tracking", img)
            cv2.waitKey(1)

            return (x, y), fingers

        # không thấy tay
        cv2.imshow("Hand Tracking", img)
        cv2.waitKey(1)

        return None, 0

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()