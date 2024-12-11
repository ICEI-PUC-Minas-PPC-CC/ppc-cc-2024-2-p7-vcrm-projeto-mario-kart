import cv2
import mediapipe as mp
import numpy as np
import json
from pynput.keyboard import Key, Controller, KeyCode

# carregar configuracoes do arquivo json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# mapear as teclas para as acoes
key_mapping = {
    "steer_left": getattr(Key, config["keys"]["steer_left"], KeyCode(char=config["keys"]["steer_left"])),
    "steer_right": getattr(Key, config["keys"]["steer_right"], KeyCode(char=config["keys"]["steer_right"])),
    "accelerate": getattr(Key, config["keys"]["accelerate"], KeyCode(char=config["keys"]["accelerate"])),
    "brake": getattr(Key, config["keys"]["brake"], KeyCode(char=config["keys"]["brake"])),
    "use_item": getattr(Key, config["keys"]["use_item"], KeyCode(char=config["keys"]["use_item"]))
}

# inicializacao
keyboard = Controller()
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)
screen_width = 640
screen_height = 480
is_accelerating = False

def calculate_steering_angle(hand_landmarks_list):
    # verifica se ha duas maos detectadas
    if len(hand_landmarks_list) != 2:
        keyboard.release(key_mapping["steer_left"])
        keyboard.release(key_mapping["steer_right"])
        return
    
    left_hand = None
    right_hand = None
    
    # determina qual mao e a esquerda e qual e a direita
    for hand_landmarks in hand_landmarks_list:
        palm_x = hand_landmarks.landmark[9].x
        
        if left_hand is None:
            left_hand = (palm_x, hand_landmarks)
        else:
            if palm_x < left_hand[0]:
                right_hand = left_hand
                left_hand = (palm_x, hand_landmarks)
            else:
                right_hand = (palm_x, hand_landmarks)
    
    # se nao houver duas maos, libera as teclas de direcao
    if left_hand is None or right_hand is None:
        keyboard.release(key_mapping["steer_left"])
        keyboard.release(key_mapping["steer_right"])
        return
    
    # calcula o angulo entre as maos
    angle = np.arctan2(
        right_hand[1].landmark[9].y - left_hand[1].landmark[9].y,
        right_hand[1].landmark[9].x - left_hand[1].landmark[9].x
    )
    angle_degrees = np.degrees(angle)
    
    # determina a direcao com base no angulo
    if angle_degrees < -10:
        keyboard.press(key_mapping["steer_right"])
        keyboard.release(key_mapping["steer_left"])
    elif angle_degrees > 10:
        keyboard.press(key_mapping["steer_left"])
        keyboard.release(key_mapping["steer_right"])
    else:
        keyboard.release(key_mapping["steer_left"])
        keyboard.release(key_mapping["steer_right"])
    
    keyboard.release(key_mapping["brake"])

def detect_palm_acceleration(hand_landmarks_list):
    global is_accelerating
    
    # verifica se ha maos detectadas
    if not hand_landmarks_list:
        return
        
    hand = hand_landmarks_list[0]

    # verifica se todos os dedos estao estendidos
    fingers_extended = all(
        hand.landmark[tip].y < hand.landmark[base].y 
        for tip, base in [(8,5), (12,9), (16,13), (20,17)]
    )
    
    # se os dedos estiverem estendidos, ativa a aceleracao
    if fingers_extended:
        is_accelerating = True
    
    if is_accelerating:
        keyboard.press(key_mapping["accelerate"])

def handle_braking_and_item(image):
    # converte a imagem para rgb
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)
    
    # verifica se ha deteccao de rosto
    if not results.multi_face_landmarks:
        keyboard.release(key_mapping["use_item"])
        keyboard.release(key_mapping["brake"])
        return
    
    face_landmarks = results.multi_face_landmarks[0]
    
    # calcula a inclinacao da cabeca
    nose_tip = face_landmarks.landmark[4]
    chin = face_landmarks.landmark[152]
    forehead = face_landmarks.landmark[10]
    
    head_tilt = (nose_tip.y - forehead.y) / (chin.y - forehead.y)
    
    # se a cabeca estiver inclinada para baixo, aciona o freio
    if head_tilt < 0.35:
        keyboard.press(key_mapping["brake"])
    else:
        keyboard.release(key_mapping["brake"])
    
    # calcula a rotacao da cabeca
    left_ear = face_landmarks.landmark[234]
    right_ear = face_landmarks.landmark[454]
    head_rotation = abs((nose_tip.x - left_ear.x) / (right_ear.x - left_ear.x) - 0.5)
    
    # se a cabeca estiver rotacionada, aciona o uso de item
    if head_rotation > 0.3:
        keyboard.press(key_mapping["use_item"])

def main():
    # loop principal para capturar e processar a imagem
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        hand_results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # desenha as marcacoes das maos na imagem
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            calculate_steering_angle(hand_results.multi_hand_landmarks)
            detect_palm_acceleration(hand_results.multi_hand_landmarks)
        
        handle_braking_and_item(image)

        # exibe a imagem com as marcacoes
        cv2.imshow('Gesture Control', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
