import cv2
from ultralytics import YOLO

def start_eye_scan():
    # بارگذاری مدل آماده YOLO برای تشخیص ۸۰ نوع شیء مختلف از جمله انسان
    model = YOLO("yolov8n.pt") 
    
    # اتصال به دوربین پیش‌فرض (کد 0)
    cap = cv2.VideoCapture(0)
    
    print("[INFO] سیستم بینایی برادر چشمی فعال شد...")
    
    while True:
        success, img = cap.read()
        if not success:
            break
            
        # پردازش تصویر و تشخیص اشیاء
        results = model(img, stream=True)
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # به دست آوردن مختصات جعبه دور شیء
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                
                # مشخص کردن نام کلاس (مثلاً person, laptop, cell phone)
                cls = int(box.cls[0])
                class_name = model.names[cls]
                conf = round(float(box.conf[0]), 2)
                
                # رسم جعبه سایبرنتیک دور شیء شناسایی شده
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, f"{class_name} {conf}", (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # نمایش خروجی مانیتورینگ
        cv2.imshow("Brother Eye - Tactical Vision", img)
        
        # خروج از برنامه با فشردن کلید q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_eye_scan()
