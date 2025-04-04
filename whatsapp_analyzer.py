import re
from collections import Counter
import matplotlib.pyplot as plt

def analyze_whatsapp_chat(file_path):
    # Updated regular expression to match the format in your file
    # Format: "DD/MM/YY, HH:MM am/pm - Sender: Message"
    pattern = r'^(\d+/\d+/\d+,\s\d+:\d+\s[ap]m)\s-\s([^:]+?)(?:\s\(.*?\))?:\s'
    
    # Counter to store the number of messages per sender
    message_count = Counter()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.match(pattern, line)
                if match:
                    sender = match.group(2).strip()
                    message_count[sender] += 1
    except UnicodeDecodeError:
        # If UTF-8 fails, try with another common encoding
        with open(file_path, 'r', encoding='utf-16') as file:
            for line in file:
                match = re.match(pattern, line)
                if match:
                    sender = match.group(2).strip()
                    message_count[sender] += 1
    
    # Filter out WhatsApp system messages
    if "Messages and calls are end-to-end encrypted" in message_count:
        del message_count["Messages and calls are end-to-end encrypted"]
    
    return message_count

def print_results(message_count):
    print("Message Count by Sender:")
    print("------------------------")
    
    # Sort by number of messages in descending order
    sorted_counts = sorted(message_count.items(), key=lambda x: x[1], reverse=True)
    
    total_messages = sum(count for _, count in sorted_counts)
    
    for sender, count in sorted_counts:
        percentage = (count / total_messages) * 100
        print(f"{sender}: {count} messages ({percentage:.1f}%)")
    
    print(f"\nTotal messages: {total_messages}")
    
    # Identify who sent the most messages
    if sorted_counts:
        most_active_sender, most_messages = sorted_counts[0]
        print(f"\nMost active member: {most_active_sender} with {most_messages} messages")

def plot_results(message_count):
    # Sort by number of messages in descending order
    sorted_counts = sorted(message_count.items(), key=lambda x: x[1], reverse=True)
    
    # Take top 10 senders if there are many
    if len(sorted_counts) > 10:
        sorted_counts = sorted_counts[:10]
        plt_title = "Top 10 Most Active Members"
    else:
        plt_title = "Message Count by Member"
    
    senders = [sender for sender, _ in sorted_counts]
    counts = [count for _, count in sorted_counts]
    
    plt.figure(figsize=(10, 6))
    plt.bar(senders, counts, color='skyblue')
    plt.xlabel('Group Members')
    plt.ylabel('Number of Messages')
    plt.title(plt_title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('whatsapp_analysis.png')
    plt.show()

def main():
    # Using the specific file path provided
    file_path = r"C:\Users\devan\whatsapp chat count\WhatsApp Chat with Ahmedabad Baila Assosiation (ABA).txt"

    message_count = analyze_whatsapp_chat(file_path)
    
    if not message_count:
        print("No messages found or incorrect file format.")
        return
    
    print_results(message_count)
    
    # Ask if user wants to plot the results
    plot_option = input("\nDo you want to generate a chart? (y/n): ")
    if plot_option.lower() == 'y':
        try:
            plot_results(message_count)
        except ImportError:
            print("Matplotlib not installed. Cannot generate chart.")
            print("Install it using: pip install matplotlib")

if __name__ == "__main__":
    main()