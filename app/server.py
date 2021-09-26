import flask
from flask import Flask
from typing import NamedTuple

from utils import db


app = Flask(__name__)


class ResultPoll(NamedTuple):
    choice: str
    voice: int


@app.route('/api/createPoll/', methods=['POST', 'GET'])
def create_poll():
    new_poll_data_json = flask.request.json
    title = new_poll_data_json["poll"]
    choices = [new_poll_data_json["choices"][key] for key in new_poll_data_json["choices"]]

    if title and choices:
        db.create_poll(title)
        poll_id = db.know_poll_id(title)

        for number in range(len(choices)):
            db.add_choice(*poll_id, choices[number])
        return 'Голосование успешно создано'
    return 'Недостаточно данных'


@app.route('/api/poll/', methods=['POST', 'GET'])
def get_poll():
    poll_choice_data_json = flask.request.json
    poll_id = int(poll_choice_data_json["poll_id"])
    choice = poll_choice_data_json["choice"]
    polling = db.get_poll(poll_id, choice)
    return polling


@app.route('/api/getResult/', methods=['POST', 'GET'])
def view_result():
    poll_data = flask.request.json
    poll = poll_data["poll"]
    list_poll_data = db.poll_result(poll)
    poll_data = list_poll_data[0]
    choices_data = list_poll_data[1]
    all_choices = format_(choices_data)

    output = [f'Вариант: {data.choice}, Количество голосов: {data.voice}' for data in all_choices]
    return f'Голосование: {poll_data[1]}\n\n' + "\n".join(output)


def format_(choice_data: list):
    all_choices = [ResultPoll(choice=tuple_choice_data[0], voice=tuple_choice_data[1], )
                   for tuple_choice_data in choice_data]
    return all_choices


if __name__ == '__main__':
    app.run(port=8000)
