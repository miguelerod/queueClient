import pymysql
from gtts import gTTS
from playsound import playsound
from time import sleep
from os import remove

OUTPUT_PATH = ".\\multimedia\\audio\\output.mp3"
LANG = "es"

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
        sound.save(OUTPUT_PATH)

        playsound(OUTPUT_PATH)

        cursor.execute(
            f"UPDATE Turnos SET Status = 1 WHERE IDTurno={turn['IDTurno']}"
        )
        db.commit()
        remove(OUTPUT_PATH)

    sleep(5)
