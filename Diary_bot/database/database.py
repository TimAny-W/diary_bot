import sqlite3
from typing import List, Any
from datetime import datetime


class Database:
    def __init__(self, name: str) -> None:
        self.name = name
        self.con = sqlite3.connect(name)
        self.cursor = self.con.cursor()
        self.db_init()

    def db_init(self) -> None:
        """Creating a table in database"""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Diary("
                            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                            "user_id INTEGER,"
                            "day INTEGER,"
                            "note TEXT)")

    def add_note(self, user_id: int, note: str) -> str:
        """Add note to the diary

        :param user_id: telegram id of user
        :param note: text to write in the diary
        :return: string result of running
        """
        if type(user_id) != int:
            return 'Error| incorrect data type of user_id |'
        day = self.get_amount_of_days(user_id) + 1
        date = datetime.now().date()
        self.cursor.execute("INSERT into Diary(user_id, day, note) VALUES(?, ?, ?)", (user_id,
                                                                                      day,
                                                                                      f'{date}\n' + note,
                                                                                      ))

        self.con.commit()

    def edit_last_note(self, user_id: int, text: str) -> None:
        """Replace text of exiting note

        :param text: text to replace
        :param user_id: telegram_user id
        :return: None
        """
        last_note_num = self.get_amount_of_days(user_id)
        original_note_text = self.get_note(user_id, last_note_num)[3] + '\n'

        self.cursor.execute('UPDATE Diary SET note = ? WHERE user_id = (?) AND day = (?)',
                            (original_note_text + text, user_id, last_note_num))

    def get_amount_of_days(self, user_id: int) -> int:
        """Getting amount of days diary of current user

        :param user_id: telegram user id
        :return: amount of days of diary
        """
        self.cursor.execute('SELECT * from Diary WHERE user_id=(?)', (user_id,))
        return len(self.cursor.fetchall())

    def get_note(self, user_id: int, day: int) -> List[Any]:
        """Getting specific note by day

        :param user_id: telegram user id
        :param day: num day of note
        :return: Note like tuple(user_id,day,note)
        """
        self.cursor.execute('SELECT * from Diary WHERE (user_id,day) = (?,?)', (user_id, day))
        return self.cursor.fetchone()

    def get_all_notes_user(self, user_id: int) -> List[Any]:
        """Getting all notes from user

        :param user_id: telegram user id
        :return: List with notes like (user_id,day,note)
        """
        self.cursor.execute('SELECT * from Diary WHERE user_id=(?)', (user_id,))
        return self.cursor.fetchall()

    def check_no_notes(self, user_id: int) -> bool:
        """Checks if the user has notes

        :param user_id: telegram user id
        :return: true if user has notes or false if user hasn't notes
        """
        self.cursor.execute('SELECT * from Diary WHERE user_id=(?)', (user_id,))
        if self.cursor.fetchall():
            return True

        return False

    def delete(self, user_id: int, day: int):
        """Delete note

        :param user_id: telegram user id
        :param day: day of note
        :return: result
        """
        self.cursor.execute('Delete FROM Diary where user_id=(?) AND day=(?)', (user_id, day))
        return 'Successfully deleted'

    def _delete_all(self) -> str:
        """Delete all from database

        :return: result of running
        """
        self.cursor.execute('DELETE from Diary')
        self.con.commit()
        return 'Database was cleaned'
