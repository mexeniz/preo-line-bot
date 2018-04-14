import pytest
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
# Include paths for module search
sys.path.insert(0, os.path.join(parentdir, 'bot'))
from order import (
    RoomOrder
)
from orderdb import (
    OrderDB
)
from response import (
    Response
)

TEST_DB_PATH = "/tmp/test-preo-bot.db"
TEST_ROOM_1 = "room1"
TEST_ORDER_1 = "order1"
TEST_ORDER_2 = "order2"

###########################
# RoomOrder test cases
###########################

def create_mock_roomorder():
    if os.path.exists(TEST_DB_PATH):
        # clean old test database before init new RoomOrder
        os.remove(TEST_DB_PATH)
    room_order = RoomOrder(TEST_DB_PATH)
    assert isinstance(room_order, RoomOrder)
    return room_order

def test_roomorder_init():
    room_order = RoomOrder(TEST_DB_PATH)
    assert isinstance(room_order, RoomOrder)
    assert isinstance(room_order.rooms_enable, dict)
    assert isinstance(room_order.order_db, OrderDB)

def test_roomorder_new_order():
    room_order = create_mock_roomorder()
    reply = room_order.new_order(TEST_ROOM_1, TEST_ORDER_1)
    assert reply == Response.text(Response.REP_NEW_ORDERLIST_CREATED, TEST_ORDER_1)
    assert True == room_order.is_order_opened(TEST_ROOM_1)

def test_roomorder_multiple_new_order():
    room_order = create_mock_roomorder()
    room_order.new_order(TEST_ROOM_1, TEST_ORDER_1)
    reply = room_order.new_order(TEST_ROOM_1, TEST_ORDER_2)
    assert reply == Response.text(Response.REP_DUP_ORDERLIST)
    assert True == room_order.is_order_opened(TEST_ROOM_1)

def test_roomorder_list_order():
    room_order = create_mock_roomorder()
    room_order.new_order(TEST_ROOM_1, TEST_ORDER_1)
    reply = room_order.list_order(TEST_ROOM_1)
    assert reply == Response.text(Response.REP_SUMMARY_ORDERLIST, "")

def test_roomorder_close_order_success():
    room_order = create_mock_roomorder()
    room_order.new_order(TEST_ROOM_1, TEST_ORDER_1)
    assert Response.text(Response.REP_ORDERLIST_CLOSED) == room_order.close_order(TEST_ROOM_1)
    assert False == room_order.is_order_opened(TEST_ROOM_1)
    # try to close again
    assert Response.text(Response.REP_ORDERLIST_ALREADY_CLOSED) == room_order.close_order(TEST_ROOM_1)

def test_roomorder_close_order_fail():
    room_order = create_mock_roomorder()
    assert None == room_order.close_order(TEST_ROOM_1)

def test_roomorder_end_order():
    room_order = create_mock_roomorder()
    room_order.new_order(TEST_ROOM_1, TEST_ORDER_1)
    reply = room_order.end_order(TEST_ROOM_1)
    assert reply == Response.text(Response.REP_END_ORDERLIST)
    assert False == room_order.is_order_opened(TEST_ROOM_1)
