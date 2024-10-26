import pandas as pd
from datetime import datetime
import glob
import json
import os
import re
import html
# Function to convert the original arrival time to human-friendly format
def format_time(iso_time):
    dt = datetime.fromisoformat(iso_time.replace('Z', '+00:00'))
    return dt.strftime("%Y-%m-%d %H:%M:%S")

# Function to display the chat conversation in a human-friendly format
def format_chat_log(conversation):
    chat_log = []
    
    # Message list formatted as conversation
    message_list = conversation.get('MessageList', [])
    
    for message in message_list:
        # Format the time for each message
        time = format_time(message.get('originalarrivaltime', 'N/A'))
        
        # Get the sender's name (use the displayName if available, or ID)
        from_id = message.get('from', 'Unknown')
        sender_name = "Andrey" if from_id == "8:andrey.0404" else conversation.get('displayName', 'Unknown')

        # Display the message content in a chat format
        # content = message.get('content', '[No content]')
        # Get the content of the message, decode any HTML entities
        content = html.unescape(message.get('content', '[No content]'))  # HTML decoding
        
        # Append a dictionary representing this message to the chat log
        chat_log.append({"Time": time, "Sender": sender_name, "Message": content})
    
    return chat_log
# Function to sanitize the file name by replacing special characters with underscores
def sanitize_file_name(name):
    # Ensure the name is a string and replace None with an empty string
    if name is None:
        name = ''
    
    # Replace any non-alphanumeric characters with underscores
    return re.sub(r'[^\w\s-]', '_', name).replace(' ', '_')

# Function to export each conversation to an Excel file
def export_conversation_to_excel(conversation):
    # Get conversation ID or display name to use for the file name
    conversation_id = conversation.get('id', 'Unknown')
    display_name = conversation.get('displayName', 'Conversation')
    # Sanitize the file name
    safe_display_name = sanitize_file_name(display_name)
    safe_conversation_id = sanitize_file_name(conversation_id)
    
    # Prepare file name (conversation_id or display_name as the file name)
    file_name = f"{safe_display_name}_{safe_conversation_id}.xlsx"
    
    # Prepare file name (conversation_id or display_name as the file name)
    # file_name = f"{display_name.replace(' ', '_')}_{conversation_id}.xlsx"
    
    # Format the chat log for this conversation
    chat_log = format_chat_log(conversation)
    
    # Convert the list of messages to a pandas DataFrame
    df = pd.DataFrame(chat_log)
    
    # Export the DataFrame to Excel
    df.to_excel(file_name, index=False, engine='openpyxl')
    print(f"Exported conversation to {file_name}")
def get_input_with_default(prompt, default_value):
    user_input = input(f"{prompt} (default: {default_value}): ")
    
    # If the user presses Enter without input, return the default value
    if not user_input:
        return default_value
    return user_input
# Main function to run the CLI
# Function to load conversations from a JSON file
def load_conversations(file_path):
    try:
        with open(file_path, 'r') as file:
            conversations = json.load(file)
        return conversations
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None

# Main function to demonstrate
def main():
    path = os.getcwd() + '/input/*.json'
    files = glob.glob(path)
    for file in files:
        print(file)
    file_path = get_input_with_default("Enter the path to the JSON file: ", files[0])
    conversations = load_conversations(file_path)

    if conversations is None:
        return
    conversations=conversations['conversations']
    # Loop through conversations and export each one
    for conversation in conversations:
        export_conversation_to_excel(conversation)

if __name__ == "__main__":
    main()
