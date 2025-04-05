#!/usr/bin/env python3
import argparse
import os
import sys
import whatsapp_analyzer
import deep_whatsapp_analyzer


def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="WhatsApp Chat Analyzer - Extract insights from your WhatsApp chats"
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Basic analyzer
    basic_parser = subparsers.add_parser(
        "basic", help="Run basic message count analysis")
    basic_parser.add_argument(
        "--file", "-f", help="Path to WhatsApp chat export file")
    basic_parser.add_argument(
        "--plot", "-p", action="store_true", help="Generate visualization")

    # Deep analyzer
    deep_parser = subparsers.add_parser(
        "deep", help="Run comprehensive analysis with visualizations")
    deep_parser.add_argument(
        "--file", "-f", help="Path to WhatsApp chat export file")
    deep_parser.add_argument(
        "--output", "-o", default="output", help="Output directory for visualizations")
    deep_parser.add_argument("--format", choices=["png", "pdf", "svg"], default="png",
                             help="Image format for visualizations")
    deep_parser.add_argument(
        "--no-plots", action="store_true", help="Skip generating plots")

    # List sample chats
    subparsers.add_parser(
        "list-samples", help="List available sample chat files")

    # Version info
    subparsers.add_parser("version", help="Show version information")

    return parser.parse_args()


def run_basic_analyzer(args):
    """Run the basic analyzer with optional visualization"""
    if not args.file:
        file_path = input("Enter the path to your WhatsApp chat export: ")
    else:
        file_path = args.file

    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return

    message_count = whatsapp_analyzer.analyze_whatsapp_chat(file_path)

    if not message_count:
        print("No messages found or incorrect file format.")
        return

    whatsapp_analyzer.print_results(message_count)

    if args.plot:
        try:
            whatsapp_analyzer.plot_results(message_count)
            print("\nVisualization saved as 'whatsapp_analysis.png'")
        except ImportError:
            print("Error: Matplotlib not installed. Cannot generate chart.")
            print("Install it using: pip install matplotlib")


def run_deep_analyzer(args):
    """Run the comprehensive analyzer with visualizations"""
    if not args.file:
        file_path = input("Enter the path to your WhatsApp chat export: ")
    else:
        file_path = args.file

    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return

    # Create output directory if it doesn't exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    print(f"Analyzing chat: {file_path}")
    print("This may take a moment for large chats...")

    # Run the deep analysis
    data = deep_whatsapp_analyzer.analyze_whatsapp_chat(file_path)

    if not data['message_count']:
        print("No messages found or incorrect file format.")
        return

    # Generate statistics report
    report_path = os.path.join(args.output, "statistics_report.txt")
    deep_whatsapp_analyzer.generate_statistics_report(data, args.output)
    print(f"Statistics report saved to: {report_path}")

    # Generate visualizations
    if not args.no_plots:
        print("Generating visualizations...")
        deep_whatsapp_analyzer.plot_message_count(data, args.output)
        deep_whatsapp_analyzer.plot_media_count(data, args.output)
        deep_whatsapp_analyzer.plot_hourly_activity(data, args.output)
        deep_whatsapp_analyzer.plot_weekday_activity(data, args.output)
        deep_whatsapp_analyzer.plot_activity_over_time(data, args.output)
        deep_whatsapp_analyzer.plot_average_message_length(data, args.output)

        try:
            deep_whatsapp_analyzer.generate_word_cloud(data, args.output)
        except ImportError:
            print("Warning: WordCloud not installed. Skipping word cloud generation.")

        deep_whatsapp_analyzer.plot_emoji_usage(data, args.output)
        print(f"Visualizations saved to: {args.output}/")

    print("\nAnalysis complete!")


def list_samples():
    """List sample chat files in the repository"""
    print("Available sample chat files:")

    if os.path.exists("sample_chat.txt"):
        print("- sample_chat.txt (Example chat for testing)")

    # Check for more samples in a samples directory if it exists
    if os.path.exists("samples"):
        for file in os.listdir("samples"):
            if file.endswith(".txt"):
                print(f"- samples/{file}")

    print("\nTo use a sample file, run:")
    print("  python cli.py basic --file sample_chat.txt")
    print("  or")
    print("  python cli.py deep --file sample_chat.txt")


def show_version():
    """Show version information"""
    print("WhatsApp Chat Analyzer v1.0.0")
    print("https://github.com/yourusername/whatsapp-chat-analyzer")
    print("\nPython version:", sys.version)

    # Check for installed packages
    try:
        import matplotlib
        print("Matplotlib version:", matplotlib.__version__)
    except ImportError:
        print("Matplotlib: Not installed")

    try:
        import numpy
        print("NumPy version:", numpy.__version__)
    except ImportError:
        print("NumPy: Not installed")

    try:
        import emoji
        print("Emoji version:", emoji.__version__)
    except ImportError:
        print("Emoji: Not installed")

    try:
        import wordcloud
        print("WordCloud version:", wordcloud.__version__)
    except ImportError:
        print("WordCloud: Not installed")


def main():
    """Main entry point for the CLI"""
    args = parse_args()

    if args.command == "basic":
        run_basic_analyzer(args)
    elif args.command == "deep":
        run_deep_analyzer(args)
    elif args.command == "list-samples":
        list_samples()
    elif args.command == "version":
        show_version()
    else:
        # No command or invalid command - show help
        print("WhatsApp Chat Analyzer - Command Line Interface")
        print("===============================================")
        print("\nUse one of the following commands:")
        print("  python cli.py basic  - Run basic message count analysis")
        print("  python cli.py deep   - Run comprehensive analysis with visualizations")
        print("  python cli.py list-samples - List available sample chat files")
        print("  python cli.py version - Show version information")
        print("\nFor more options, use: python cli.py --help")


if __name__ == "__main__":
    main()
