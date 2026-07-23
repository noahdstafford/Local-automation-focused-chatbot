import os
import json
# Pythons file operatiosn toolkit for moving files across folders
import shutil
from chat import ask_ollama


#Sets a variable pointing to the specific folder on your computer that you want to organise
organiser_access = 'test_sort'
# Looks in file and gives a list of all the names in an unorganised fromat
files_org = os.listdir(organiser_access)

# File for every file in the folder variable 
for file in files_org:
    # Prints name of the file currently being processed 
    print(file)

#Creates main function to, giving the messy list of files
def organise_files(files_org):
    # Prompt outline for ollama
    organiser_prompt = f"""You are a file organizing assistant. Given this list of files, suggest how to organize them.

You can suggest three types of actions:
- move: {{"action": "move", "file": "example.pdf", "destination": "Documents"}}
- rename: {{"action": "rename", "file": "old_name.txt", "new_name": "new_name.txt"}}
- delete: {{"action": "delete", "file": "unwanted_file.zip"}}

Respond ONLY with a JSON list of actions, no other text.

FILES:
{files_org}"""
    # Sends the specific files and instructions to AI
    organised_response = ask_ollama(organiser_prompt)
    # Sends the AI generated JSON response text back to script
    return organised_response

# Triggers the function above and saves the raw JSON text from the AI
organiser_result = organise_files(files_org)
# Prints raw AI response on screen 
print(f"\nFiles organised:\n{organiser_result}")
# Take sthe raw generated text by the AI and converts it to a stand python list of dictionaries so the code can interact with it 
actions = json.loads(organiser_result)

# Starts a loop to go through every single suggestion the AI made, one by one.
for action in actions:
    # Checks if the AI suggested moving a file
    if action["action"] == "move":
        # Builds the exact file path of where the file is currently sitting
        source_path = os.path.join(organiser_access, action["file"])
        # Builds the exact file path of the folder the AI wants to put it in
        destination_folder = os.path.join(organiser_access, action["destination"])
        # If the AI suggested a folder naem that doesnt exist yet this creates it 
        os.makedirs(destination_folder, exist_ok=True)
        # The actual moving. It picks the file up and drops it in the new folder
        shutil.move(source_path, destination_folder)
        # Adds a new line to the log just so the process it carried out can be check in the case of failure
        with open("organizer_log.txt", "a") as log:
            log.write(f"Moved {action['file']} to {action['destination']}\n")

    #Checks if the AI suggested renaming a file
    elif action["action"] == "rename":
        # Feature to ensure the permanent change can be check first by user via y/n
        confirm = input(f"Rename {action['file']} to {action['new_name']}? (y/n): ")
        if confirm.lower() == "y":
            # Finds the current file and the new name suggested and alters the file on the computers hard drive
            old_path = os.path.join(organiser_access, action["file"])
            new_path = os.path.join(organiser_access, action["new_name"])
            os.rename(old_path, new_path)
            # Adds a new line to the log just so the process it carried out can be check in the case of failure
            with open("organizer_log.txt", "a") as log:
                log.write(f"Renamed {action['file']} to {action['new_name']}\n")
        else:
            print("Skipped rename.")

    #Checks if the AI identified junk to delete
    elif action["action"] == "delete":
        # Makes user double check permanent decision
        confirm = input(f"Delete {action['file']}? (y/n): ")
        if confirm.lower() == "y":
            # If approved it locates the junk file and permanently deletes it from your system
            file_path = os.path.join(organiser_access, action["file"])
            os.remove(file_path)
            # Adds a new line to the log just so the process it carried out can be check in the case of failure
            with open("organizer_log.txt", "a") as log:
                log.write(f"Deleted {action['file']}\n")
        else:
            print("Skipped delete.")