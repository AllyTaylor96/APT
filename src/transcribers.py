import os
import logging
import warnings
from pathlib import Path

import whisper

from io_functions import write_json

class WhisperTranscriber():
    """A class to handle dir-of-audio-files - - - > dir-of-transcription-files."""

    def __init__(self,
                 audio_dir: str,
                 output_dir: str,
                 request_id: str,
                 requested_model: str
                ):

        self.audio_dir = Path(audio_dir)
        self.output_dir = Path(output_dir)
        self.request_id = request_id

        # maybe best to move this stuff into separate 'instantiate' function

        # set up output directories
        self.interim_output_dir = self.output_dir / 'interim'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.interim_output_dir.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger('apt')
        self.audio_paths = self._get_audio_paths()

        warnings.filterwarnings('ignore', 'You are using `torch.load` with `weights_only=False`*.')
        self.model = whisper.load_model(requested_model)

    def _get_audio_paths(self) -> list[Path]:
        """Check suitable audio paths are there, and return if so."""

        allowed_audio_encodings = ['*.mp3', '*.wav', '.ogg', '.flac']
        input_audio_paths = []
        for encoding in allowed_audio_encodings:
            input_audio_paths.extend(self.audio_dir.glob(f'**/{encoding}'))

        if input_audio_paths:
            return input_audio_paths
        else:
            self.logger.warning(f'No valid audio files found! Valid types {str(allowed_audio_encodings)}.')
            self.logger.warning('Exiting as unable to continue.')
            exit()

    def run_transcription(self) -> list[dict]:
        """Use model to transcribe the audio files provided."""

        for audio_path in self.audio_paths:
            self.logger.info(f'Transcribing {audio_path.stem}')

            raw_whisper_result = self.model.transcribe(str(audio_path))
            write_json(raw_whisper_result, str(self.interim_output_dir / f'{audio_path.stem}.raw.json'))
