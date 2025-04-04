from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="whatsapp-chat-analyzer",
    version="1.0.0",
    author="WhatsApp Chat Analyzer Team",
    author_email="example@example.com",
    description="A tool for analyzing and visualizing WhatsApp chat exports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/whatsapp-chat-analyzer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "matplotlib>=3.5.1",
        "numpy>=1.22.3",
        "emoji>=1.7.0",
        "wordcloud>=1.8.1",
    ],
    entry_points={
        "console_scripts": [
            "whatsapp-analyzer=whatsapp_analyzer:main",
            "whatsapp-deep-analyzer=deep_whatsapp_analyzer:main",
        ],
    },
) 