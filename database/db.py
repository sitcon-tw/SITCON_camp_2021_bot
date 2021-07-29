import sqlite3
import sys
import traceback
from typing import List, Tuple, Union

from utils import gen_code

con = sqlite3.connect('database/sqlite.db')

sql_init = open('database/init.sql', 'r').read()
con.executescript(sql_init)
con.commit()

Code = str
Point = int
UsedBy = int
Error = Union[str, None]
CodePoint = Tuple[Code, Point, UsedBy]


def handle_error(err: sqlite3.Error) -> None:
    print(f'[-] SQLite error: {" ".join(err.args)}')
    print('[-] SQLite traceback: ')
    exc_type, exc_value, exc_tb = sys.exc_info()
    print(traceback.print_exception(exc_type, exc_value, exc_tb))


def gen_point_code(point: int = 0, amount: int = 1) -> Tuple[Union[List[str], None], Error]:
    sql = 'INSERT INTO `point_code`(`code`, `point`) VALUES (?, ?)'

    # keep trying until codes are unique
    while True:
        codes = [(gen_code(), point) for _ in range(amount)]

        try:
            con.executemany(sql, codes)
            con.commit()
            return ([code[0] for code in codes], None)

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


def use_point_code(code: str, group: int) -> Tuple[Union[Point, None], Error]:
    sql_check_not_used = 'SELECT `used_by`, `point` FROM `point_code` WHERE `code` = ?'
    sql_update = 'UPDATE `point_code` SET `used_by` = ? WHERE `code` = ?'

    try:
        cur = con.execute(sql_check_not_used, (code, ))
        res = cur.fetchone()
        con.commit()

        if res is None:
            return (None, 'not exists')

        used_by, point = res

        if used_by > 0 or used_by == -1:
            return (None, 'used')

        con.execute(sql_update, (group, code))
        con.commit()

        return (point, None)

    except sqlite3.Error as err:
        handle_error(err)
        return (None, ' '.join(err.args))


def delete_point_code(code: str) -> Tuple[None, Error]:
    sql_check_not_used = 'SELECT 1 FROM `point_code` WHERE `code` = ? AND `used_by` = 0'
    sql_delete = 'UPDATE `point_code` SET `used_by` = -1 WHERE `code` = ?'

    try:
        cur = con.execute(sql_check_not_used, (code, ))
        res = cur.fetchone()
        con.commit()

        if res is None:
            return (None, 'used')

        con.execute(sql_delete, (code, ))
        con.commit()

        return (None, None)

    except sqlite3.Error as err:
        handle_error(err)
        return (None, ' '.join(err.args))


def get_group_point() -> Tuple[Union[List[Tuple[int, int]], None], Error]:
    """
    Return a list of tuple where the `i`-th value is the rank `i+1`-th (group, point)

    e.g. if res[0] == (5, 100), then group 5 is currently at rank 1 with 100 points
    """

    sql = '''
        SELECT `used_by` AS `group`, SUM(`point`) AS `point`
        FROM `point_code`
        WHERE `used_by` > 0
        GROUP BY `used_by`
        ORDER BY `point` DESC, `group` ASC
    '''

    try:
        cur = con.execute(sql)
        rows = cur.fetchall()
        con.commit()

        res = []
        groups = set()
        for row in rows:
            res.append(row)
            groups.add(row[0])

        for i in range(1, 10):
            if i not in groups:
                res.append((i, 0))

        return (res, None)

    except sqlite3.Error as err:
        handle_error(err)
        return (None, ' '.join(err.args))


def get_group_selection_message_id() -> Tuple[Union[int, None], Error]:
    sql = 'SELECT `id` FROM `message` LIMIT 1'

    try:
        cur = con.execute(sql)
        row = cur.fetchone()
        con.commit()

        if row is None:
            return (None, 'not exists')

        return (row[0], None)

    except sqlite3.Error as err:
        handle_error(err)
        return (None, ' '.join(err.args))


def store_group_selection_message_id(id: int) -> Tuple[None, Error]:
    sql = 'INSERT INTO `message` VALUES (?)'

    try:
        con.execute(sql, (id, ))
        con.commit()

        return (None, None)

    except sqlite3.Error as err:
        handle_error(err)
        return (None, ' '.join(err.args))

