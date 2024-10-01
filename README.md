# Azure Text-to-Speech Synthesizer

This project utilizes the Azure Cognitive Services Speech SDK to convert text from a file into speech and save it as an MP3 file. The application allows users to select a voice based on regional availability, and synthesizes the text using the chosen voice.

## Features

- Read text from an input file (`input.txt`).
- List available voices and their regions for selection.
- Convert the selected text to speech and save it as an MP3 file.
- Support for multiple languages and dialects.

## Prerequisites

Before running this project, make sure you have the following:

- Python 3.x installed.
- An Azure account with access to the Speech service.
- Your Speech service subscription key and region.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/repository-name.git
   cd repository-name
   ```

2. **Install required packages:**

   Make sure you have `azure-cognitiveservices-speech` and `babel` installed. You can install them using pip:

   ```bash
   pip install azure-cognitiveservices-speech babel
   ```

3. **Set up environment variables:**

   Set your Azure Speech service subscription key and region as environment variables:

   ```bash
   export SPEECH_KEY='your_speech_service_key'
   export SPEECH_REGION='your_speech_service_region'
   ```

   Replace `'your_speech_service_key'` and `'your_speech_service_region'` with your actual Speech service credentials.

## Usage

1. **Create an input text file:**

   Create a file named `input.txt` in the same directory as the script. Add the text you want to convert to speech in this file.

2. **Run the application:**

   Execute the main Python script:

   ```bash
   python your_script_name.py
   ```

   Replace `your_script_name.py` with the actual name of your Python file.

3. **Select a region and voice:**

   The application will display a list of available regions. Enter the number corresponding to your desired region. Then, it will show the voices available in that region for you to choose from.

4. **Output:**

   The synthesized speech will be saved as an MP3 file in the same directory with a filename format like `output_YYYYMMDDHHMMSS.mp3`, where `YYYYMMDDHHMMSS` represents the timestamp.

## Example

After executing the script and following the prompts, you should see output similar to this:

```
Available Regions:
1: English (United States)
2: Swedish (Sweden)
...

Select a region by number: 2
You selected region: Swedish (Sweden)

Available voices in the selected region:
1: Name: sv-SE-MattiasNeural, Language: sv-SE, Gender: Male
...

Select a voice by number: 1
You selected: sv-SE-MattiasNeural (sv-SE)
Speech synthesized and saved to [output_20231001010101.mp3]
```
