import tkinter as tk
from bot import SCBruckbergChatbot
from data import fragen_antworten  # Importiere die Fragen und Antworten

# Chatbot-Instanz erstellen
bot = SCBruckbergChatbot(fragen_antworten)

def send_message():
    user_input = entry.get().strip()  # Benutzertext holen und Leerzeichen entfernen
    if user_input:
        chatbox.config(state=tk.NORMAL)
        chatbox.insert(tk.END, f"Du: {user_input}\n", "user")  # Benutzereingabe anzeigen
        entry.delete(0, tk.END)  # Eingabefeld leeren
        
        bot_response = bot.antworten(user_input)  # Bot antwortet
        
        # Falls der Bot eine Rückfrage stellt (z.B. "ja/nein"), in die GUI schreiben
        if "ja/nein" in bot_response.lower():
            chatbox.insert(tk.END, f"Bot: {bot_response}\n", "bot")
            chatbox.insert(tk.END, "Antworte mit 'ja' oder 'nein' in das Eingabefeld.\n", "bot")
        else:
            chatbox.insert(tk.END, f"Bot: {bot_response}\n", "bot")  # Normale Antwort ausgeben

        chatbox.config(state=tk.DISABLED)
        chatbox.yview(tk.END)  # Nach unten scrollen
        
def start_chatbot_gui():
    global chatbox, entry  # Damit wir in anderen Funktionen darauf zugreifen können
    
    # Hauptfenster erstellen
    root = tk.Tk()
    root.title("SC Bruckberg Chatbot ⚽")
    root.geometry("500x600")

    # Chat-Anzeige
    chatbox = tk.Text(root, state=tk.DISABLED, wrap=tk.WORD, font=("Arial", 12))
    chatbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Text-Styling für User und Bot
    chatbox.tag_configure("user", foreground="blue")
    chatbox.tag_configure("bot", foreground="green")

    # Begrüßungsnachricht vom Bot
    chatbox.config(state=tk.NORMAL)
    chatbox.insert(tk.END, "⚽ Willkommen beim SC Bruckberg Chatbot!\n", "bot")
    chatbox.insert(tk.END, "Frag mich etwas über den Verein. (Tippe 'exit' zum Beenden)\n\n", "bot")
    chatbox.config(state=tk.DISABLED)

    # Eingabefeld
    entry = tk.Entry(root, font=("Arial", 12))
    entry.pack(pady=10, padx=10, fill=tk.X)
    entry.bind("<Return>", lambda event: send_message())  # Nachricht senden mit ENTER

    # Senden-Button
    send_button = tk.Button(root, text="Senden", command=send_message, font=("Arial", 12))
    send_button.pack(pady=5)

    root.mainloop()
