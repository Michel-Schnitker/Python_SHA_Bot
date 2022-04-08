
# Studentisches Hilfsystem zur Alltagsbewaeltigung (SHA - SHzA_Robot)

# import global Code/Data
from telegram.ext import *
#import os

#import local Code/Data
import data
import func
import apikey

#API_KEY = os.environ.get("SHA_API_KEY")
API_KEY = apikey.key


def start(action, context):
    newMessage = " Hallo ich bin SHA,\nihr Studentisches Hilfsystem zur Alltagsbewaeltigung im Training"
    context.bot.send_message(chat_id=action.effective_chat.id, text=newMessage)

def helpHandler(action, context):
    action.message.reply_text("start - Begrüßungstext\n"\
                                "help - Liste aller Befehle\n"\
                                "hunger - tippe: \"/hunger help\" für mehr Hilfe\n"\
                                "selbstzerstoerung - terminiert den Bot\n"\
                                "mute/unmute - Einstellung für Feedback\n")


def hungerHandler(action, context):
    request = action.message.text.split()
    request.remove("/hunger")
    #action.message.reply_text(request)

    if(len(request) == 0):
        action.message.reply_text(func.rand_text(data.Nahrungsliste))
        return


    if(request[0] == "random"):
        action.message.reply_text(func.rand_text(data.Nahrungsliste))
    
    elif(request[0] == "poll"):
        context.bot.send_poll(chat_id=action.effective_chat.id, question="Was essen wir ?", options=data.Nahrungsliste, is_anonymous=False, type='regular', allows_multiple_answers=False)
    
    elif(request[0] == "add"):
        request.remove("add")
        for each in request:
            data.Nahrungsliste.append(each)

    elif(request[0] == "remove"):
        request.remove("remove")
        for each in request:
            data.Nahrungsliste.remove(each)

    elif(request[0] == "list"):
        listString = ""
        for each in data.Nahrungsliste:
            listString += each + "\n"
        action.message.reply_text(listString)

    else:
        action.message.reply_text("help - verständliche Befehle\n"\
                                    "poll - Erstellt Umfrage\n"\
                                    "add x - Fügt Option x hinzu\n"\
                                    "remove x - entfernt Option x\n"\
                                    "list - Zeigt aktuelle Optionen\n"\
                                    "random - Lasst den Zufall entscheiden\n")



def killSwitch(action, context):
    context.bot.leave_chat(chat_id=action.effective_chat.id)
    context.bot.stop()
    exit()

def kommunikationOn(update, context):
    data.mute = True

def kommunikationOff(update, context):
    data.mute = False

def unknownCommand(update, context):
    if(data.mute):
        context.bot.send_message(chat_id=update.effective_chat.id, text=func.rand_text(data.unknown))

def verstaendnisCommand(update, context):
    if(data.mute):
        context.bot.send_message(chat_id=update.effective_chat.id, text=func.rand_text(data.verstaendnis))

def main():
    
    data.Nahrungsliste = data.Essen_bestellen + data.Essen_kochen

    updater = Updater(API_KEY)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('hunger', hungerHandler))
    dp.add_handler(CommandHandler('help', helpHandler))
    dp.add_handler(CommandHandler('selbstzerstoerung', killSwitch))
    dp.add_handler(CommandHandler('mute', kommunikationOff))
    dp.add_handler(CommandHandler('unmute', kommunikationOn))

    # message handler must be last handler, otherwise it would block commands
    dp.add_handler(MessageHandler(Filters.command, unknownCommand))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), verstaendnisCommand))

    updater.start_polling(0)

    updater.idle() #?

if __name__ == "__main__":
    main()