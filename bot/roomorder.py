from response import Response
from preodb import PreoDB

class RoomOrder:
    def __init__(self, db_path=PreoDB.DEFAULT_DB_PATH):
        self.preo_db = PreoDB(db_path)

    def new_order(self, room_id, list_name):
        if self.preo_db.is_room_order_exist(room_id):
            # Room order has already been created.
            return Response.text(Response.REP_DUP_ORDERLIST)

        self.preo_db.new_room_order(room_id, list_name)
        return Response.text(Response.REP_NEW_ORDERLIST_CREATED, list_name)

    def set_item(self, room_id, user_name, item_name, amount):
        if not self.preo_db.is_room_order_exist(room_id):
            # Room order has not been created yet.
            print("Error: room order %s does not exist" % (room_id))
            return None

        if not self.preo_db.is_room_order_enable(room_id):
            # Room order is not enabled.
            print("Error: room order %s is not enabled" % (room_id))
            return Response.text(Response.REP_ORDERLIST_ALREADY_CLOSED)

        self.preo_db.set_order(room_id, user_name, item_name, amount)
        return Response.text(Response.REP_SET_ITEM, user_name, item_name, amount)

    def delete_item(self, room_id, user_name, item_name):
        if not self.preo_db.is_room_order_exist(room_id):
            # Room order has not been created yet.
            print("Error: room order %s does not exist" % (room_id))
            return None

        if not self.preo_db.is_room_order_enable(room_id):
            # Room order is not enabled.
            print("Error: room order %s is not enabled" % (room_id))
            return Response.text(Response.REP_ORDERLIST_ALREADY_CLOSED)
        if not self.preo_db.get_order_by_user_item(room_id, user_name, item_name):
            # Item does not exist.
            print("Error: item %s for %s does not exist in %s" % (item_name, user_name, room_id))
            return Response.text(Response.REP_DEL_NOT_EXIST_ITEM, user_name, item_name)

        self.preo_db.del_order(room_id, user_name, item_name)
        return Response.text(Response.REP_DEL_ITEM, user_name, item_name)

    def list_order(self, room_id):
        room_order = self.preo_db.get_room_order(room_id)
        if room_order == None:
            # Room order has not been created yet.
            print("Error: room order %s does not exist" % (room_id))
            return None

        order_list = self.preo_db.get_order_by_room(room_id)
        text = self.__order_list_to_str(order_list)
        return Response.text(Response.REP_SUMMARY_ORDERLIST, room_order.list_name, text)

    def close_order(self, room_id):
        if not self.preo_db.is_room_order_exist(room_id):
            # Room order has not been created yet.
            print("Error: room order %s does not exist" % (room_id))
            return None

        if not self.preo_db.is_room_order_enable(room_id):
            # Room order has already been disabled.
            return Response.text(Response.REP_ORDERLIST_ALREADY_CLOSED)

        self.preo_db.disable_room_order(room_id)
        return Response.text(Response.REP_ORDERLIST_CLOSED)

    def open_order(self, room_id):
        if not self.preo_db.is_room_order_exist(room_id):
            # Room order has not been created yet.
            print("Error: room order %s does not exist" % (room_id))
            return None

        if self.preo_db.is_room_order_enable(room_id):
            # Room order has already been enabled.
            return Response.text(Response.REP_ORDERLIST_ALREADY_OPENED)

        self.preo_db.enable_room_order(room_id)
        return Response.text(Response.REP_OPEN_ORDERLIST)

    def is_order_opened(self, room_id):
        if not self.preo_db.is_room_order_exist(room_id):
            # Room order has not been created.
            return False

        return self.preo_db.is_room_order_enable(room_id)

    def end_order(self, room_id):
        room_order = self.preo_db.get_room_order(room_id)
        if room_order == None:
            # Room order has not been created.
            print("Error: room order %s does not exist" % (room_id))
            return None

        order_list = self.preo_db.get_order_by_room(room_id)
        text = self.__order_list_to_str(order_list)
        self.preo_db.del_room_order(room_id)

        return Response.text(Response.REP_END_ORDERLIST, room_order.list_name, text)

    @staticmethod
    def __order_print_user_item_amount(order):
        return "%s: %s %s" % (order.user_name, order.item_name, order.amount)

    @staticmethod
    def __order_list_to_str(order_list):
        # Creating a dict mapping item name into a list of text list and total maount
        # ex. "milk" : (["user1", "user3(2)"], 3)
        order_dict = {}
        for order in order_list:
            item_name = order.item_name
            amount = order.amount
            text = order.user_name if amount == 1 else "%s(%d)" % (order.user_name, amount)
            if item_name in order_dict:
                order_dict[item_name][0].append(text)
                order_dict[item_name][1] += amount
            else:
                order_dict[item_name] = [[text], amount]

        order_text = ""
        for item_name, args in order_dict.items():
            order_text += "%s %d: %s\n" % (item_name, args[1], " ".join(args[0]))
        return order_text.strip()

""" deprecated code use for reference
class Order:
    def __init__(self, name):
        self.name = name
        self.enable = True
        self.order_by_menu = {}
        self.order_by_user = {}

    def add_order(self, user, menu, amount=1):
        if self.enable:
            return Response.text(Response.REP_NOT_IMPLEMENT)
        else:
            return Response.text(Response.REP_ORDERLIST_CLOSED, self.name)

    def del_order(self, user, menu, amount=-1):
        if self.enable:
            return Response.text(Response.REP_NOT_IMPLEMENT)
        else:
            return Response.text(Response.REP_ORDERLIST_CLOSED, self.name)

    def set_enable(self, flag):
        self.enable = flag

    def order_by_menu_string(self):
        text = ""
        for menu, amount in self.order_by_menu:
            text += "%s %d" % (menu, amount) + "\n"
        return text[:-1]

    def order_by_user_string(self):
        text = ""
        for user, order in self.order_by_user:
            text += user + "\n"
            for menu, amount in order:
                text += menu + " " + amount + "\n"
        return text[:-1]

    def list_order_by_menu(self):
        return Response.text(Response.REP_ORDER_PRINT, self.name, self.order_by_menu_string)

    def list_order_by_user(self):
        return Response.text(Response.REP_ORDER_PRINT, self.name, self.order_by_user_string)

    def __str__(self):
        return self.order_by_user_string()
"""
