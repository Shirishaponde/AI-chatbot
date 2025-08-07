# # import sys
# # import tkinter as tk
# # from tkinter import font
# # import pyttsx3
# # import speech_recognition as sr
# # import threading
# # import google.generativeai as genai

# # # --- Google Gemini API Setup ---
# # # IMPORTANT: 1. Run 'pip install google-generativeai' in your terminal.
# # #            2. Get your API key from https://aistudio.google.com/app/apikey
# # #            3. Paste your API key below.
# # try:
# #     GOOGLE_API_KEY = "AIzaSyBRXEG2uoeX5wwzRIAPD67wpGJoU3JIKO4" 
# #     WEATHER_API_KEY="Key: 27d849c7479b45a9b91135215250708"
# #     genai.configure(api_key=GOOGLE_API_KEY)
# #     # model = genai.GenerativeModel('gemini-pro')
 
# #     model = genai.GenerativeModel('gemini-1.5-flash-latest')
# #     # Start a chat session to maintain conversational context
# #     chat_session = model.start_chat(history=[])
# # except Exception as e:
# #     print(f"Error configuring Google AI: {e}\nIs your API key correct?")
# #     model = None

# # # --- Text-to-Speech Setup ---
# # engine = pyttsx3.init()
# # engine.setProperty('voice', engine.getProperty('voices')[0].id)
# # engine.setProperty('rate', 160) # Slightly faster rate
# # engine.setProperty('volume', 1.0)

# # def speak(text):
# #     """Run text-to-speech in a separate thread to avoid freezing the GUI."""
# #     def run_speak():
# #         engine.say(text)
# #         engine.runAndWait()
# #     threading.Thread(target=run_speak, daemon=True).start()

# # # --- GUI Setup ---
# # root = tk.Tk()
# # root.title("Google Gemini Chatbot")
# # root.geometry("450x600")
# # root.configure(bg="#090101")

# # default_font = font.nametofont("TkDefaultFont")
# # default_font.configure(family="Arial", size=11)

# # # --- Core Behavior ---
# # def insert_chat(actor, message):
# #     """Inserts a message into the chat log with proper formatting and auto-scrolls."""
# #     chat_log.config(state="normal")
# #     if actor == "Bot":
# #         chat_log.insert(tk.END, f"Bot: {message}\n\n", "bot_message")
# #     else:
# #         chat_log.insert(tk.END, f"You: {message}\n", "user_message")
# #     chat_log.config(state="disabled")
# #     chat_log.see(tk.END)

# # def get_ai_response(user_input):
# #     """Sends the user's message to the Gemini API and handles the response."""
# #     try:
# #         # Use the chat session to send the message and get a streaming response
# #         response = chat_session.send_message(user_input, stream=True)
        
# #         full_response = ""
# #         # Update the chat log in real-time as the response streams in
# #         for chunk in response:
# #             # Check if chunk contains text
# #             if hasattr(chunk, 'text'):
# #                 full_response += chunk.text
# #                 # GUI updates must happen on the main thread
# #                 root.after(0, lambda text=full_response: update_bot_message(text))

# #         # Speak the final complete response
# #         speak(full_response)

# #     except Exception as e:
# #         error_message = f"Sorry, I ran into an error: {e}"
# #         print(error_message)
# #         root.after(0, lambda: insert_chat("Bot", error_message))
# #         speak(error_message)

# # def update_bot_message(text):
# #     """Updates or inserts the bot's message in the chat log."""
# #     chat_log.config(state="normal")
# #     # Check if the last entry is from the bot, if so, update it.
# #     # This creates the "typing" effect.
# #     current_content = chat_log.get("1.0", tk.END).strip()
# #     if current_content.endswith("Bot:"):
# #         chat_log.insert(tk.END, f" {text}\n\n")
# #     else:
# #         last_line_index = f"{int(chat_log.index('end-1c').split('.')[0])}.0"
# #         chat_log.delete(last_line_index, tk.END)
# #         chat_log.insert(tk.END, f"Bot: {text}\n\n")
    
# #     chat_log.config(state="disabled")
# #     chat_log.see(tk.END)


# # def send_message(event=None):
# #     """Handles sending a message from the entry box."""
# #     user_input = entry.get().strip()
# #     if not user_input:
# #         return
    
# #     insert_chat("You", user_input)
# #     entry.delete(0, tk.END)

# #     if user_input.lower() == "quit":
# #         response = "Goodbye! Have a great day."
# #         insert_chat("Bot", response)
# #         speak(response)
# #         root.after(2000, root.destroy)
# #         return

# #     # Check if the model was configured correctly
# #     if not model:
# #         error_msg = "AI model not configured. Please check your API key."
# #         insert_chat("Bot", error_msg)
# #         speak(error_msg)
# #         return

# #     # Start the "Bot is typing..." placeholder
# #     insert_chat("Bot", "")
# #     root.update_idletasks()
    
# #     # Run the API call in a separate thread to keep the GUI responsive
# #     threading.Thread(target=get_ai_response, args=(user_input,), daemon=True).start()


# # def voice_input():
# #     """Handles voice input and processes it."""
# #     def run_listen():
# #         r = sr.Recognizer()
# #         with sr.Microphone() as source:
# #             insert_chat("Bot", "Listening...")
# #             root.update_idletasks()
# #             r.adjust_for_ambient_noise(source, duration=1)
            
# #             try:
# #                 audio = r.listen(source, timeout=5)
# #                 user_input = r.recognize_google(audio)
                
# #                 # Update GUI on the main thread
# #                 root.after(0, lambda: entry.delete(0, tk.END))
# #                 root.after(0, lambda: entry.insert(0, user_input))
# #                 root.after(100, send_message)

# #             except sr.UnknownValueError:
# #                 speak("Sorry, I couldn't understand that.")
# #             except sr.RequestError:
# #                 speak("Network error. Please check your connection.")
# #             except sr.WaitTimeoutError:
# #                 speak("Listening timed out.")

# #     threading.Thread(target=run_listen, daemon=True).start()

# # # --- Widget Layout ---
# # chat_log = tk.Text(root, bd=1, bg="#ffffff", font=("Arial", 12), state="disabled", wrap=tk.WORD, padx=5, pady=5)
# # chat_log.tag_configure("user_message", foreground="#007bff", font=("Arial", 12, "bold"))
# # chat_log.tag_configure("bot_message", foreground="#202124")
# # chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# # bottom_frame = tk.Frame(root, bg="#f0f0f0")
# # bottom_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

# # entry = tk.Entry(bottom_frame, font=("Arial", 12))
# # entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
# # entry.bind("<Return>", send_message)

# # send_button = tk.Button(bottom_frame, text="➤", font=("Arial", 16, "bold"), bg="#007bff", fg="white", command=send_message, width=3, relief=tk.FLAT)
# # send_button.pack(side=tk.LEFT, padx=(8, 0))

# # voice_button = tk.Button(bottom_frame, text="🎤", font=("Arial", 16), bg="#28a745", fg="white", command=voice_input, width=3, relief=tk.FLAT)
# # voice_button.pack(side=tk.LEFT, padx=(5, 0))

# # # --- Start the application ---
# # root.mainloop()

# import sys
# import tkinter as tk
# from tkinter import font
# import pyttsx3
# import speech_recognition as sr
# import threading
# import google.generativeai as genai
# import requests # ✅ NEW: For making API calls to the weather service
# import json     # ✅ NEW: For handling the API response

# # --- API Key Configuration ---
# try:
#     # 1. Google Gemini API Key
#     GOOGLE_API_KEY = "AIzaSyCTaDgYOZiI7vdpT6zrsF0m1NoP9EY75oc" # <--- PASTE YOUR GOOGLE API KEY
#     genai.configure(api_key=GOOGLE_API_KEY)
    
#     # ✅ NEW: 2. OpenWeatherMap API Key
#     OPENWEATHER_API_KEY = " 27d849c7479b45a9b91135215250708" # <--- PASTE YOUR WEATHER API KEY

# except Exception as e:
#     print(f"API Key Error: {e}")

# # --- ✅ NEW: Weather Tool Function ---
# def get_weather(location: str):
#     """
#     Get the current weather for a specified location using the OpenWeatherMap API.
#     """
#     if not OPENWEATHER_API_KEY:
#         return "Weather API key is not configured."
    
#     base_url = "http://api.openweathermap.org/data/2.5/weather"
#     params = {
#         "q": location,
#         "appid": OPENWEATHER_API_KEY,
#         "units": "metric"  # Use 'imperial' for Fahrenheit
#     }
    
#     try:
#         response = requests.get(base_url, params=params)
#         response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
#         weather_data = response.json()
        
#         if weather_data.get("cod") != 200:
#             return f"Error: {weather_data.get('message', 'Could not find weather for that location.')}"

#         # Extract and format the weather information
#         city = weather_data.get("name")
#         temp = weather_data["main"]["temp"]
#         description = weather_data["weather"][0]["description"]
#         humidity = weather_data["main"]["humidity"]
        
#         return json.dumps({
#             "location": city,
#             "temperature_celsius": f"{temp}°C",
#             "description": description,
#             "humidity": f"{humidity}%"
#         })

#     except requests.exceptions.RequestException as e:
#         return f"Network error while fetching weather: {e}"
#     except Exception as e:
#         return f"An error occurred: {e}"

# # --- ✅ MODIFIED: Configure Gemini Model with the Weather Tool ---
# try:
#     model = genai.GenerativeModel(
#         model_name='gemini-1.5-flash-latest',
#         tools=[get_weather] # Tell the model about the tool it can use
#     )
#     chat_session = model.start_chat(enable_automatic_function_calling=True)
# except Exception as e:
#     print(f"Error configuring Google AI model: {e}")
#     model = None

# # --- Text-to-Speech Setup ---
# engine = pyttsx3.init()
# engine.setProperty('voice', engine.getProperty('voices')[0].id)
# engine.setProperty('rate', 160)
# engine.setProperty('volume', 1.0)

# def speak(text):
#     """Run text-to-speech in a separate thread to avoid freezing the GUI."""
#     def run_speak():
#         engine.say(text)
#         engine.runAndWait()
#     threading.Thread(target=run_speak, daemon=True).start()

# # --- GUI Setup ---
# root = tk.Tk()
# root.title("Gemini Bot with Weather 🌦️")
# root.geometry("450x600")
# root.configure(bg="#f0f0f0")
# default_font = font.nametofont("TkDefaultFont")
# default_font.configure(family="Arial", size=11)

# # --- Core Behavior ---
# def insert_chat(actor, message):
#     """Inserts a message into the chat log."""
#     chat_log.config(state="normal")
#     if actor == "Bot":
#         chat_log.insert(tk.END, f"Bot: {message}\n\n", "bot_message")
#     else:
#         chat_log.insert(tk.END, f"You: {message}\n", "user_message")
#     chat_log.config(state="disabled")
#     chat_log.see(tk.END)

# def get_ai_response(user_input):
#     """Handles the conversation with the Gemini API, including tool calls."""
#     try:
#         # Send the user's message to the chat session
#         response = chat_session.send_message(user_input)
        
#         # The model will automatically handle the function call and response.
#         # We just need to get the final text part.
#         final_text = response.text
#         insert_chat("Bot", final_text)
#         speak(final_text)

#     except Exception as e:
#         error_message = f"Sorry, an error occurred with the AI model: {e}"
#         print(error_message)
#         insert_chat("Bot", error_message)
#         speak(error_message)

# def send_message(event=None):
#     """Handles sending a message from the entry box."""
#     user_input = entry.get().strip()
#     if not user_input:
#         return
    
#     insert_chat("You", user_input)
#     entry.delete(0, tk.END)

#     if user_input.lower() == "quit":
#         response = "Goodbye! Have a great day."
#         insert_chat("Bot", response)
#         speak(response)
#         root.after(2000, root.destroy)
#         return

#     if not model:
#         error_msg = "AI model not configured. Please check your API keys."
#         insert_chat("Bot", error_msg)
#         speak(error_msg)
#         return
    
#     # Run the conversation in a thread to keep the GUI responsive
#     threading.Thread(target=get_ai_response, args=(user_input,), daemon=True).start()

# def voice_input():
#     """Handles voice input."""
#     def run_listen():
#         r = sr.Recognizer()
#         with sr.Microphone() as source:
#             insert_chat("Bot", "Listening...")
#             root.update_idletasks()
#             r.adjust_for_ambient_noise(source, duration=1)
            
#             try:
#                 audio = r.listen(source, timeout=5)
#                 user_input = r.recognize_google(audio)
                
#                 root.after(0, lambda: entry.delete(0, tk.END))
#                 root.after(0, lambda: entry.insert(0, user_input))
#                 root.after(100, send_message)

#             except Exception as e:
#                 speak("Sorry, I couldn't understand that.")

#     threading.Thread(target=run_listen, daemon=True).start()

# # --- Widget Layout ---
# chat_log = tk.Text(root, bd=1, bg="#ffffff", font=("Arial", 12), state="disabled", wrap=tk.WORD, padx=5, pady=5)
# chat_log.tag_configure("user_message", foreground="#007bff", font=("Arial", 12, "bold"))
# chat_log.tag_configure("bot_message", foreground="#202124")
# chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# bottom_frame = tk.Frame(root, bg="#f0f0f0")
# bottom_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

# entry = tk.Entry(bottom_frame, font=("Arial", 12))
# entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
# entry.bind("<Return>", send_message)

# send_button = tk.Button(bottom_frame, text="➤", font=("Arial", 16, "bold"), bg="#007bff", fg="white", command=send_message, width=3, relief=tk.FLAT)
# send_button.pack(side=tk.LEFT, padx=(8, 0))

# voice_button = tk.Button(bottom_frame, text="🎤", font=("Arial", 16), bg="#28a745", fg="white", command=voice_input, width=3, relief=tk.FLAT)
# voice_button.pack(side=tk.LEFT, padx=(5, 0))

# # --- Start the application ---
# root.mainloop()


# import sys
# import tkinter as tk
# from tkinter import font
# import pyttsx3
# import speech_recognition as sr
# import threading
# import google.generativeai as genai
# import requests
# import json

# # --- API Key Configuration ---
# try:
#     # 1. Google Gemini API Key
#     GOOGLE_API_KEY = "AIzaSyCTaDgYOZiI7vdpT6zrsF0m1NoP9EY75oc" # <--- PASTE YOUR GOOGLE API KEY
#     genai.configure(api_key=GOOGLE_API_KEY)
    
#     # 2. OpenWeatherMap API Key
#     OPENWEATHER_API_KEY = " 27d849c7479b45a9b91135215250708" # <--- PASTE YOUR WEATHER API KEY
# except Exception as e:
#     print(f"API Key Error: {e}")
    
# # --- ✅ NEW: State flag to prevent listening loops ---
# is_listening = False

# # --- Weather Tool Function ---
# def get_weather(location: str):
#     """Gets current weather for a location using OpenWeatherMap API."""
#     # (The get_weather function code remains the same as before)
#     if not OPENWEATHER_API_KEY or "YOUR_OPENWEATHERMAP_API_KEY" in OPENWEATHER_API_KEY:
#         return "Weather API key is not configured."
#     base_url = "http://api.openweathermap.org/data/2.5/weather"
#     params = {"q": location, "appid": OPENWEATHER_API_KEY, "units": "metric"}
#     try:
#         response = requests.get(base_url, params=params)
#         response.raise_for_status()
#         weather_data = response.json()
#         if weather_data.get("cod") != 200:
#             return f"Error: {weather_data.get('message', 'Could not find weather for that location.')}"
#         city = weather_data.get("name")
#         temp = weather_data["main"]["temp"]
#         description = weather_data["weather"][0]["description"]
#         humidity = weather_data["main"]["humidity"]
#         return json.dumps({
#             "location": city, "temperature_celsius": f"{temp}°C",
#             "description": description, "humidity": f"{humidity}%"
#         })
#     except Exception as e:
#         return f"An error occurred while fetching weather: {e}"

# # --- Configure Gemini Model with Tools ---
# try:
#     model = genai.GenerativeModel(
#         model_name='gemini-1.5-flash-latest',
#         tools=[get_weather]
#     )
#     chat_session = model.start_chat(enable_automatic_function_calling=True)
# except Exception as e:
#     print(f"Error configuring Google AI model: {e}")
#     model = None

# # --- Text-to-Speech Setup ---
# engine = pyttsx3.init()
# engine.setProperty('voice', engine.getProperty('voices')[0].id)
# engine.setProperty('rate', 160)

# def speak(text):
#     def run_speak():
#         engine.say(text)
#         engine.runAndWait()
#     threading.Thread(target=run_speak, daemon=True).start()

# # --- GUI Setup ---
# root = tk.Tk()
# root.title("Gemini Bot with Weather 🌦️")
# root.geometry("450x600")
# root.configure(bg="#f0f0f0")
# default_font = font.nametofont("TkDefaultFont")
# default_font.configure(family="Arial", size=11)

# # --- Core Behavior ---
# def insert_chat(actor, message):
#     chat_log.config(state="normal")
#     if actor == "Bot":
#         chat_log.insert(tk.END, f"Bot: {message}\n\n", "bot_message")
#     else:
#         chat_log.insert(tk.END, f"You: {message}\n", "user_message")
#     chat_log.config(state="disabled")
#     chat_log.see(tk.END)

# def get_ai_response(user_input):
#     try:
#         response = chat_session.send_message(user_input)
#         final_text = response.text
#         insert_chat("Bot", final_text)
#         speak(final_text)
#     except Exception as e:
#         error_message = f"Sorry, an error occurred: {e}"
#         print(error_message)
#         insert_chat("Bot", error_message)

# def send_message(event=None):
#     user_input = entry.get().strip()
#     if not user_input: return
#     insert_chat("You", user_input)
#     entry.delete(0, tk.END)
#     if user_input.lower() == "quit":
#         root.after(1000, root.destroy)
#         return
#     if not model:
#         insert_chat("Bot", "AI model not configured.")
#         return
#     threading.Thread(target=get_ai_response, args=(user_input,), daemon=True).start()

# # --- 💡 MODIFIED: Voice input function with state management ---
# def voice_input():
#     """Handles voice input, preventing loops with a state flag."""
#     global is_listening # Use the global flag

#     if is_listening:
#         print("Already listening.")
#         return # Exit if a listening session is already active

#     is_listening = True # Set the flag to block other requests

#     def run_listen():
#         global is_listening
#         r = sr.Recognizer()
#         with sr.Microphone() as source:
#             insert_chat("Bot", "Listening...")
#             root.update_idletasks()
#             r.adjust_for_ambient_noise(source, duration=1)
#             try:
#                 audio = r.listen(source, timeout=5)
#                 user_input = r.recognize_google(audio)
#                 root.after(0, lambda: entry.delete(0, tk.END))
#                 root.after(0, lambda: entry.insert(0, user_input))
#                 root.after(100, send_message)
#             except sr.UnknownValueError:
#                 insert_chat("Bot", "Sorry, I couldn't understand that.")
#             except sr.RequestError:
#                 insert_chat("Bot", "Network error, please check your connection.")
#             except sr.WaitTimeoutError:
#                 insert_chat("Bot", "Listening timed out.")
#             finally:
#                 # ✅ CRUCIAL: Always reset the flag when finished
#                 is_listening = False

#     threading.Thread(target=run_listen, daemon=True).start()

# # --- Widget Layout ---
# chat_log = tk.Text(root, bd=1, bg="#ffffff", font=("Arial", 12), state="disabled", wrap=tk.WORD, padx=5, pady=5)
# chat_log.tag_configure("user_message", foreground="#007bff", font=("Arial", 12, "bold"))
# chat_log.tag_configure("bot_message", foreground="#202124")
# chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# bottom_frame = tk.Frame(root, bg="#f0f0f0")
# bottom_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

# entry = tk.Entry(bottom_frame, font=("Arial", 12))
# entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
# entry.bind("<Return>", send_message)

# send_button = tk.Button(bottom_frame, text="➤", font=("Arial", 16, "bold"), bg="#007bff", fg="white", command=send_message, width=3, relief=tk.FLAT)
# send_button.pack(side=tk.LEFT, padx=(8, 0))

# voice_button = tk.Button(bottom_frame, text="🎤", font=("Arial", 16), bg="#28a745", fg="white", command=voice_input, width=3, relief=tk.FLAT)
# voice_button.pack(side=tk.LEFT, padx=(5, 0))

# # --- Start the application ---
# root.mainloop()



import sys
import tkinter as tk
from tkinter import font
import pyttsx3
import speech_recognition as sr
import threading
import google.generativeai as genai
import requests
import json

# --- API Key Configuration ---
# IMPORTANT: You must fill in both API keys for the bot to work.
try:
    # 1. Google Gemini API Key
    GOOGLE_API_KEY = "AIzaSyCTaDgYOZiI7vdpT6zrsF0m1NoP9EY75oc" # <--- PASTE YOUR GOOGLE API KEY
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # 2. OpenWeatherMap API Key
    OPENWEATHER_API_KEY = " 27d849c7479b45a9b91135215250708" # <--- PASTE YOUR WEATHER API KEY

except Exception as e:
    print(f"API Key Error: {e}")

# --- State flag to prevent listening loops ---
is_listening = False

# --- Weather Tool Function ---
def get_weather(location: str):
    """Gets current weather for a specified location using the OpenWeatherMap API."""
    if not OPENWEATHER_API_KEY or " 27d849c7479b45a9b91135215250708" in OPENWEATHER_API_KEY:
        return "Weather API key is not configured in the code."
    
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": location, "appid": OPENWEATHER_API_KEY, "units": "metric"}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        weather_data = response.json()
        
        if weather_data.get("cod") != 200:
            return f"Error: {weather_data.get('message', 'Could not find weather for that location.')}"

        city = weather_data.get("name")
        temp = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        humidity = weather_data["main"]["humidity"]
        
        # Return data as a JSON string for the AI model
        return json.dumps({
            "location": city, "temperature_celsius": f"{temp}°C",
            "description": description, "humidity": f"{humidity}%"
        })

    except Exception as e:
        return f"An error occurred while fetching weather: {e}"

# --- Configure Gemini Model with the Weather Tool ---
try:
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash-latest',
        tools=[get_weather] # Tell the model about the tool it can use
    )
    # Enable automatic function calling
    chat_session = model.start_chat(enable_automatic_function_calling=True)
except Exception as e:
    print(f"Error configuring Google AI model: {e}")
    model = None

# --- Text-to-Speech Setup ---
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[0].id)
engine.setProperty('rate', 160)

def speak(text):
    """Run text-to-speech in a separate thread to avoid freezing the GUI."""
    def run_speak():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run_speak, daemon=True).start()

# --- GUI Setup ---
root = tk.Tk()
root.title("Gemini AI Bot Assistant")
root.geometry("450x600")
root.configure(bg="#f0f0f0")
default_font = font.nametofont("TkDefaultFont")
default_font.configure(family="Arial", size=11)

# --- Core Behavior ---
def insert_chat(actor, message):
    """Inserts a message into the chat log with proper formatting."""
    chat_log.config(state="normal")
    if actor == "Bot":
        chat_log.insert(tk.END, f"Bot: {message}\n\n", "bot_message")
    else:
        chat_log.insert(tk.END, f"You: {message}\n", "user_message")
    chat_log.config(state="disabled")
    chat_log.see(tk.END)

def get_ai_response(user_input):
    """Handles the full conversation with the Gemini API, including tool calls."""
    try:
        # Send message to the model. Automatic function calling handles the rest.
        response = chat_session.send_message(user_input)
        final_text = response.text
        insert_chat("Bot", final_text)
        speak(final_text)

    except Exception as e:
        error_message = f"Sorry, an error occurred with the AI model: {e}"
        print(error_message)
        insert_chat("Bot", error_message)

def send_message(event=None):
    """Handles sending a message from the entry box."""
    user_input = entry.get().strip()
    if not user_input: return
    insert_chat("You", user_input)
    entry.delete(0, tk.END)

    if user_input.lower() == "quit":
        speak("Goodbye!")
        root.after(1000, root.destroy)
        return

    if not model:
        insert_chat("Bot", "AI model is not configured. Please check your API keys.")
        return
        
    # Run the conversation in a thread to keep the GUI responsive
    threading.Thread(target=get_ai_response, args=(user_input,), daemon=True).start()

def voice_input():
    """Handles voice input, preventing loops with a state flag."""
    global is_listening

    if is_listening:
        print("Already listening, please wait.")
        return # Exit if a listening session is already active

    is_listening = True # Set the flag to block other requests

    def run_listen():
        global is_listening
        r = sr.Recognizer()
        with sr.Microphone() as source:
            insert_chat("Bot", "Listening...")
            root.update_idletasks()
            r.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = r.listen(source, timeout=5)
                user_input = r.recognize_google(audio)
                root.after(0, lambda: entry.delete(0, tk.END))
                root.after(0, lambda: entry.insert(0, user_input))
                root.after(100, send_message)
            except sr.UnknownValueError:
                insert_chat("Bot", "Sorry, I couldn't understand that.")
            except sr.RequestError:
                insert_chat("Bot", "Network error. Please check your internet connection.")
            except sr.WaitTimeoutError:
                insert_chat("Bot", "Listening timed out. Please try again.")
            finally:
                # CRUCIAL: Always reset the flag when finished so you can listen again.
                is_listening = False

    threading.Thread(target=run_listen, daemon=True).start()

# --- Widget Layout ---
chat_log = tk.Text(root, bd=1, bg="#EAE6E6", font=("Arial", 12), state="disabled", wrap=tk.WORD, padx=5, pady=5)
chat_log.tag_configure("user_message", foreground="#007bff", font=("Arial", 12, "bold"))
chat_log.tag_configure("bot_message", foreground="#202124")
chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

bottom_frame = tk.Frame(root, bg="#f0f0f0")
bottom_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

entry = tk.Entry(bottom_frame, font=("Arial", 12))
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
entry.bind("<Return>", send_message)

send_button = tk.Button(bottom_frame, text="➤", font=("Arial", 16, "bold"), bg="#007bff", fg="white", command=send_message, width=3, relief=tk.FLAT)
send_button.pack(side=tk.LEFT, padx=(8, 0))

voice_button = tk.Button(bottom_frame, text="🎤", font=("Arial", 16), bg="#28a745", fg="white", command=voice_input, width=3, relief=tk.FLAT)
voice_button.pack(side=tk.LEFT, padx=(5, 0))

# --- Start the application ---
root.mainloop()