# import requests
# from bs4 import BeautifulSoup
# import time
# import telebot
# import hashlib
#
# # Initialize the Telegram bot
# token = '1110616107:AAFVOX5bQdFkb7VeFAypG4-fzZ--C9OlreA'  # Replace with your bot token
# bot = telebot.TeleBot(token)
import requests
from bs4 import BeautifulSoup
import time
import telebot
import hashlib

# Initialize the Telegram bot
token = '1110616107:AAFVOX5bQdFkb7VeFAypG4-fzZ--C9OlreA'  # Replace with your bot token
bot = telebot.TeleBot(token)

url = 'https://www.opencve.io/cve'  # Replace with the actual URL
previous_content = ""  # Define the previous_content variable here


@bot.message_handler(commands=['start'])
def handle_start(message):
    global previous_content  # Use the global keyword to access the previous_content variable from outside the function
    while True:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            cve_entries = soup.find_all('tr', class_='cve-header')

            current_content = ""
            print(current_content)
            for entry in cve_entries:
                cve_number = entry.find('strong').text
                summary = entry.find_next_sibling('tr', class_='cve-summary')
                if summary:
                    description = summary.find('td', {'class': 'col-md-12', 'colspan': '5'}).text
                    current_content += f"{cve_number}: {description}\n"

            current_hash = hashlib.md5(current_content.encode('utf-8')).hexdigest()
            print(current_content)
            if current_content != previous_content:
                if len(current_content) > 1000:  # Adjust the threshold as needed
                    bot.send_message(message.chat.id,
                                     "Changes detected in CVE descriptions exceed maximum length. Please check manually.")
                else:
                    bot.send_message(message.chat.id, "Changes detected in CVE descriptions:\n" + current_content)
                previous_content = current_content

        else:
            bot.send_message(message.chat.id, "Failed to fetch data from the website")

        time.sleep(1800)  # Sleep for 30 minutes (1800 seconds)


bot.polling()