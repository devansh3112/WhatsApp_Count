# Development Guide

This document provides information for developers who want to extend or modify the WhatsApp Chat Analyzer.

## Project Structure

```
whatsapp-chat-analyzer/
├── whatsapp_analyzer.py     # Basic analyzer script
├── deep_whatsapp_analyzer.py # Advanced analyzer with visualizations
├── requirements.txt         # Python dependencies
├── sample_chat.txt          # Example chat file for testing
├── docs/                    # Documentation
│   ├── USAGE.md             # Detailed usage instructions
│   └── DEVELOPMENT.md       # This file
├── output/                  # Generated reports and visualizations
│   └── .gitkeep             # Ensures directory is tracked by git
├── README.md                # Project overview
├── LICENSE                  # MIT License
└── .gitignore               # Git ignore file
```

## Code Architecture

### Basic Analyzer (`whatsapp_analyzer.py`)

The basic analyzer implements core functionality:

1. `analyze_whatsapp_chat()`: Parses the chat file and counts messages per sender
2. `print_results()`: Displays message statistics in the console
3. `plot_results()`: Creates a simple bar chart visualization
4. `main()`: Entry point that handles user input and calls other functions

### Deep Analyzer (`deep_whatsapp_analyzer.py`)

The deep analyzer extends the basic functionality:

1. `analyze_whatsapp_chat()`: Enhanced version that extracts additional metrics
   - Message counts
   - Word frequency
   - Emoji usage
   - Media messages
   - Activity patterns (hourly, daily, timeline)
   - Message length stats

2. Visualization functions:
   - `plot_message_count()`: Bar chart of messages per sender
   - `plot_media_count()`: Bar chart of media messages per sender
   - `plot_hourly_activity()`: Line chart of messages by hour
   - `plot_weekday_activity()`: Bar chart of messages by weekday
   - `plot_activity_over_time()`: Timeline chart of activity
   - `plot_average_message_length()`: Bar chart of avg message length by sender
   - `generate_word_cloud()`: Word cloud of most common terms
   - `plot_emoji_usage()`: Bar chart of emoji frequency

3. `generate_statistics_report()`: Creates a comprehensive text report

## Regular Expression Pattern

The chat parsing relies on a regex pattern to extract message metadata:

```python
pattern = r'^(\d+/\d+/\d+),\s(\d+:\d+\s[ap]m)\s-\s([^:]+?)(?:\s\(.*?\))?:\s(.*)$'
```

This pattern matches:
1. Date (`\d+/\d+/\d+`): e.g., "13/04/22"
2. Time (`\d+:\d+\s[ap]m`): e.g., "9:15 am"
3. Sender name (`[^:]+?`): e.g., "John Doe"
4. Message content (`(.*)`): The actual message text

## Adding New Features

### 1. Sentiment Analysis

To add sentiment analysis:

1. Add the required dependency:
   ```bash
   pip install textblob
   ```

2. Import the library:
   ```python
   from textblob import TextBlob
   ```

3. Modify the `analyze_whatsapp_chat()` function:
   ```python
   # Add to data structures
   sentiment_scores = defaultdict(list)
   
   # Add to message parsing
   if text:
       blob = TextBlob(text)
       sentiment_scores[sender.strip()].append(blob.sentiment.polarity)
   
   # Calculate average sentiment per sender
   avg_sentiment = {sender: sum(scores)/len(scores) if scores else 0 
                    for sender, scores in sentiment_scores.items()}
   
   # Add to return value
   return {
       # ... existing items ...
       'avg_sentiment': avg_sentiment
   }
   ```

4. Create a visualization function:
   ```python
   def plot_sentiment_analysis(data, output_dir):
       sentiments = data['avg_sentiment']
       senders = list(sentiments.keys())
       scores = list(sentiments.values())
       
       plt.figure(figsize=(12, 8))
       bars = plt.bar(senders, scores, color='lightgreen')
       
       plt.axhline(y=0, color='r', linestyle='-', alpha=0.3)
       plt.xlabel('Group Members')
       plt.ylabel('Average Sentiment Score')
       plt.title('Sentiment Analysis by Member')
       plt.xticks(rotation=45, ha='right')
       plt.tight_layout()
       plt.savefig(f'{output_dir}/sentiment_analysis.png')
       plt.close()
   ```

### 2. Response Time Analysis

To analyze how quickly people respond to each other:

1. Track message timestamps in sequence
2. Calculate the time difference between messages
3. Filter for actual responses (e.g., messages that mention someone)
4. Visualize average response times

### 3. Topic Modeling

For identifying conversation themes:

1. Add required dependencies:
   ```bash
   pip install gensim nltk
   ```

2. Preprocess text (remove stopwords, lemmatize)
3. Apply LDA (Latent Dirichlet Allocation) topic modeling
4. Visualize topic distribution

## Testing

When adding new features, test with different types of chat exports:

1. Individual chats
2. Group chats with many members
3. Chats in different languages
4. Chats with various media types
5. Very large chat histories
6. Chats with different date/time formats

## Performance Optimization

For processing large chat files:

1. Consider using `pandas` for data manipulation
2. Implement batch processing for very large files
3. Use multiprocessing for parallel analysis
4. Add progress indicators for long-running operations

## Contributing Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature-name`)
3. Implement your changes
4. Add tests if applicable
5. Ensure code follows existing style
6. Update documentation to reflect changes
7. Submit a pull request

## Code Style

Follow these guidelines:

1. Use PEP 8 for Python code style
2. Add docstrings to all functions and classes
3. Use meaningful variable and function names
4. Keep functions small and focused on a single task
5. Comment complex logic 