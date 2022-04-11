#!/usr/bin/env python3.10
from __future__ import annotations

import os
import random
from typing import Dict, List

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# Studentisches Hilfssystem zur Alltagsbewältigung (SHA - SHzA_Robot)

# --- Global vars that hold data for eating ---

possible_dishes: Dict[str, List[str]] = {
    "order": [
        "Pizza",
        "Döner",
        "Sushi",
    ],

    "make_self": [
        "Wraps machen",
        "Nudelauflauf",
    ],

    "custom": [],

}

replies: Dict[bool, List[str]] = {
    True: [
        "Keine Sorge ich höre Ihnen zu!",
        "Ich verstehe",
        "Was denkt Ihre Mutter darüber ?",
        "Ich wünschte mein Leben wäre so interessant",
        "Uhhhhh, da stimme ich Ihnen zu",
        "Das hat Einstein auch schon gesagt!",
        "nein wirklich ?"
    ],
    False: [
        "Ich kann Sie nicht verstehen",
        "Ich konnte Ihr Bedürfnis nicht parsen"
    ]
}

# -/- Global vars that hold data for eating ---

is_muted = False


def rand_text(strings: List[str]) -> str:
    return random.choice(strings)


def start(action: Update, _: CallbackContext) -> None:  # type: ignore[type-arg]
    action.message.reply_text(" Hallo ich bin SHA,\nihr studentisches Hilfssystem zur Alltagsbewältigung im Training")


def help_handler(action: Update, _: CallbackContext) -> None:  # type: ignore[type-arg]
    action.message.reply_text("""
start - Begrüßungstext
help - Liste aller Befehle
hunger - tippe: "/hunger help" für mehr Hilfe
selbstzerstoerung - terminiert den Bot
mute/unmute - Einstellung für Feedback
                              """)


def hunger_handler(action: Update, context: CallbackContext) -> None:  # type: ignore[type-arg]
    request = action.message.text.split()[1:]
    nahrungsliste = [item for row in possible_dishes.values() for item in row]

    # TODO: Check the poll for results.

    match request:
        case [""] | ["random"]:
            # TODO: Is this the desired behaviour?
            action.message.reply_text(rand_text(nahrungsliste))

        case ["poll"]:
            if action.effective_chat is None:
                action.message.reply_text("Ich kann leider nicht mit einer Umfrage antworten 😔")
            else:
                context.bot.send_poll(chat_id=action.effective_chat.id, question="Was essen wir ?", options=nahrungsliste, is_anonymous=False, type='regular', allows_multiple_answers=True)

        case ["add", *item]:
            possible_dishes["custom"].extend(item)

        case ["remove", *item]:
            for it in item:
                if it in possible_dishes["custom"]:
                    possible_dishes["custom"].remove(it)
                else:
                    action.message.reply_text(f"Fehler: {repr(it)} war nicht in den Optionen enthalten.")

        case ["list"]:
            action.message.reply_text("".join(nahrungsliste))

        case _:
            action.message.reply_text("""
help - verständliche Befehle
poll - Erstellt Umfrage
add x - Fügt Option x hinzu
remove x - entfernt Option x
list - Zeigt aktuelle Optionen
random - Lasst den Zufall entscheiden
                    """)


def kill_switch(action: Update, context: CallbackContext) -> None:  # type: ignore[type-arg]
    if action.effective_chat is None:
        action.message.reply_text("Fehler: Ich kann nicht aus diesem Chat austreten!")
        return

    context.bot.leave_chat(chat_id=action.effective_chat.id)

    # Forcefully tell the OS that this process *needs* to be killed. Prevents any exceptions.
    os._exit(1)


# TODO: Can this be removed in favor of checking if
def kommunikation_on(_: Update, __: CallbackContext) -> None:  # type: ignore[type-arg]
    global is_muted
    is_muted = False


def kommunikation_off(_: Update, __: CallbackContext) -> None:  # type: ignore[type-arg]
    global is_muted
    is_muted = True


def unknown_command(update: Update, context: CallbackContext) -> None:  # type: ignore[type-arg]
    if update.effective_chat is not None and not is_muted:
        context.bot.send_message(chat_id=update.effective_chat.id, text=rand_text(replies[False]))


def verstaendnis_command(update: Update, context: CallbackContext) -> None:  # type: ignore[type-arg]
    if update.effective_chat is not None and not is_muted:
        context.bot.send_message(chat_id=update.effective_chat.id, text=rand_text(replies[True]))


def main() -> None:
    API_KEY = os.environ.get("SHA_API_KEY")

    if API_KEY is None:
        print("Error: I cannot find the API Key. Make sure to store it in the environment variable \"SHA_API_KEY\"")
        os._exit(1)

    updater = Updater(API_KEY)
    dp = updater.dispatcher  # type: ignore[has-type]

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('hunger', hunger_handler))
    dp.add_handler(CommandHandler('help', help_handler))
    dp.add_handler(CommandHandler('selbstzerstoerung', kill_switch))
    dp.add_handler(CommandHandler('mute', kommunikation_off))
    dp.add_handler(CommandHandler('unmute', kommunikation_on))

    # message handler must be last handler, otherwise it would block commands
    dp.add_handler(MessageHandler(Filters.command, unknown_command))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), verstaendnis_command))

    updater.start_polling(0)


if __name__ == "__main__":
    main()
