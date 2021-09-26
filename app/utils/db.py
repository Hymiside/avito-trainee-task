import sqlite3

conn = sqlite3.connect('utils/service.db', check_same_thread=False)
cursor = conn.cursor()


def create_poll(poll_: str):
    cursor.execute("INSERT INTO polls(poll) VALUES(?);", (poll_,))
    conn.commit()


def know_poll_id(poll_: str):
    poll_id = [id_ for id_ in cursor.execute(f"SELECT id FROM polls WHERE poll=?", (poll_,)).fetchone()]
    return poll_id


def add_choice(poll_id: int, choice: str):
    cursor.execute(f"INSERT INTO choices(poll_id, choice) VALUES(?, ?);", (poll_id, choice))
    conn.commit()


def get_poll(poll_id: int, choice: str):
    voice_not_format = cursor.execute(f"SELECT voices FROM choices WHERE poll_id=? AND choice=?",
                                      (poll_id, choice,)).fetchall()
    if voice_not_format:
        voice = [voice for tuple_voice in voice_not_format for voice in tuple_voice]
        up_voice = update_voice(voice)
        cursor.execute(f"UPDATE choices SET voices=? WHERE poll_id=? AND choice=?", (up_voice, poll_id, choice, ))
        conn.commit()
        return 'Вы успешно проголосовали'
    return 'Такого голосования не существует'


def update_voice(voice: list):
    for number in voice:
        number += 1
        return number


def poll_result(poll: str):
    poll_data = [data for data in cursor.execute(f"SELECT id, poll FROM polls WHERE poll=?", (poll,)).fetchone()]
    choices_data = [data for data in cursor.execute(f"SELECT choice, voices FROM choices WHERE poll_id=?",
                                                    (poll_data[0], )).fetchall()]
    list_poll_data = [poll_data, choices_data]
    return list_poll_data


def init_db():
    """Инициализирует БД"""
    with open("utils/createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT * FROM sqlite_master")
    table_exists = cursor.fetchall()

    if not table_exists:
        init_db()


check_db_exists()
