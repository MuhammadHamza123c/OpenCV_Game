import mediapipe as mp
import time
import cv2
import random

def rock(handy):
    thumb_top = handy.landmark[4].x
    thumb_pitch = handy.landmark[2].x
    index_top = handy.landmark[8].y
    index_down = handy.landmark[6].y
    middle_top = handy.landmark[12].y
    middle_down = handy.landmark[10].y
    ring_top = handy.landmark[16].y
    ring_down = handy.landmark[14].y
    small_top = handy.landmark[20].y
    small_down = handy.landmark[18].y
    return (thumb_top < thumb_pitch and index_top > index_down and 
            middle_top > middle_down and ring_top > ring_down and 
            small_top > small_down)

def scissor(handy):
    thumb_top = handy.landmark[4].x
    thumb_pitch = handy.landmark[2].x
    index_top = handy.landmark[8].y
    index_down = handy.landmark[6].y
    middle_top = handy.landmark[12].y
    middle_down = handy.landmark[10].y
    ring_top = handy.landmark[16].y
    ring_down = handy.landmark[14].y
    small_top = handy.landmark[20].y
    small_down = handy.landmark[18].y
    return (thumb_pitch > thumb_top and index_top < index_down and 
            middle_top < middle_down and ring_top > ring_down and 
            small_top > small_down)

def paper(handy):
    index_top = handy.landmark[8].y
    index_down = handy.landmark[6].y
    middle_top = handy.landmark[12].y
    middle_down = handy.landmark[10].y
    ring_top = handy.landmark[16].y
    ring_down = handy.landmark[14].y
    small_top = handy.landmark[20].y
    small_down = handy.landmark[18].y
    return (index_top < index_down and middle_top < middle_down and 
            ring_top < ring_down and small_top < small_down)

def computer_move():
    return random.choice(['rock', 'paper', 'scissor'])

# Score initialization
user_score = 0
computer_score = 0

# Mediapipe setup
mp_hand = mp.solutions.hands
Hands = mp_hand.Hands()
draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = Hands.process(rgb)

    if result.multi_hand_landmarks:
        for handy in result.multi_hand_landmarks:
            draw.draw_landmarks(frame, handy, mp_hand.HAND_CONNECTIONS)

            move = ""
            if rock(handy):
                move = "rock"
            elif paper(handy):
                move = "paper"
            elif scissor(handy):
                move = "scissor"

            if move:
                opponent = computer_move()
                print(f"User: {move} | Computer: {opponent}")

                if move == opponent:
                    print("It's a tie!")
                elif (move == "rock" and opponent == "scissor") or \
                     (move == "paper" and opponent == "rock") or \
                     (move == "scissor" and opponent == "paper"):
                    user_score += 1
                    print("User Beat ✅")
                else:
                    computer_score += 1
                    print("Computer Beat ✅")
                
                print(f"User Score: {user_score} | Computer Score: {computer_score}")
                time.sleep(3)  # Wait before next move

    cv2.imshow("Rock Paper Scissor", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Final Scores:")
        print(f"User Score: {user_score}")
        print(f"Computer Score: {computer_score}")
        break

cap.release()
cv2.destroyAllWindows()
