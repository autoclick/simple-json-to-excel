import glob
import json
import os
from datetime import datetime

# Function to convert the original arrival time to human-friendly format
def format_time(iso_time):
    dt = datetime.fromisoformat(iso_time.replace('Z', '+00:00'))
    return dt.strftime("%Y-%m-%d %H:%M:%S")

# Function to display the chat conversation in a human-friendly format
def display_chat_log(conversation):
    print(f"Conversation with: SKYPE ID: {conversation.get('id')} ({conversation.get('displayName', 'Unknown')})")
    
    # Properties (displaying last received message time)
    properties = conversation.get('properties', {})
    print(f"Last message received: {properties.get('lastimreceivedtime', 'N/A')}\n")

    # Message list formatted as conversation
    message_list = conversation.get('MessageList', [])
    
    for message in message_list:
        # Format the time for each message
        time = format_time(message.get('originalarrivaltime', 'N/A'))
        
        # Get the sender's name (use the displayName if available, or ID)
        from_id = message.get('from', 'Unknown')
        sender_name = conversation.get('displayName', 'Unknown')
        sender_id = conversation.get('id', 'Unknown')

        # Display the message content in a chat format
        content = message.get('content', '[No content]')
        
        # Output in human-friendly format
        print(f"[{time}] SKYPE ID:==={from_id}===: {content}\n")
# Function to load conversations from a JSON file
def load_conversations(file_path):
    try:
        with open(file_path, 'r') as file:
            conversations = json.load(file)
        return conversations
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None

# Function to display menu of conversations
def display_menu(conversations):
    based=len(conversations)-1
    print(f"Select a conversation by index(0-{based}):")
    for idx, conversation in enumerate(conversations):
        print(f"SKYPE ID: {idx} ({conversation.get('displayName', 'Unknown')})")
    print("Enter 'q' to quit.")

def display_conversation(conversation):
    print(f"ID: {conversation.get('id')}")
    print(f"Display Name: {conversation.get('displayName')}")
    print(f"Version: {conversation.get('version')}")
    
    # Properties (if needed)
    properties = conversation.get('properties', {})
    print(f"Last IM Received Time: {properties.get('lastimreceivedtime')}")
    print(f"Conversation Status: {properties.get('conversationstatus')}")
    
    # Thread Properties - Check if threadProperties exists before accessing members
    thread_properties = conversation.get('threadProperties', None)
    
    if thread_properties:
        members = thread_properties.get('members', [])
        print("\nMembers:")
        if members:
            for idx, member in enumerate(members):
                print(f"{idx + 1}. {member}")
        else:
            print("No members found.")
    else:
        print("No thread properties available.")
def get_input_with_default(prompt, default_value):
    user_input = input(f"{prompt} (default: {default_value}): ")
    
    # If the user presses Enter without input, return the default value
    if not user_input:
        return default_value
    return user_input
# Main function to run the CLI
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
    user_input="0"
    while True:
        display_menu(conversations)
        
        try:
            index = int(user_input)
            print(f"Conversations Index: {index}")
            if 0 <= index < len(conversations):
                display_chat_log(conversations[index])
            else:
                print("Invalid index, please try again.")
        except ValueError:
            print("Invalid input, please enter a number.")
        based=len(conversations)-1
        print(f"Select a conversation by index(0-{based}) - List SKYPE Name ID on Top of Screen:")
        user_input = input("Enter conversation index or 'q' to quit: ")
        
        if user_input.lower() == 'q':
            print("Exiting program.")
            break

if __name__ == "__main__":
    main()