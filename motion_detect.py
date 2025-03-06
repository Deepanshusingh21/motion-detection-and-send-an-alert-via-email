import cv2
import smtplib
from email.mime.text import MIMEText

def send_alert():
    sender_email = "deepanshusingh9918@gmail.com"
    receiver_email = "singhdeepanshu979@gmail.com"
    password = ""
    
    msg = MIMEText("Motion detected! Check your AI Camera system.")
    msg['Subject'] = "AI Camera Alert"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Alert email sent!")
    except Exception as e:
        print("Error sending email:", e)

def motion_alert():
    cap = cv2.VideoCapture(0)
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    
    while cap.isOpened():
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            if cv2.contourArea(contour) < 5000:
                continue
            send_alert()
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        cv2.imshow("Motion Detector", frame1)
        frame1 = frame2
        ret, frame2 = cap.read()
        
        if cv2.waitKey(10) == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    motion_alert()
