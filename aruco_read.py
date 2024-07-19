from __future__ import print_function
import cv2

class ArucoMarkerDetector:
    def __init__(self, dictionary="DICT_ARUCO_ORIGINAL"):
        self.desired_aruco_dictionary = dictionary
        self.ARUCO_DICT = {
            "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
            "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
            "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
            "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
            "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
            "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
            "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
            "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
            "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
            "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
            "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
            "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
            "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
            "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
            "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
            "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
            "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL
        }
        self.this_aruco_dictionary = cv2.aruco.getPredefinedDictionary(self.ARUCO_DICT[self.desired_aruco_dictionary])
        self.this_aruco_parameters = cv2.aruco.DetectorParameters()
        self.arucoID = None

    def detect_markers(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()

            if not ret:
                print("[ERROR] Failed to capture frame.")
                break

            corners, ids, rejected = cv2.aruco.detectMarkers(frame, self.this_aruco_dictionary, parameters=self.this_aruco_parameters)

            detected_ids = []

            if ids is not None and len(ids) > 0:
                ids = ids.flatten()

                for (marker_corner, marker_id) in zip(corners, ids):
                    corners = marker_corner.reshape((4, 2))
                    top_left, top_right, bottom_right, bottom_left = corners

                    top_right = (int(top_right[0]), int(top_right[1]))
                    bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
                    bottom_left = (int(bottom_left[0]), int(bottom_left[1]))
                    top_left = (int(top_left[0]), int(top_left[1]))

                    cv2.line(frame, top_left, top_right, (0, 255, 0), 2)
                    cv2.line(frame, top_right, bottom_right, (0, 255, 0), 2)
                    cv2.line(frame, bottom_right, bottom_left, (0, 255, 0), 2)
                    cv2.line(frame, bottom_left, top_left, (0, 255, 0), 2)

                    center_x = int((top_left[0] + bottom_right[0]) / 2.0)
                    center_y = int((top_left[1] + bottom_right[1]) / 2.0)
                    cv2.circle(frame, (center_x, center_y), 4, (0, 0, 255), -1)

                    cv2.putText(frame, str(marker_id),
                                (top_left[0], top_left[1] - 15),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 255, 0), 2)

                self.arucoID = marker_id 
                # print(self.arucoID)

            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def run(self):
        self.detect_markers()