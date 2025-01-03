import os
import pandas as pd
from datetime import datetime

def parse_txt_to_csv(txt_folder, output_csv):
    data = []
    
    # Iterate through all text files in the export folder
    for filename in os.listdir(txt_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(txt_folder, filename)
            
            # Open and read the conversation text file
            with open(filepath, "r") as file:
                for line in file:
                    # Parse each line for timestamp, sender, and message
                    try:
                        # Example line format: "[2025-01-01 12:00:00] Sender: Message content"
                        parts = line.strip().split(" ", 2)
                        timestamp = " ".join(parts[:2]).strip("[]")
                        sender_message = parts[2].split(": ", 1)
                        sender = sender_message[0]
                        message = sender_message[1] if len(sender_message) > 1 else ""
                        
                        # Append to data list
                        data.append({"timestamp": timestamp, "sender": sender, "message": message})
                    except Exception as e:
                        print(f"Skipping line due to error: {line}")
                        continue

    # Convert data to DataFrame
    df = pd.DataFrame(data)
    
    # Format timestamps (if necessary)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    
    # Save DataFrame to CSV
    df.to_csv(output_csv, index=False)
    print(f"CSV file created: {output_csv}")

# Define the folder containing TXT files and the output CSV file
txt_folder = os.path.expanduser("~/imessage_export")
output_csv = os.path.expanduser("~/Desktop/imessage_export.csv")

# Run the conversion
parse_txt_to_csv(txt_folder, output_csv)
