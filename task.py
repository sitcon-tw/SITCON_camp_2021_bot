from __future__ import annotations
import json
from typing import List, TypedDict, Union


class Answer(TypedDict):
    password: str
    message: str
    is_correct: bool
    log: NotRequired[bool]


class Task(TypedDict):
    task_id: str
    max_attempt: NotRequired[int]
    point: int
    answers: List[Answer]
    wrong_message: str


with open('escape_room_task.json', 'rb') as f:
    TASKS: List[Task] = json.load(f)

# check schema at runtime,
# just to make sure I didn't type them wrong...
for task in TASKS:
    assert type(task) is dict
    assert type(task['task_id']) is str
    assert 'max_attempt' not in task or type(task['max_attempt']) is int
    assert type(task['point']) is int
    assert type(task['answers']) is list
    for answer in task['answers']:
        assert type(answer) is dict
        assert type(answer['password']) is str
        assert type(answer['message']) is str
        assert type(answer['is_correct']) is bool
        assert 'log' not in answer or type(answer['log']) is bool
    assert type(task['wrong_message']) is str


def get_task_by_id(task_id: str) -> Union[None, Task]:
    return next(filter(lambda task: task['task_id'] == task_id, TASKS), None)


def get_answer_by_password(password: str, answers: List[Answer]) -> Union[None, Answer]:
    return next(filter(lambda ans: ans['password'] == password, answers), None)
