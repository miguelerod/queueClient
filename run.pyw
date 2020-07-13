import pymysql

from io import BytesIO
from gtts import gTTS
from pygame import mixer
from time import sleep

OUTPUT_PATH = ".\\multimedia\\audio\\output.mp3"
BELL_PATH = ".\\multimedia\\audio\\aviso.mpeg"
LANG = "es"


def speak(file):
    mixer.init()
    mixer.music.load(file)
    mixer.music.play()
    while mixer.music.get_busy():
        continue


while True:
    db = pymysql.connect(host="165.22.193.102", port=3306, user="root",
                         passwd="251bcf0468f6a63ad84270418534dfea39076f9b1b911744", db="turno")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        "SELECT IDTurno, Number, Position FROM Turnos WHERE Status = 0 ORDER BY IDTurno ASC"
    )
    turn = cursor.fetchone()

    if turn:
        text_to_read = f"Turno número {turn['Number']}, favor pasar a la posición {turn['Position']}"
        sound = gTTS(text=text_to_read, lang=LANG)
        with BytesIO() as stream:
            sound.write_to_fp(stream)
            stream.seek(0)
            print(f"Playing {text_to_read}...")
            speak(BELL_PATH)
            speak(stream)

        cursor.execute(
            f"UPDATE Turnos SET Status = 1 WHERE IDTurno={turn['IDTurno']}"
        )
        print("Updating db...")
        db.commit()

    sleep(5)
