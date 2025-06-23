import datetime

from fastapi import FastAPI

app = FastAPI()


day_to_word_map = {
    0:"Хорошего понедельника",
    1:"Хорошего вторника",
    2:"Хорошей среды",
    3:"Хорошего четверга",
    4:"Хорошей пятницы",
    5:"Хорошей субботы",
    6:"Хорошего воскресенья",
}


@app.get("/hello_world/{username}")
def hello_world(username: str):
    cur_day = datetime.datetime.today().weekday()
    greetings = day_to_word_map[cur_day]
    return f"Привет {username}. {greetings}"