import cv2
import face_recognition
import os

def start_eye_scan():
    print("[INFO] در حال بارگذاری داده‌های چهره اپراتور...")
    
    # مسیر عکس خودتان را مشخص کنید
    known_image_path = "faces/operator.jpg"
    
    if not os.path.exists(known_image_path):
        print("[ERROR] عکس operator.jpg در پوشه faces پیدا نشد!")
        return

    # بارگذاری و رمزگذاری (Encoding) چهره شما
    known_image = face_recognition.load_image_file(known_image_path)
    try:
        known_face_encoding = face_recognition.face_encodings(known_image)[0]
    except IndexError:
        print("[ERROR] هوش مصنوعی نتوانست چهره‌ای در عکس operator.jpg پیدا کند. عکس واضح‌تری بگذارید.")
        return

    # تعریف لیست چهره‌های شناخته شده
    known_face_encodings = [known_face_encoding]
    known_face_names = ["Operator (Authorized)"]

    # فعال‌سازی دوربین
    cap = cv2.VideoCapture(0)
    print("[INFO] سیستم اسکن چهره برادر چشمی فعال شد...")

    while True:
        success, frame = cap.read()
        if not success:
            break

        # کوچک کردن تصویر برای پردازش سریع‌تر سیستم
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # تبدیل رنگ تصویر به RGB (مناسب برای کتابخانه face_recognition)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # پیدا کردن تمام چهره‌ها در فریم فعلی دوربین
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            # مقایسه چهره جلوی دوربین با عکس شما
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            name = "Unknown Subject (Target)"
            color = (0, 0, 255) # رنگ قرمز برای غریبه‌ها

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                color = (0, 255, 0) # رنگ سبز برای شما (اپراتور)

            # بازگرداندن مختصات چهره به اندازه واقعی
            top, right, bottom, left = face_location
            top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4

            # رسم باکس سایبرنتیک دور چهره
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        # نمایش پنجره مانیتورینگ
        cv2.imshow("Brother Eye - Facial Recognition OS", frame)

        # خروج با کلید q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_eye_scan()
