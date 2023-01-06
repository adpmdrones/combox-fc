#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import exchange
 


# IMPORTANTE: inserire il token fornito dal BotFather nella seguente stringa
TOKEN="5400252474:AAEmdKWMQGYSJf5WkOBNufq81fZC6x2gECs"

EXCHANGE=1.125
 
def from_usd_to_eur(usd):
	return usd/EXCHANGE
 
def from_eur_to_usd(eur):
	return EXCHANGE*eur 


def extract_number(text):
     return text.split()[1].strip()
 
def convert_usd(update, context):
     usd=float(extract_number(update.message.text))
     eur=exchange.from_usd_to_eur(usd)
     print(f'Eseguita conversione da {usd} USD a {eur} EUR')
     update.message.reply_text(f'{eur} EUR')
 
def convert_eur(update, context):
     eur=float(extract_number(update.message.text))
     usd=exchange.from_eur_to_usd(eur)
     print(f'Eseguita conversione da {eur} EUR a {usd} USD')
     update.message.reply_text(f'{usd} USD')
 
def main():
   upd= Updater(TOKEN, use_context=True)
   disp=upd.dispatcher
 
   disp.add_handler(CommandHandler("usd", convert_usd))
   disp.add_handler(CommandHandler("eur", convert_eur))
 
   upd.start_polling()
 
   upd.idle()
 
if __name__=='__main__':
   main()