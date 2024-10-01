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
            print(f'Current settings:\nVocie:\033[32m {voice_value} \033[0m')

            print('\nDo you want to change settings? \n1. Yes\n2. No')
            answer = input('\nAnswer: ')

            os.system('cls')
            if answer == '1':
                change_settings(speechConfig)
            elif answer == '2':
                return voice_value
            else:
                print('Answer most be 1 or 2!!!')
                
    
        input('stop')

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
    if text_from_input_file =='':
        print('\033[31minput text empty\033[0m')
        exit()
    print(text_from_input_file)
    print('\nContinue with above text?\n1. Yes\n2. No')
    Answer = input('\nAnswer: ')

    if Answer != 1:
        exit()

    return text_from_input_file

def set_file_name():
    current_time = datetime.now()
    time_string = current_time.strftime("%Y%m%d%H%M%S")
    fileName = f"output {time_string}.mp3"

    return  fileName

def speech_config():
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))

    return speech_config

def get_locale_name(locale_code):
    try:
        codes =  locale_code.split('-') 
        code = codes[0]+'_'+codes[1]
        return Locale.parse(code).get_display_name('en_US')
    except:
        return locale_code

def list_available_voices(speech_config):
    """List available voices and let the user select one."""
    # Create a SpeechSynthesizer instance to retrieve voices
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    voice_list = synthesizer.get_voices_async().get()  # Get voices using the synthesizer

    if voice_list.reason == speechsdk.ResultReason.VoicesListRetrieved:
        # Store unique locales from the available voices in a set
        regions = {voice.locale for voice in voice_list.voices}

        # Convert the set to a sorted list
        sorted_regions = sorted(regions)

        print("Available Regions:")
        for index, region in enumerate(sorted_regions):
            full_region_name = get_locale_name(region)
            print(f"{index + 1}: {full_region_name}")

        # Get the user's selected region
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

        # Now filter voices by the selected region
        print("Available voices in the selected region:")
        filtered_voices = [voice for voice in voice_list.voices if voice.locale == selected_region]

        for index, voice in enumerate(filtered_voices):
            # Extract only the name and locale in the desired format
            voice_name = f"{voice.locale}-{voice.name.split(' ')[-1].replace('Neural)', 'Neural')}"  # Adjust for Neural
            print(f"{index + 1}: Name: {voice_name}, Language: {voice.locale}, Gender: {voice.gender}")

        # Voice selection
        while True:
            try:
                choice = int(input("Select a voice by number: ")) - 1
                if 0 <= choice < len(filtered_voices):
                    selected_voice = filtered_voices[choice]
                    # Again extract only the name and locale for the selected voice
                    voice_name = f"{selected_voice.locale}-{selected_voice.name.split(' ')[-1].replace('Neural)', 'Neural')}"  # Adjust for Neural
                    print(f"You selected: {voice_name} ({selected_voice.locale})")
                    return voice_name  # Return in the format 'locale-name'
                else:
                    print("Invalid choice. Please select a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    else:
        print("Error retrieving voices:", voice_list.reason)
        return None  # Return None if there was an error


def text_synthesis(speech_config, filename, voiceName, text):

    # Specify the file path to save the audio as an MP3 file
    file_path = filename
    audio_config = speechsdk.audio.AudioOutputConfig(filename=file_path)

    # The neural multilingual voice can speak different languages based on the input text.
    print('så här ser röst namnet ut:', voiceName)
    speech_config.speech_synthesis_voice_name = voiceName #'sv-SE-MattiasNeural'

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    text = text

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    # Check if the synthesis is successful
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized and saved to [{file_path}]")
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print(f"Error details: {cancellation_details.error_details}")
                print("Did you set the speech resource key and region values?")

if __name__ == "__main__":
    main()
