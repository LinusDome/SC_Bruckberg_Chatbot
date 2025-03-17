#main
from bot import SCBruckbergChatbot

bot = SCBruckbergChatbot()

print("⚽ Willkommen beim SC Bruckberg Chatbot! Frag mich etwas über den Verein. (Tippe 'exit' zum Beenden)")

while True:
    user_input = input("Du: ")
    if user_input.lower() == "exit":
        print("Bot: Bis bald! ⚽")
        break
    print("Bot:", bot.antworten(user_input))