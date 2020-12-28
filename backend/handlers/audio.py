import datetime
import logging
import os

from pydub import AudioSegment

CHUNK_LENGTH = 10_000

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
    segment = AudioSegment.from_file(file_path)[:3_600_000]
    original_segment_delta = datetime.timedelta(seconds=int(segment.duration_seconds))
    temporary_message = context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            f"Improving {audio_or_voice.file_unique_id}. Please wait...\n"
            f"Original duration: {original_segment_delta}"
        ),
    )
    segment = chunked_improve(full_segment=segment)
    LOG.info(f"Saving...; {improved_file_path=}")
    segment.export(improved_file_path)

    final_segment_delta = datetime.timedelta(seconds=int(segment.duration_seconds))
    context.bot.edit_message_text(
        chat_id=temporary_message.chat_id,
        message_id=temporary_message.message_id,
        text=(
            f"Improved {audio_or_voice.file_unique_id}.\n"
            f"Original duration: {original_segment_delta}\n"
            f"Final duration: {final_segment_delta}\n"
            f"You saved: {original_segment_delta - final_segment_delta}"
        ),
    )


def chunked_improve(*, full_segment):
    updated_segment = full_segment[:0]
    duration = int(full_segment.duration_seconds * 1000)
    for i in range(0, duration, CHUNK_LENGTH):
        segment = full_segment[i : i + CHUNK_LENGTH]
        LOG.info(f"Normalizing...; {segment.duration_seconds=}; {segment.dBFS=}; {segment.max_dBFS=};")
        segment = segment.normalize(headroom=0.1)
        LOG.info(f"Removing silence...; {segment.duration_seconds=}; {segment.dBFS=}; {segment.max_dBFS=};")
        segment = segment.strip_silence(silence_len=100, silence_thresh=segment.dBFS * 1.5, padding=100)
        updated_segment += segment
    return updated_segment
