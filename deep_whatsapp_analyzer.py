import re
from collections import Counter, defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from wordcloud import WordCloud
import numpy as np
import emoji
import os


def analyze_whatsapp_chat(file_path):
    # Regular expression to match the format in your file
    pattern = r'^(\d+/\d+/\d+),\s(\d+:\d+\s[ap]m)\s-\s([^:]+?)(?:\s\(.*?\))?:\s(.*)$'

    # Data structures for various analytics
    message_count = Counter()
    word_count = Counter()
    emoji_count = Counter()
    media_count = Counter()
    hourly_activity = Counter()
    weekday_activity = Counter()
    date_activity = defaultdict(int)
    message_lengths = defaultdict(list)
    all_text = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Split by new message pattern (date at beginning of line)
            messages = re.split(r'\n(?=\d+/\d+/\d+)', content)

            for message in messages:
                match = re.match(pattern, message, re.DOTALL)
                if match:
                    date_str, time_str, sender, text = match.groups()

                    # Parse date and time
                    try:
                        date_obj = datetime.strptime(
                            f"{date_str}, {time_str}", "%d/%m/%y, %I:%M %p")

                        # Count messages by sender
                        message_count[sender.strip()] += 1

                        # Count messages by hour
                        hour = date_obj.hour
                        hourly_activity[hour] += 1

                        # Count messages by weekday
                        weekday = date_obj.strftime('%A')
                        weekday_activity[weekday] += 1

                        # Count messages by date
                        date_only = date_obj.strftime('%Y-%m-%d')
                        date_activity[date_only] += 1

                        # Word analysis
                        if text:
                            # Check for media messages
                            if "<Media omitted>" in text or "image omitted" in text or "video omitted" in text:
                                media_count[sender.strip()] += 1
                            else:
                                # Count words
                                words = text.split()
                                word_count.update(words)

                                # Store message length
                                message_lengths[sender.strip()].append(
                                    len(words))

                                # Store text for word cloud
                                all_text.append(text)

                                # Count emojis
                                for char in text:
                                    if char in emoji.EMOJI_DATA:
                                        emoji_count[char] += 1
                    except ValueError:
                        # Skip messages with invalid date formats
                        pass
    except UnicodeDecodeError:
        # If UTF-8 fails, try with another encoding
        with open(file_path, 'r', encoding='utf-16') as file:
            # Repeat the same analysis...
            content = file.read()
            # Split by new message pattern
            messages = re.split(r'\n(?=\d+/\d+/\d+)', content)

            for message in messages:
                match = re.match(pattern, message, re.DOTALL)
                if match:
                    # Same processing as above...
                    date_str, time_str, sender, text = match.groups()

                    try:
                        date_obj = datetime.strptime(
                            f"{date_str}, {time_str}", "%d/%m/%y, %I:%M %p")
                        message_count[sender.strip()] += 1
                        hour = date_obj.hour
                        hourly_activity[hour] += 1
                        weekday = date_obj.strftime('%A')
                        weekday_activity[weekday] += 1
                        date_only = date_obj.strftime('%Y-%m-%d')
                        date_activity[date_only] += 1

                        if text:
                            if "<Media omitted>" in text or "image omitted" in text or "video omitted" in text:
                                media_count[sender.strip()] += 1
                            else:
                                words = text.split()
                                word_count.update(words)
                                message_lengths[sender.strip()].append(
                                    len(words))
                                all_text.append(text)

                                for char in text:
                                    if char in emoji.EMOJI_DATA:
                                        emoji_count[char] += 1
                    except ValueError:
                        pass

    # Calculate average message length by sender
    avg_message_lengths = {sender: sum(lengths)/len(lengths) if lengths else 0
                           for sender, lengths in message_lengths.items()}

    # Combine all text for word cloud
    all_text_combined = ' '.join(all_text)

    return {
        'message_count': message_count,
        'word_count': word_count,
        'emoji_count': emoji_count,
        'media_count': media_count,
        'hourly_activity': hourly_activity,
        'weekday_activity': weekday_activity,
        'date_activity': date_activity,
        'avg_message_length': avg_message_lengths,
        'all_text': all_text_combined
    }


def create_output_directory():
    """Create an 'output' directory if it doesn't exist"""
    if not os.path.exists('output'):
        os.makedirs('output')
    return 'output'


def plot_message_count(data, output_dir):
    sorted_counts = sorted(
        data['message_count'].items(), key=lambda x: x[1], reverse=True)

    # Take top 15 senders if there are many
    if len(sorted_counts) > 15:
        sorted_counts = sorted_counts[:15]
        plt_title = "Top 15 Most Active Members"
    else:
        plt_title = "Message Count by Member"

    senders = [sender for sender, _ in sorted_counts]
    counts = [count for _, count in sorted_counts]

    plt.figure(figsize=(12, 8))
    bars = plt.bar(senders, counts, color='skyblue')

    # Add count labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f'{int(height)}', ha='center', va='bottom')

    plt.xlabel('Group Members')
    plt.ylabel('Number of Messages')
    plt.title(plt_title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/message_count.png')
    plt.close()


def plot_media_count(data, output_dir):
    sorted_counts = sorted(data['media_count'].items(),
                           key=lambda x: x[1], reverse=True)

    # Take top 10 senders
    if len(sorted_counts) > 10:
        sorted_counts = sorted_counts[:10]

    senders = [sender for sender, _ in sorted_counts]
    counts = [count for _, count in sorted_counts]

    plt.figure(figsize=(12, 8))
    bars = plt.bar(senders, counts, color='lightgreen')

    # Add count labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f'{int(height)}', ha='center', va='bottom')

    plt.xlabel('Group Members')
    plt.ylabel('Number of Media Messages')
    plt.title('Media Messages by Member')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/media_count.png')
    plt.close()


def plot_hourly_activity(data, output_dir):
    hours = range(24)
    counts = [data['hourly_activity'][hour] for hour in hours]

    plt.figure(figsize=(12, 6))
    plt.bar(hours, counts, color='salmon')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Messages')
    plt.title('Group Activity by Hour')
    plt.xticks(hours)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/hourly_activity.png')
    plt.close()


def plot_weekday_activity(data, output_dir):
    # Get weekday order right
    days = ['Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday']
    counts = [data['weekday_activity'][day] for day in days]

    plt.figure(figsize=(12, 6))
    plt.bar(days, counts, color='lightcoral')
    plt.xlabel('Day of Week')
    plt.ylabel('Number of Messages')
    plt.title('Group Activity by Day of Week')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/weekday_activity.png')
    plt.close()


def plot_activity_over_time(data, output_dir):
    dates = sorted(data['date_activity'].keys())
    counts = [data['date_activity'][date] for date in dates]

    # Convert string dates to datetime objects
    date_objects = [datetime.strptime(date, '%Y-%m-%d') for date in dates]

    plt.figure(figsize=(14, 6))
    plt.plot(date_objects, counts, marker='o',
             linestyle='-', color='royalblue')
    plt.xlabel('Date')
    plt.ylabel('Number of Messages')
    plt.title('Group Activity Over Time')

    # Format x-axis to show dates nicely
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/activity_timeline.png')
    plt.close()


def plot_average_message_length(data, output_dir):
    sorted_lengths = sorted(
        data['avg_message_length'].items(), key=lambda x: x[1], reverse=True)

    # Take top 15
    if len(sorted_lengths) > 15:
        sorted_lengths = sorted_lengths[:15]

    senders = [sender for sender, _ in sorted_lengths]
    lengths = [length for _, length in sorted_lengths]

    plt.figure(figsize=(12, 8))
    bars = plt.bar(senders, lengths, color='mediumpurple')

    # Add length labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f'{height:.1f}', ha='center', va='bottom')

    plt.xlabel('Group Members')
    plt.ylabel('Average Words per Message')
    plt.title('Average Message Length by Member')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/avg_message_length.png')
    plt.close()


def generate_word_cloud(data, output_dir):
    # Filter out common WhatsApp and common words
    text = data['all_text']

    # List of common words to exclude
    stopwords = set([
        "the", "and", "to", "of", "in", "a", "is", "that", "for", "on", "with",
        "as", "this", "by", "an", "are", "at", "be", "but", "or", "have", "it",
        "from", "you", "was", "not", "what", "all", "they", "when", "we", "there",
        "can", "no", "yes", "Media", "omitted", "hai", "he", "che", "ne", "ma"
    ])

    # Create and generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white',
                          stopwords=stopwords, max_words=100,
                          collocations=False).generate(text)

    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(f'{output_dir}/wordcloud.png')
    plt.close()


def plot_emoji_usage(data, output_dir):
    emoji_counts = data['emoji_count']

    if not emoji_counts:
        return  # Skip if no emojis found

    # Get top 15 emojis
    top_emojis = sorted(emoji_counts.items(),
                        key=lambda x: x[1], reverse=True)[:15]
    emojis = [emoji for emoji, _ in top_emojis]
    counts = [count for _, count in top_emojis]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(emojis, counts, color='gold')

    # Add count labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f'{int(height)}', ha='center', va='bottom')

    plt.xlabel('Emoji')
    plt.ylabel('Count')
    plt.title('Top 15 Most Used Emojis')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/emoji_usage.png')
    plt.close()


def generate_statistics_report(data, output_dir):
    with open(f'{output_dir}/statistics_report.txt', 'w', encoding='utf-8') as f:
        # General statistics
        total_messages = sum(data['message_count'].values())
        total_members = len(data['message_count'])

        f.write("===== WhatsApp Chat Analysis Report =====\n\n")
        f.write(f"Total Messages: {total_messages}\n")
        f.write(f"Total Group Members: {total_members}\n\n")

        # Most active members
        f.write("Top 5 Most Active Members:\n")
        sorted_members = sorted(
            data['message_count'].items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (member, count) in enumerate(sorted_members, 1):
            percentage = (count / total_messages) * 100
            f.write(f"{i}. {member}: {count} messages ({percentage:.1f}%)\n")

        f.write("\n")

        # Media statistics
        total_media = sum(data['media_count'].values())
        f.write(f"Total Media Messages: {total_media}\n")
        if total_media > 0:
            media_percentage = (total_media / total_messages) * 100
            f.write(f"Media Messages Percentage: {media_percentage:.1f}%\n")

            f.write("\nTop 3 Media Senders:\n")
            sorted_media = sorted(
                data['media_count'].items(), key=lambda x: x[1], reverse=True)[:3]
            for i, (member, count) in enumerate(sorted_media, 1):
                percentage = (count / total_media) * 100
                f.write(
                    f"{i}. {member}: {count} media messages ({percentage:.1f}%)\n")

        f.write("\n")

        # Activity patterns
        most_active_hour = max(
            data['hourly_activity'].items(), key=lambda x: x[1])[0]
        most_active_day = max(
            data['weekday_activity'].items(), key=lambda x: x[1])[0]

        f.write(
            f"Most Active Hour: {most_active_hour}:00 - {most_active_hour+1}:00\n")
        f.write(f"Most Active Day: {most_active_day}\n\n")

        # Message length statistics
        if data['avg_message_length']:
            avg_lengths = data['avg_message_length']
            overall_avg = sum(avg_lengths.values()) / len(avg_lengths)
            max_avg = max(avg_lengths.items(), key=lambda x: x[1])

            f.write(
                f"Overall Average Message Length: {overall_avg:.1f} words\n")
            f.write(
                f"Member with Longest Messages: {max_avg[0]} ({max_avg[1]:.1f} words on average)\n\n")

        # Word statistics
        if data['word_count']:
            total_words = sum(data['word_count'].values())
            f.write(f"Total Words: {total_words}\n")

            f.write("\nTop 10 Most Used Words:\n")
            # Filter out very short words
            filtered_words = {word: count for word,
                              count in data['word_count'].items() if len(word) > 2}
            top_words = sorted(filtered_words.items(),
                               key=lambda x: x[1], reverse=True)[:10]
            for i, (word, count) in enumerate(top_words, 1):
                f.write(f"{i}. {word}: {count} times\n")

        f.write("\n")

        # Emoji statistics
        if data['emoji_count']:
            total_emojis = sum(data['emoji_count'].values())
            f.write(f"Total Emojis: {total_emojis}\n")

            f.write("\nTop 5 Most Used Emojis:\n")
            top_emojis = sorted(data['emoji_count'].items(
            ), key=lambda x: x[1], reverse=True)[:5]
            for i, (emoji_char, count) in enumerate(top_emojis, 1):
                f.write(f"{i}. {emoji_char}: {count} times\n")


def main():
    file_path = os.getenv("FILE_PATH")

    print("Analyzing chat data...")
    data = analyze_whatsapp_chat(file_path)

    if not data['message_count']:
        print("No messages found or incorrect file format.")
        return

    # Create output directory
    output_dir = create_output_directory()
    print(f"Output will be saved to '{output_dir}' directory")

    # Generate all plots and reports
    print("Generating reports and visualizations...")

    # Basic message analysis
    plot_message_count(data, output_dir)

    # Media analysis
    if data['media_count']:
        plot_media_count(data, output_dir)

    # Activity patterns
    plot_hourly_activity(data, output_dir)
    plot_weekday_activity(data, output_dir)
    plot_activity_over_time(data, output_dir)

    # Message length analysis
    if data['avg_message_length']:
        plot_average_message_length(data, output_dir)

    # Word analysis
    if data['all_text']:
        try:
            generate_word_cloud(data, output_dir)
        except ImportError:
            print("WordCloud package not installed. Skipping word cloud generation.")

    # Emoji analysis
    if data['emoji_count']:
        try:
            plot_emoji_usage(data, output_dir)
        except ImportError:
            print("Emoji package not installed. Skipping emoji analysis.")

    # Generate text report
    generate_statistics_report(data, output_dir)

    print("\nAnalysis complete! You can find all results in the 'output' directory.")
    print("\nHere's a summary of most active members:")

    # Display a simple summary
    sorted_counts = sorted(
        data['message_count'].items(), key=lambda x: x[1], reverse=True)
    total_messages = sum(count for _, count in sorted_counts)

    for i, (sender, count) in enumerate(sorted_counts[:5], 1):
        percentage = (count / total_messages) * 100
        print(f"{i}. {sender}: {count} messages ({percentage:.1f}%)")


if __name__ == "__main__":
    main()
