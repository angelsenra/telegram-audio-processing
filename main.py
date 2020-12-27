from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import strip_silence
import logging

LOG = logging.getLogger("pydub.converter")
LOG.setLevel(logging.DEBUG)
LOG.addHandler(logging.StreamHandler())

audio = AudioSegment.from_mp3("testAudios/audio_001.mp3")
segment = audio[:30000]
print(segment, segment.duration_seconds)
# faster =  segment.speedup(playback_speed=1.5, chunk_size=150, crossfade=25)
# print(faster, faster.duration_seconds)
better = segment.strip_silence(silence_len=100, silence_thresh=segment.dBFS * 1.5, padding=100)
print(better, better.duration_seconds)
