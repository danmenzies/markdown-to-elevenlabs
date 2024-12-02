import os
from pathlib import Path
from elevenlabs import ElevenLabs
from pydub import AudioSegment


class build_output:
    """
    This class is used to build the output of the program
    """

    def __init__(self, PROJECT_ROOT, voice_id, api_key):
        """
        Constructor for build_output class
        :param PROJECT_ROOT: Project root
        :param voice_id: ElevenLabs Voice ID
        :param api_key: ElevenLabs API Key
        """
        self.PROJECT_ROOT = PROJECT_ROOT
        self.voice_id = voice_id
        self.api_key = api_key
        self.input_dir = os.path.join(PROJECT_ROOT, "output", "markdown")
        self.output_dir = os.path.join(PROJECT_ROOT, "output", "audio")
        self.client = ElevenLabs(api_key=api_key)
        self.audio_files = []

    def components(self):
        """
        Main function to build the audio output
        """
        for markdown_folder in os.listdir(self.input_dir):
            folder_path = os.path.join(self.input_dir, markdown_folder)
            if os.path.isdir(folder_path):
                self.process_folder(markdown_folder)

    def process_folder(self, folder_name):
        """
        Process a single folder of split Markdown files
        :param folder_name: Name of the folder
        """
        folder_path = os.path.join(self.input_dir, folder_name)
        audio_output_folder = os.path.join(self.output_dir, folder_name)

        # Create audio output folder if it doesn't exist
        os.makedirs(audio_output_folder, exist_ok=True)

        for file_name in sorted(os.listdir(folder_path)):
            if file_name.endswith(".md"):
                section_path = os.path.join(folder_path, file_name)
                output_audio_path = os.path.join(audio_output_folder, file_name.replace(".md", ".mp3"))
                self.generate_audio(section_path, output_audio_path)

    def combine_final_audio(self):
        """
        Combine all the audio files into one
        :return:
        """

        # Combine all audio files into one
        for folder_name in sorted(os.listdir(self.output_dir)):
            combined_audio_path = os.path.join(self.output_dir, f"{folder_name}.mp3")
            print(f"Combining audio for: {folder_name}")

            # Get all audio files in the folder
            audio_files = []
            folder_path = os.path.join(self.output_dir, folder_name)
            for file_name in sorted(os.listdir(folder_path)):
                if file_name.endswith(".mp3"):
                    audio_files.append(os.path.join(folder_path, file_name))
            # Combine audio files for each folder
            self.combine_audio(audio_files, combined_audio_path)

    def generate_audio(self, input_file, output_audio_path):
        """
        Generate audio for a single section using ElevenLabs API
        :param input_file: Path to the Markdown file section
        :param output_audio_path: Path to save the generated audio
        """
        with open(input_file, "r") as file:
            text = file.read().strip()

        if not text:
            print(f"Skipping empty file: {input_file}")
            return None

        # Generate audio using ElevenLabs API
        print(f"Generating audio for: {input_file}")
        response = self.client.text_to_speech.convert(
            voice_id=self.voice_id,
            model_id="eleven_multilingual_v2",  # Use the updated multilingual model
            text=text,
        )

        # Collect the full audio content from the generator
        audio_content = b"".join(response)

        # Save the response audio to file
        with open(output_audio_path, "wb") as audio_file:
            audio_file.write(audio_content)

        return output_audio_path

    def combine_audio(self, audio_files, combined_audio_path):
        """
        Combine multiple audio files into one with natural gaps
        :param audio_files: List of audio file paths
        :param combined_audio_path: Path to save the combined audio file
        """
        combined_audio = None
        gap = AudioSegment.silent(duration=1000)  # 1-second pause

        for audio_file in audio_files:

            try:
                audio_segment = AudioSegment.from_file(audio_file)
            except Exception as e:
                print(f"Error processing file {audio_file}: {e}")
                continue

            if combined_audio is None:
                combined_audio = audio_segment
            else:
                combined_audio += gap + audio_segment

        if combined_audio:
            print(f"Saving combined audio to: {combined_audio_path}")
            combined_audio.export(combined_audio_path, format="mp3")
