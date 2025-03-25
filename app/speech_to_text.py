# import wave
# import collections
# import pyaudio
# import webrtcvad
# from faster_whisper import WhisperModel

# class VAD:
#     def __init__(self, mode=3, sample_rate=16000, frame_duration_ms=30):
#         self.vad = webrtcvad.Vad(mode)
#         self.sample_rate = sample_rate
#         self.frame_duration_ms = frame_duration_ms
#         self.frame_size = int(sample_rate * frame_duration_ms / 1000)
#         self.ring_buffer = collections.deque(maxlen=30)
#         self.triggered = False

#         # Load Faster Whisper model
#         model_size = "small"  # Change to "base", "large-v3", etc., as needed
#         self.model = WhisperModel(model_size, device="cpu", compute_type="float32")

#     def frame_generator(self):
#         p = pyaudio.PyAudio()
#         stream = p.open(format=pyaudio.paInt16,
#                         channels=1,
#                         rate=self.sample_rate,
#                         input=True,
#                         frames_per_buffer=self.frame_size)

#         while True:
#             frame = stream.read(self.frame_size)
#             yield frame

#     def process_audio(self):
#         frames = []
#         for frame in self.frame_generator():
#             is_speech = self.vad.is_speech(frame, self.sample_rate)
#             if not self.triggered:
#                 self.ring_buffer.append((frame, is_speech))
#                 num_voiced = len([f for f, speech in self.ring_buffer if speech])
#                 if num_voiced > 0.9 * self.ring_buffer.maxlen:
#                     self.triggered = True
#                     frames.extend([f for f, s in self.ring_buffer])
#                     self.ring_buffer.clear()
#             else:
#                 frames.append(frame)
#                 self.ring_buffer.append((frame, is_speech))
#                 num_unvoiced = len([f for f, speech in self.ring_buffer if not speech])
#                 if num_unvoiced > 0.9 * self.ring_buffer.maxlen:
#                     self.triggered = False
#                     self.ring_buffer.clear()
#                     return self.recognize_speech(frames)
#                     frames = []

#     def recognize_speech(self, frames):
#         # Convert frames to a numpy array and save as a WAV file
#         audio_data = b''.join(frames)
#         temp_file = "temp_audio.wav"
        
#         # Save audio to a WAV file
#         with wave.open(temp_file, 'wb') as wf:
#             wf.setnchannels(1)  # Mono channel
#             wf.setsampwidth(2)  # 16-bit audio
#             wf.setframerate(self.sample_rate)
#             wf.writeframes(audio_data)

#         # Transcribe audio using Faster Whisper
#         segments, info = self.model.transcribe(temp_file, beam_size=5)
        
#         # Collect transcribed text
#         transcription = " ".join([segment.text for segment in segments])
#         return transcription


import wave
import collections
import pyaudio
import webrtcvad
from faster_whisper import WhisperModel

class VAD:
    def __init__(self, mode=3, sample_rate=16000, frame_duration_ms=30):
        self.vad = webrtcvad.Vad(mode)
        self.sample_rate = sample_rate
        self.frame_duration_ms = frame_duration_ms
        self.frame_size = int(sample_rate * frame_duration_ms / 1000)
        self.ring_buffer = collections.deque(maxlen=30)
        self.triggered = False

        # Load Faster Whisper model
        model_size = "small"  # Change to "base", "large-v3", etc., as needed
        self.model = WhisperModel(model_size, device="cpu", compute_type="float32")

    def frame_generator(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=self.sample_rate,
                        input=True,
                        frames_per_buffer=self.frame_size)
        try:
            while True:
                frame = stream.read(self.frame_size, exception_on_overflow=False)
                yield frame
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

    def process_audio(self):
        frames = []
        for frame in self.frame_generator():
            is_speech = self.vad.is_speech(frame, self.sample_rate)
            if not self.triggered:
                self.ring_buffer.append((frame, is_speech))
                num_voiced = len([f for f, speech in self.ring_buffer if speech])
                if num_voiced > 0.9 * self.ring_buffer.maxlen:
                    self.triggered = True
                    frames.extend([f for f, s in self.ring_buffer])
                    self.ring_buffer.clear()
            else:
                frames.append(frame)
                self.ring_buffer.append((frame, is_speech))
                num_unvoiced = len([f for f, speech in self.ring_buffer if not speech])
                if num_unvoiced > 0.9 * self.ring_buffer.maxlen:
                    self.triggered = False
                    self.ring_buffer.clear()
                    return self.recognize_speech(frames)
                    frames = []

    def recognize_speech(self, frames):
        audio_data = b''.join(frames)
        temp_file = "temp_audio.wav"
        
        # Save audio to a WAV file
        with wave.open(temp_file, 'wb') as wf:
            wf.setnchannels(1)  # Mono channel
            wf.setsampwidth(2)  # 16-bit audio
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data)

        # Transcribe audio using Faster Whisper
        segments, info = self.model.transcribe(temp_file, beam_size=5)
        
        # Collect transcribed text
        transcription = " ".join([segment.text for segment in segments])
        return transcription

    def recognize_speech_from_file(self, file_path):
        # Transcribe audio from file
        segments, info = self.model.transcribe(file_path, beam_size=5)
        transcription = " ".join([segment.text for segment in segments])
        return transcription

