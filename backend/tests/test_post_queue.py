import pytest

from ascmonitor.channels import Channel
from ascmonitor.post_queue import PostQueue, QueueEmptyException


@pytest.fixture
def post_queue(mongo):
    return PostQueue("test-channel", mongo)


def test_empty(post_queue):
    assert post_queue.view() == []


def test_view(post_queue):
    first, second = "id-1", "id-2"
    post_queue.append(first)
    post_queue.append(second)
    assert post_queue.view() == ["id-1", "id-2"]


def test_append(post_queue):
    first, second = "id-1", "id-2"

    post_queue.append(first)
    assert post_queue.view() == ["id-1"]

    post_queue.append(second)
    assert post_queue.view() == ["id-1", "id-2"]


def test_append__duplicate(post_queue):
    first, second = "id-1", "id-2"
    post_queue.append(first)
    post_queue.append(second)

    with pytest.raises(ValueError):
        post_queue.append(first)


def test_remove__first(post_queue):
    first, second = "id-1", "id-2"
    post_queue.append(first)
    post_queue.append(second)

    post_queue.remove(first)
    assert post_queue.view() == ["id-2"]


def test_remove__second(post_queue):
    first, second = "id-1", "id-2"
    post_queue.append(first)
    post_queue.append(second)

    post_queue.remove(second)
    assert post_queue.view() == ["id-1"]


def test_remove__missing(post_queue):
    first, second = "id-1", "id-2"
    post_queue.append(first)
    assert post_queue.view() == ["id-1"]

    post_queue.remove(second)
    assert post_queue.view() == ["id-1"]


def test_move_up(post_queue):
    first, second = "id-1", "id-2"
    post_queue.append(first)
    post_queue.append(second)

    post_queue.move_up(second)
    assert post_queue.view() == ["id-2", "id-1"]

    # if in front, nothing changes
    post_queue.move_up(second)
    assert post_queue.view() == ["id-2", "id-1"]


def test_move_down(post_queue):
    first, second = "id-1", "id-2"
    post_queue.append(first)
    post_queue.append(second)

    post_queue.move_down(first)
    assert post_queue.view() == ["id-2", "id-1"]

    # if in back, nothing changes
    post_queue.move_down(first)
    assert post_queue.view() == ["id-2", "id-1"]


def test_pop(post_queue):
    first, second = "id-1", "id-2"
    post_queue.append(first)
    post_queue.append(second)

    head = post_queue.pop()
    assert head == "id-1"
    assert post_queue.view() == ["id-2"]


def test_pop__empty(post_queue):
    with pytest.raises(QueueEmptyException):
        post_queue.pop()
