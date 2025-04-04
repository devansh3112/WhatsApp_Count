# Detailed Usage Guide

## Exporting Your WhatsApp Chat

To analyze your WhatsApp conversations, you first need to export them from the app:

1. Open WhatsApp on your phone
2. Navigate to the chat/group you want to analyze 
3. Tap on the three dots (⋮) in the top-right corner
4. Select "More" → "Export chat"
5. Choose "Without Media" (for faster processing)
6. Select your preferred sharing method to get the file to your computer
   - Email, cloud storage, etc.

The export will be a text file with a name like "WhatsApp Chat with [Group/Contact Name].txt"

## Basic Analysis

For a quick overview of message counts by sender:

```bash
python whatsapp_analyzer.py
```

When prompted, enter the path to your exported chat file. The script will analyze the file and display:
- Message count per sender
- Percentage of total messages
- Total message count
- Most active group member

### Command Line Options

You can also specify the file path directly:

```bash
python whatsapp_analyzer.py --file "path/to/your/chat_export.txt"
```

## Deep Analysis

For comprehensive analysis with visualizations:

```bash
python deep_whatsapp_analyzer.py
```

The deep analyzer will:
1. Parse the entire chat history
2. Generate multiple visualizations
3. Create a detailed statistics report
4. Save all outputs to the `output` directory

### Customizing Analysis

You can customize the deep analysis by modifying parameters in the script:

- To change the number of top words shown:
  ```python
  # Change NUM_TOP_WORDS to your desired value
  NUM_TOP_WORDS = 15  # Default is 10
  ```

- To exclude specific words from word cloud:
  ```python
  # Add words to the STOPWORDS list
  STOPWORDS = ["the", "and", "is", ...]
  ```

- To change visualization styles:
  ```python
  # Modify plot parameters
  plt.figure(figsize=(14, 8))  # Larger figure size
  plt.style.use('dark_background')  # Different style
  ```

## Understanding the Results

### Message Count Visualization

Shows the number of messages sent by each chat participant, helping you identify the most active members.

### Media Count Analysis

Displays who shares the most media (images, videos, documents, etc.) in the chat.

### Hourly Activity

Shows message distribution by hour of the day, revealing when the chat is most active.

### Weekday Activity

Indicates which days of the week see the most chat activity.

### Activity Timeline

Tracks conversation volume over time, showing trends and patterns in engagement.

### Message Length Analysis

Compares average message length across participants, indicating who tends to write longer or shorter messages.

### Word Cloud

Visualizes the most frequently used words in the chat, with larger words appearing more often.

### Emoji Analysis

Shows which emojis are used most frequently in the conversation.

## Troubleshooting

### Encoding Issues

If you see garbled text or encoding errors:

```
UnicodeDecodeError: 'utf-8' codec can't decode byte...
```

Try specifying a different encoding when opening the file:

```python
with open(file_path, 'r', encoding='utf-16-le') as file:
```

WhatsApp exports can use different encodings depending on language and platform.

### Date Format Issues

If your date formats aren't being recognized, you may need to adjust the regex pattern in the script to match your locale's date format:

```python
# For DD/MM/YY format
pattern = r'^(\d+/\d+/\d+),\s(\d+:\d+\s[ap]m)\s-\s([^:]+?)(?:\s\(.*?\))?:\s(.*)$'

# For MM/DD/YY format
pattern = r'^(\d+/\d+/\d+),\s(\d+:\d+\s[ap]m)\s-\s([^:]+?)(?:\s\(.*?\))?:\s(.*)$'
```

### Performance with Large Files

For very large chat exports (several MB or larger):
- Consider using the `--sample` flag to analyze only a portion of the chat
- Increase system memory allocation if available
- Try splitting the analysis into smaller chunks 