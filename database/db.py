import sqlite3
import sys
import traceback
from typing import List, Tuple, Union

from utils import gen_code 

con = sqlite3.connect('database/sqlite.db')

sql_init = open('database/init.sql', 'r').read()
con.execute(sql_init)
con.commit()

Error = Union[str, None]
CodePoint = Tuple[str, int, int]


def handle_error(err: sqlite3.Error) -> None:
    print(f'[-] SQLite error: {" ".join(err.args)}')
    print('[-] SQLite traceback: ')
    exc_type, exc_value, exc_tb = sys.exc_info()
    print(traceback.print_exception(exc_type, exc_value, exc_tb))


def gen_point_code(point: int = 0, amount: int = 1) -> Tuple[None, Error]:
    sql = 'INSERT INTO `point_code`(`code`, `point`) VALUES (?, ?)'

    # keep trying until codes are unique
    while True:
        codes = [(gen_code(), point) for _ in range(amount)]

        try:
            con.executemany(sql, codes)
            con.commit()
            return (None, None)

        except sqlite3.IntegrityError:
            con.rollback()
            continue

        except sqlite3.Error as err:
            handle_error(err)
            return (None, ' '.join(err.args))


def get_point_code() -> Tuple[Union[None, List[CodePoint]], Error]:
    sql = 'SELECT * FROM `point_code`'

    try:
        cur = con.execute(sql)
        rows = cur.fetchall()
        con.commit()
        return (rows, None)

    except sqlite3.Error as err:
        handle_error(err)
        return (None, ' '.join(err.args))


def use_point_code(code: str, group: int) -> Tuple[None, Error]:
    sql_check_not_used = 'SELECT 1 FROM `point_code` WHERE `code` = ? AND used_by = 0'
    sql_update = 'UPDATE `point_code` SET `used_by` = ? WHERE `code` = ?'

    try:
        cur = con.execute(sql_check_not_used, (code))
        res = cur.fetchone()
        con.commit()

        if len(res) == 1:
            return (None, 'Code already used!')

        con.execute(sql_update, (group, code))
        con.commit()

        return (None, None)

    except sqlite3.Error as err:
        handle_error(err)
        return (None, ' '.join(err.args))


def delete_point_code(code: str) -> Tuple[None, Error]:
    sql_check_not_used = 'SELECT 1 FROM `point_code` WHERE `code` = ? AND used_by = 0'
    sql_delete = 'UPDATE `point_code` SET `used_by` = -1 WHERE `code` = ?'

    try:
        cur = con.execute(sql_check_not_used, (code))
        res = cur.fetchone()
        con.commit()

        if len(res) == 1:
            return (None, 'Code already used!')

        con.execute(sql_delete, (code))
        con.commit()

        return (None, None)

    except sqlite3.Error as err:
        handle_error(err)
        return (None, ' '.join(err.args))

