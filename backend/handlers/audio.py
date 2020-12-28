import datetime
import logging
import os

from pydub import AudioSegment

PYDUB_LOG = logging.getLogger("pydub.converter")
PYDUB_LOG.setLevel(logging.INFO)
PYDUB_LOG.addHandler(logging.StreamHandler())
LOG = logging.getLogger(__name__)


def echo_audio(update, context):
    message = update.effective_message
    audio = message.audio
    file_name = f"audio-{audio.file_unique_id}.ogg"
    file_path = f"files/{file_name}"
    improved_file_path = f"files/improved-{file_name}"
    LOG.info(f"{update.update_id=}; AUDIO: {file_path=}")

    if not os.path.exists(improved_file_path):
        improve_audio_or_voice(
            audio, file_path=file_path, improved_file_path=improved_file_path, update=update, context=context
        )

    LOG.info(f"Sending file...; {improved_file_path=}")
    with open(improved_file_path, "rb") as f:
        context.bot.send_audio(
            chat_id=update.effective_chat.id,
            audio=f,
            reply_to_message_id=message.message_id,
        )


def echo_voice(update, context):
    message = update.effective_message
    voice = update.message.voice
    file_name = f"voice-{voice.file_unique_id}.oga"
    file_path = f"files/{file_name}"
    improved_file_path = f"files/improved-{file_name}"
    LOG.info(f"{update.update_id=}; VOICE: {file_path=}")

    if not os.path.exists(improved_file_path):
        improve_audio_or_voice(
            voice, file_path=file_path, improved_file_path=improved_file_path, update=update, context=context
        )

    LOG.info(f"Sending file...; {improved_file_path=}")
    with open(improved_file_path, "rb") as f:
        context.bot.send_voice(
            chat_id=update.effective_chat.id,
            voice=f,
            reply_to_message_id=message.message_id,
        )


def improve_audio_or_voice(audio_or_voice, *, file_path, improved_file_path, update, context):
    file_info = audio_or_voice.get_file()
    LOG.info(f"Downloading...; {file_info=}")
    assert file_path == file_info.download(custom_path=file_path)
    LOG.info(f"Opening...; {file_path=}")
    segment = AudioSegment.from_file(file_path)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            f"I'm improving {audio_or_voice.file_unique_id}. Please wait...\n"
            f"ETA: {datetime.timedelta(seconds=segment.duration_seconds // 3)}"
        ),
    )
    LOG.info(f"Removing silence...; {segment.duration_seconds=}; {segment.dBFS=}; {segment.max_dBFS=};")
    segment = segment.strip_silence(silence_len=100, silence_thresh=segment.dBFS * 1.5, padding=100)
    LOG.info(f"Saving...; {improved_file_path=}")
    segment.export(improved_file_path)
