import os
import logging
import uuid
from pathlib import Path

from azure.storage.blob import BlobServiceClient


class AzureBlobHandler():
    """A class to handle dir-of-audio-files - - - > Azure storage blob."""

    def __init__(self,
                 audio_dir: str,
                 blob_key: str,
                 blob_container_link: str,
                 request_id: str
                ):

        self.audio_dir = Path(audio_dir)
        self.blob_service_client = BlobServiceClient(blob_container_link, blob_key)
        self.request_id = request_id

        self.logger = logging.getLogger('apt')

    def upload_to_blob(self):

        # first check for audio files + get filepaths
        input_audio_paths = self._get_audio_paths()

        # create a container to store the individual audio files in
        container_client = self.blob_service_client.create_container(self.request_id)
        self.logger.info(f'Created container in blob environment: name {self.request_id}')

        # upload files to that container
        for audio_path in input_audio_paths:
            self.logger.info(f'Uploading file {audio_path.name}...')
            blob_client = self.blob_service_client.get_blob_client(container=self.request_id, blob=audio_path.name)

            with open(file=str(audio_path), mode='rb') as audio_data:
                blob_client.upload_blob(audio_data)

        self.logger.info(f'All files uploaded successfully!')

        return container_client

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


# class AzureTranscriptionHandler():
#     """A class to handle Azure storage blob -> dir-of-azure-speech-outputs."""
