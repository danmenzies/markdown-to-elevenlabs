import os
from dotenv import load_dotenv, find_dotenv
import argparse
from pathlib import Path
from src.split_markdown import split_markdown
from src.build_output import build_output

def main(voice_id, api_key, reset, audio_only, markdown_only, combine_only):
    """
    Main function to run the program
    :param voice_id: ElevenLabs Voice ID
    :param api_key: ElevenLabs API Key
    :param reset: Reset the program
    :param audio_only: Only build the audio components
    :param markdown_only: Only build the markdown components
    :param combine_only: Only build the final, combined audio files
    :return: None
    """

    if sum([markdown_only, audio_only, combine_only]) > 1:
        print("Error: Only one of --markdown-only, --audio-only, or --combine-only can be enabled at a time.")
        exit(1)

    # Load environment variables
    env_path = find_dotenv()
    if not env_path:
        print("Error: .env file not found. Please create one in the project root.")
        exit(1)
    load_dotenv(env_path)

    # Set the voice_id and api_key if not provided
    if voice_id is None:
        voice_id = os.getenv("ELEVENLABS_VOICE_ID")

    if api_key is None:
        api_key = os.getenv("ELEVENLABS_API_KEY")

    # Set the project root
    PROJECT_ROOT = Path(env_path).parent

    if reset:
        os.system(f"rm -rf {os.path.join(PROJECT_ROOT, 'output')}")

    # Initialize the split_markdown class
    if not audio_only and not combine_only:
        split_md = split_markdown(PROJECT_ROOT)
        files_to_process = split_md.main(reset)

    # Initialize the build_output class
    audio = build_output(PROJECT_ROOT, voice_id, api_key)

    # Build the audio components
    if not markdown_only and not combine_only:
        audio.components()

    # Combine the audio files
    if not markdown_only and not audio_only:
        audio.combine_final_audio()


if __name__ == "__main__":

    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Convert Markdown files to audio using the Elevenlabs API."
    )
    parser.add_argument(
        "--voice-id",
        type=str,
        default=os.getenv("ELEVENLABS_VOICE_ID"),
        help="Voice ID to use for Elevenlabs. Defaults to the ID in the .env file.",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=os.getenv("ELEVENLABS_API_KEY"),
        help="API Key for Elevenlabs. Defaults to the key in the .env file.",
    )
    parser.add_argument(
        "--reset",
        action='store_true',
        default=False,
        help="Delete previous iterations, and start again (warning, can incur unexpected API expenses).",
    )
    parser.add_argument(
        "--audio-only",
        action='store_true',
        default=False,
        help="Only build the audio components.",
    )
    parser.add_argument(
        "--markdown-only",
        action='store_true',
        default=False,
        help="Only build the markdown components.",
    )
    parser.add_argument(
        "--combine-only",
        action='store_true',
        default=False,
        help="Only build the final, combined audio files.",
    )

    args = parser.parse_args()
    main(
        voice_id=args.voice_id,
        api_key=args.api_key,
        reset=args.reset,
        audio_only=args.audio_only,
        markdown_only=args.markdown_only,
        combine_only=args.combine_only
    )
