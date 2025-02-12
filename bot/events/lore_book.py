import os
import pymysql
import re
from collections import Counter
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from datetime import date

# Initialize GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")         
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()

# Database credentials
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME2 = os.getenv("DB_NAME2")

# Connect to the database
try:
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME2
    )
except pymysql.MySQLError as e:
    print("Error connecting to the database:", e)
    exit(1)

# Extract daily themes from chat logs
def extract_themes(messages):
    words = re.findall(r'\b\w+\b', ' '.join(messages).lower())
    word_counts = Counter(words)
    common_themes = [word for word, count in word_counts.items() if count > 3 and len(word) > 3]
    return common_themes[:5]

# Fetch today's chat messages from the database
def fetch_chat_logs():
    with connection.cursor() as cursor: 
        cursor.execute("SELECT message FROM chat_logs WHERE date = %s", (date.today(),))
        messages = [row[0] for row in cursor.fetchall()]
    return messages

# Add this function to your main script
def store_chat_log(username, message):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO chat_logs (username, message) VALUES (%s, %s)",
                (username, message)
            )
        connection.commit()
    except pymysql.MySQLError as e:
        print("Error storing chat log:", e)


# Generate lore entry based on themes
def generate_lore_entry(themes):
    # Format the prompt based on extracted themes
    prompt = (
        f"In the land of [Server Name], the factions have been stirring. Recently, there has been talk of {', '.join(themes)}. "
        "Create a new lore entry for today that ties these discussions into the story of the server."
    )
    
    # Encode the prompt and generate a response
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(input_ids, max_length=200, num_return_sequences=1, temperature=0.7)
    
    # Decode the generated text
    lore_entry = tokenizer.decode(output[0], skip_special_tokens=True)
    return lore_entry

# Store generated lore in the database
def store_lore_entry(themes, lore_entry):
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO lore_entries (date, themes, lore) VALUES (%s, %s, %s)",
            (date.today(), ', '.join(themes), lore_entry)
        )
    connection.commit()

# Main function to perform daily lore generation
def daily_lore_update():
    messages = fetch_chat_logs()
    if not messages:
        print("No chat logs found for today.")
        return
    
    themes = extract_themes(messages)
    if not themes:
        print("No significant themes found in today's chat logs.")
        return

    lore_entry = generate_lore_entry(themes)
    store_lore_entry(themes, lore_entry)
    print("New lore entry generated and stored in the database.")


# Run the daily lore update and close the connection after
try:
    daily_lore_update()
finally:
    connection.close()
