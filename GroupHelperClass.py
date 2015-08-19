#!/usr/bin/env python3
# coding: utf-8

import telegram
import Commands


class GroupHelper:

    def __init__(self, token, last_update_id=None):
        self.last_update_id = last_update_id
        self.Bot = telegram.Bot(token)
        self.chat_id = 0 # None

#   def listener(self, interruption=1):
#   #Вернуть поток, который бы делал check_update с промежутком interruption
#   #А check_update удалить
#        pass

    @staticmethod
    def parse_message(message):
        # добавить корректную обработку kwargs
        result = []
        command = ""
        args = []

        for word in message.split():
            if word.startswith('/'):
                if command:
                    result.append((command, args[:]))
                    command = word
                    args = []
                else:
                    command = word
            else:
                args.append(word)
        else:
            result.append((command, args[:]))

        return result


    def check_update(self):
        try:
            for update in self.Bot.getUpdates(offset=self.last_update_id+1 if self.last_update_id else None):
                self.chat_id = update.message.chat_id
                for (command, args) in self.parse_message(update.message.text):
                    self.last_update_id = update.update_id
                    Commands.commands[command](self, *args)

        except Exception as e:
            print(e)
            self.Bot.sendMessage(text="Опаньки, мы это не предусмотрели!",
                                             chat_id=self.chat_id)


    def send_message(self, message, to_all=False):
        if to_all:
            pass
        else:
            self.Bot.sendMessage(text=message, chat_id=self.chat_id)

    #def send_document
    #def send_photo
    #def send_video
    #def send_audio


# -------------------------------------------------------------------------------------------------------------------- #


    @Commands.define_command(help_text="""HELP METHOD HELP""")
    def help(self, *args):
        result = ""
        help_text_template = "{command} - {description}\n"

        for arg in args:
            command = '/' + arg
            result += help_text_template.format(command=command, description=Commands.commands[command].help_text)

        if not result:
            for command in Commands.commands:
                result += help_text_template.format(command=command, description=Commands.commands[command].help_text)

        self.send_message(result)

        return result



    @Commands.define_command(help_text="START METHOD HELP")
    def start(self):
        result = "START METHOD RETURN"
        self.send_message(result)
        return result


    @Commands.define_command(help_text="TEST METHOD HELP")
    def test(self, attr_1, attr_2):
        result = "TEST METHOD RETURN(" + attr_1 + attr_2 + ")"
        self.send_message(result)
        return result


    @Commands.define_command(special_name="")
    def _empty(self, *args):
        result = ' '.join(args) + "\n_empty"
        self.send_message(result)
        return result


    @Commands.define_command(special_name="/")
    def _one_slash(self, *args):
        result = ' '.join(args) + "\n_one_slash"
        self.send_message(result)
        return result