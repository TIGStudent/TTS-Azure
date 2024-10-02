import os
import azure.cognitiveservices.speech as speechsdk
from datetime import datetime
from babel import Locale
import yaml

def main():
    speechConfig = speech_config()
    filename = set_file_name()
    voiceName = settings(speechConfig)
    inputText = get_input()
    print(voiceName)
    text_synthesis(speechConfig, filename, voiceName, inputText)

def settings(speechConfig):
    while True:
        with open('settings.yaml', 'r') as f:
            settings = yaml.safe_load(f)
        voice_value = settings.get('voice')

        os.system('cls')
        print(f'Current settings:\nVoice:\033[32m {voice_value} \033[0m')

        print('\nDo you want to change settings? \n1. Yes\n2. No')
        answer = input('\nAnswer: ')

        os.system('cls')
        if answer == '1':
            change_settings(speechConfig)
        elif answer == '2':
            return voice_value
        else:
            print('Answer must be 1 or 2!!!')

def change_settings(speechConfig):
    with open('settings.yaml', 'r') as f:
        settings = yaml.safe_load(f)

    settings['voice'] = list_available_voices(speechConfig)

    with open('settings.yaml', 'w') as file:
        yaml.dump(settings, file)

def get_input():
    file_path = 'input.txt'

    with open(file_path, 'r', encoding='utf-8') as file:
        text_from_input_file = file.read()
    os.system('cls')
    if text_from_input_file == '':
        print('\033[31minput text empty\033[0m')
        exit()
    print(text_from_input_file)
    print('\nContinue with above text?\n1. Yes\n2. No')
    Answer = input('\nAnswer: ')

    if Answer != '1':
        exit()

    return text_from_input_file

def set_file_name():
    current_time = datetime.now()
    time_string = current_time.strftime("%Y%m%d%H%M%S")
    fileName = f"output {time_string}.mp3"

    return fileName

def speech_config():
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    return speech_config

def get_locale_name(locale_code):
    try:
        codes = locale_code.split('-')
        code = codes[0] + '_' + codes[1]
        return Locale.parse(code).get_display_name('en_US')
    except:
        return locale_code

def list_available_voices(speech_config):
    """List available voices and let the user select one."""
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    voice_list = synthesizer.get_voices_async().get()

    if voice_list.reason == speechsdk.ResultReason.VoicesListRetrieved:
        regions = {voice.locale for voice in voice_list.voices}
        sorted_regions = sorted(regions)

        print("Available Regions:")
        for index, region in enumerate(sorted_regions):
            full_region_name = get_locale_name(region)
            print(f"{index + 1}: {full_region_name}")

        while True:
            try:
                region_choice = int(input("Select a region by number: ")) - 1
                if 0 <= region_choice < len(sorted_regions):
                    selected_region = sorted_regions[region_choice]
                    print(f"You selected region: {get_locale_name(selected_region)}")
                    break
                else:
                    print("Invalid choice. Please select a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        print("Available voices in the selected region:")
        filtered_voices = [voice for voice in voice_list.voices if voice.locale == selected_region]

        for index, voice in enumerate(filtered_voices):
            voice_name = f"{voice.locale}-{voice.name.split(' ')[-1].replace('Neural)', 'Neural')}"
            print(f"{index + 1}: Name: {voice_name}, Language: {voice.locale}, Gender: {voice.gender}")

        while True:
            try:
                choice = int(input("Select a voice by number: ")) - 1
                if 0 <= choice < len(filtered_voices):
                    selected_voice = filtered_voices[choice]
                    voice_name = f"{selected_voice.locale}-{selected_voice.name.split(' ')[-1].replace('Neural)', 'Neural')}"
                    print(f"You selected: {voice_name} ({selected_voice.locale})")
                    return voice_name
                else:
                    print("Invalid choice. Please select a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    else:
        print("Error retrieving voices:", voice_list.reason)
        return None

def chunk_text(text, max_length=5000):
    """Split text into chunks of max_length."""
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 2 <= max_length:  # +2 for ". "
            current_chunk += sentence + '. '
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + '. '

    if current_chunk:  # Add the last chunk
        chunks.append(current_chunk.strip())

    return chunks

def text_synthesis(speech_config, filename, voiceName, text):
    speech_config.speech_synthesis_voice_name = voiceName
    text_chunks = chunk_text(text)

    # Set up the audio output to save the synthesized speech to a file
    audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)

    # Create a SpeechSynthesizer with the specified audio output
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    for chunk in text_chunks:
        # Start synthesizing each chunk
        print(f"Synthesizing chunk: {chunk[:30]}...")  # Preview of the chunk
        speech_synthesis_result = speech_synthesizer.speak_text(chunk)  # Synthesize synchronously

        # Check if the synthesis is successful
        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Chunk synthesized successfully.")
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print(f"Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print(f"Error details: {cancellation_details.error_details}")
                    print("Did you set the speech resource key and region values?")

if __name__ == "__main__":
    main()
