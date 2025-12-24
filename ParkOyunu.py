import cv2
import mediapipe as mp
import numpy as np
import time
import pygame
import os

# =====================
# DOSYA YOLU AYARLARI
# =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def path(file): return os.path.join(BASE_DIR, file)

# =====================
# PYGAME SES AYARLARI
# =====================
pygame.init()
horn_sound = None
try:
    pygame.mixer.init(frequency=22050, size=-16, channels=4, buffer=512)
    engine_sound = pygame.mixer.Sound(path("engine.wav"))
    park_sound   = pygame.mixer.Sound(path("park.wav"))
    error_sound  = pygame.mixer.Sound(path("error.wav"))
    if os.path.exists(path("horn.wav")):
        horn_sound = pygame.mixer.Sound(path("horn.wav"))
        horn_sound.set_volume(0.7)
    
    engine_channel = pygame.mixer.Channel(0)
    fx_channel = pygame.mixer.Channel(1)
    horn_channel = pygame.mixer.Channel(2)
except Exception as e:
    print(f"Ses yukleme uyarisi: {e}")

# =====================
# PNG ÇİZME FONKSİYONU (SABİT DÜZ ÇİZİM)
# =====================
def draw_png_fixed(frame, img, x, y):
    if img is None: return
    h, w = img.shape[:2]
    if x < 0 or y < 0 or x + w > frame.shape[1] or y + h > frame.shape[0]: return
    
    if img.shape[2] == 4:
        alpha = img[:, :, 3] / 255.0
        for c in range(3):
            frame[y:y+h, x:x+w, c] = (alpha * img[:, :, c] + (1 - alpha) * frame[y:y+h, x:x+w, c])
    else: 
        frame[y:y+h, x:x+w] = img[:, :, :3]

# =====================
# MEDIAPIPE AYARLARI
# =====================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, model_complexity=0, min_detection_confidence=0.4, min_tracking_confidence=0.4)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

car_size = (100, 60)
car_img = cv2.imread(path("car.png"), cv2.IMREAD_UNCHANGED)
if car_img is not None: car_img = cv2.resize(car_img, car_size)

# =====================
# OYUN NESNELERİ
# =====================
def create_game_objects():
    cars, parks = [], []
    for i in range(5):
        cars.append({"id": i+1, "start_x": 50, "start_y": 80+i*110, "x": 50, "y": 80+i*110, "hold": False, "parked": False})
        parks.append({"id": i+1, "x": 1000, "y": 80+i*110})
    return cars, parks

cars, parks = create_game_objects()
score, selected_car, game_time, game_over, win = 0, None, 60, False, False
start_time = time.time()

# =====================
# ANA DÖNGÜ
# =====================
while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)
    h_f, w_f, _ = frame.shape
    
    # Oyun Durum Kontrolü
    if not game_over:
        remaining = max(0, game_time - int(time.time() - start_time))
        
        # TÜM ARAÇLAR PARK EDİLDİ Mİ? (Kazanma Kontrolü)
        all_parked = all(car["parked"] for car in cars)
        
        if all_parked:
            win = True
            game_over = True
        elif remaining == 0:
            game_over = True
    else:
        # Oyun bittiğinde süreyi dondur
        remaining = remaining

    finger_x, finger_y = None, None
    num_fingers = 0

    if not game_over:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)
        
        if result.multi_hand_landmarks:
            hand_lms = result.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, hand_lms, mp_hands.HAND_CONNECTIONS)
            
            # Parmak sayma
            fingers = []
            if abs(hand_lms.landmark[4].x - hand_lms.landmark[17].x) > abs(hand_lms.landmark[3].x - hand_lms.landmark[17].x):
                fingers.append(1)
            for tip in [8, 12, 16, 20]:
                if hand_lms.landmark[tip].y < hand_lms.landmark[tip-2].y: fingers.append(1)
            num_fingers = len(fingers)
            
            finger_x = int(hand_lms.landmark[8].x * w_f)
            finger_y = int(hand_lms.landmark[8].y * h_f)

            if num_fingers == 5 and horn_sound and not horn_channel.get_busy():
                horn_channel.play(horn_sound)

    # SÜRÜŞ MANTIĞI
    if finger_x and finger_y and not game_over:
        if selected_car is None:
            for car in cars:
                if not car["parked"] and car["x"] < finger_x < car["x"]+car_size[0] and car["y"] < finger_y < car["y"]+car_size[1]:
                    selected_car = car
                    car["hold"] = True
                    try: engine_channel.play(engine_sound, -1)
                    except: pass
                    break
        
        if selected_car and selected_car["hold"]:
            selected_car["x"], selected_car["y"] = finger_x - 50, finger_y - 30
            for park in parks:
                if park["x"] < selected_car["x"] < park["x"]+120 and park["y"] < selected_car["y"] < park["y"]+70:
                    if park["id"] == selected_car["id"]:
                        score += 10
                        selected_car["parked"] = True
                        try: fx_channel.play(park_sound)
                        except: pass
                    else:
                        selected_car["x"], selected_car["y"] = selected_car["start_x"], selected_car["start_y"]
                        try: fx_channel.play(error_sound)
                        except: pass
                    selected_car["hold"], selected_car = False, None
                    try: engine_channel.stop()
                    except: pass
                    break

    # EKRAN ÇİZİMLERİ
    for park in parks:
        cv2.rectangle(frame, (park["x"], park["y"]), (park["x"]+120, park["y"]+70), (255, 0, 0), 2)
    for car in cars:
        draw_png_fixed(frame, car_img, car["x"], car["y"])

    cv2.putText(frame, f"SKOR: {score}  SURE: {remaining}", (50, 50), 1, 2, (0, 255, 255), 2)

    # OYUN SONU EKRANI (TEBRİKLER MESAJI)
    if win:
        # Yeşil bir tebrik kutusu çiz
        cv2.rectangle(frame, (250, 250), (1030, 470), (0, 150, 0), -1) # Arka plan
        cv2.rectangle(frame, (250, 250), (1030, 470), (255, 255, 255), 4) # Çerçeve
        cv2.putText(frame, "TEBRIKLER!", (500, 320), 1, 3, (255, 255, 255), 4)
        cv2.putText(frame, "TUM ARACLAR PARK EDILDI", (330, 380), 1, 2, (255, 255, 255), 3)
        cv2.putText(frame, "TEKRAR ICIN 'R'YE BASIN", (420, 430), 1, 1.5, (200, 200, 200), 2)
    elif game_over:
        # Süre biterse çıkan kırmızı ekran
        cv2.putText(frame, "SURE BITTI! OYUN BITTI", (380, 360), 1, 3, (0, 0, 255), 4)
        cv2.putText(frame, "TEKRAR ICIN 'R'", (530, 420), 1, 2, (255, 255, 255), 2)

    cv2.imshow("Park Etme Oyunu - Final", frame)
    
    key = cv2.waitKey(1)
    if key == 27: break
    if key == ord('r'): 
        cars, parks = create_game_objects()
        score, selected_car, game_over, win, start_time = 0, None, False, False, time.time()

cap.release()
cv2.destroyAllWindows()
pygame.quit()