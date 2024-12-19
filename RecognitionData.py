import cv2
import numpy as np
from PIL import Image
import queryDB as db
from gtts import gTTS
import os
# Khởi tạo webcam và đặt độ phân giải của nó thành 900x720
cam = cv2.VideoCapture(0)
cam.set(3, 900)
cam.set(4, 720)
# Khởi tạo một đối tượng CascadeClassifier trong thư viện OpenCV
# với tệp tin XML chứa thông tin về mô hình Cascade để phát hiện khuôn mặt trên hình ảnh đầu vào
face_cascade = cv2.CascadeClassifier("libs/haarcascade_frontalface_default.xml")
# Tạo ra một đối tượng nhận dạng khuôn mặt bằng thuật toán LBPH
recognizer = cv2.face.LBPHFaceRecognizer_create()
# Dùng để đọc dữ liệu được huấn luyện từ tệp
recognizer.read('recognizer/trainningData.yml')
fontface = cv2.FONT_HERSHEY_SIMPLEX

# Vòng lặp vô hạn để lấy liên tục hình ảnh từ camera.
while True:
    ret, frame = cam.read()# cam.read() là hàm để đọc hình ảnh từ camera và lưu trữ vào biến frame.
    # Chuyển đổi hình ảnh màu sang độ xám để đơn giản hóa trong việc phát hiện khuôn mặt
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)

    for (x, y, w, h) in faces:
        # Vẽ một hình chữ nhật xung quanh khuôn mặt được phát hiện
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Thực hiện nhận diện khuôn mặt và xác định người đó bằng
        # cách so sánh khuôn mặt được phát hiện từ cam với các khuôn mặt được train trước đó.
        roi_gray = gray[y:y + h, x:x + w]
        # Kết quả này trả về là id và confidence -> độ tin cậy
        id, confidence = recognizer.predict(roi_gray)
        if confidence < 40:
            profile = db.getProfile(id)# Gọi đến hàm getProfile để lấy thông tin
            # Nếu profile mà không bằng rỗng thì hiển thị tên
            if profile is not None:
                # Hiển thị ra tên trong khung cam
                cv2.putText(frame, "" + str(profile[1]), (x + 10, y + h + 30),
                            fontface, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Unknown", (x + 10, y + h + 30), fontface,
                        1, (0, 0, 255), 2)
    cv2.imshow("Nhận Diện Khuôn Mặt", frame)
    if cv2.waitKey(1) == ord('q'):
        break

print("\nThoát...")
cam.release()
cv2.destroyAllWindows()
