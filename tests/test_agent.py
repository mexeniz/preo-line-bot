import pytest
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
# Include paths for module search
sys.path.insert(0, os.path.join(parentdir, 'bot'))

from agent import (
    Agent, BotCMD, GroupParser
)
from linebot.models import (
    MessageEvent, TextMessage
)

###########################
# BotCMD test cases
###########################

def test_bot_cmd_parse_command():
    assert BotCMD.parse_command("new") == BotCMD.NEW_ORDER
    assert BotCMD.parse_command("add") == BotCMD.ADD_ORDER
    assert BotCMD.parse_command("") == BotCMD.UNKNOWN_CMD
    assert BotCMD.parse_command(None) == BotCMD.UNKNOWN_CMD

###########################
# GroupParser test cases
###########################

def test_bot_group_parser():
    # Return correctly 
    assert GroupParser.parse_text_group("!a b 5") == {"cmd":"a", "order":"b", "num": "5"} 
    assert GroupParser.parse_text_group("!a b c 5") == {"cmd":"a", "order":"b c", "num": "5"} 
    # Not match regex, return None 
    assert GroupParser.parse_text_group("!a b") == None
    assert GroupParser.parse_text_group("!a 5") == None
    assert GroupParser.parse_text_group("!a b 3 d") == None
    assert GroupParser.parse_text_group("!a 5 b") == None
    assert GroupParser.parse_text_group("a b 5") == None
    # "order" should handle special char correclty
    assert GroupParser.parse_text_group("!add Hamburger,Steak 5") == {"cmd":"add", "order":"Hamburger,Steak", "num":"5"}
    # "num" only count last number; other number will be in "order"
    assert GroupParser.parse_text_group("!add Hamburger,Steak 5 19") == {"cmd":"add", "order":"Hamburger,Steak 5", "num":"19"}
    # Single Command 
    assert GroupParser.parse_text_group("!Help") == {"cmd":"Help"}
    assert GroupParser.parse_text_group("Help") == None 
    assert GroupParser.parse_text_group("Help5") == None 
    assert GroupParser.parse_text_group("Help help") == None
    # From Real Command
    assert GroupParser.parse_text_group("!new") == {"cmd":"new"}
    assert GroupParser.parse_text_group("!add food 3") == {"cmd":"add", "order":"food", "num":"3"}
    assert GroupParser.parse_text_group("!del food food 3") == {"cmd":"del", "order":"food food", "num":"3"}
    assert GroupParser.parse_text_group("!end") == {"cmd":"end"}
    assert GroupParser.parse_text_group("!list") == {"cmd":"list"}
    assert GroupParser.parse_text_group("!help") == {"cmd":"help"}

###########################
# Agent test cases
###########################

# Init agent and mock object
agent = Agent()
text_message = TextMessage(text="mock message")
mock_event = MessageEvent(timestamp=123, source='123',
                          reply_token='123', message=text_message)


def test_agent_handle_text_message():
    assert agent.handle_text_message(mock_event) == mock_event.message.text
