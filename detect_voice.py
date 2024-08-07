from voices import GenerateVoices
from scipy.io import wavfile
from scipy.signal import find_peaks
from pydub.audio_segment import AudioSegment
from pydub.utils import make_chunks
from time import sleep, time
import speech_recognition as sr
import matplotlib.pyplot as plt
import numpy as np
import os 
import math



class Detection:
    def __init__(self):
        self.clean_dirs = ['words']
        self.clean_cwd()
        pass
    def clean_cwd(self):
        for direct in self.clean_dirs:
            files = os.listdir(direct)
            files = [os.path.join(direct, i) for i in files]
            for file in files:
                    if os.path.isfile(file):
                        os.remove(file)

    def plot(self,data):
        plt.figure(figsize=(15, 5))
        plt.plot(data)
        plt.title('Waveform of the Audio File')
        plt.xlabel('Sample Index')
        plt.ylabel('Amplitude')
        plt.show()

    def recognize_words(self, file_name):
        print(file_name)
        r = sr.Recognizer()
        text = ''
        with sr.AudioFile(file_name) as source:
            audio = r.record(source)
        try: 
            text = r.recognize_google(audio)
            print("what you said: ", text)
        except Exception as e:
            print('Error: ', e, file_name)
            return None
        
        return text
    def save_captions(self, data):

                with open('text.srt', 'wb') as f:
                    srt_data = b""
                    starter = ""
                    for i, stamps in enumerate(data):
                        start, end = stamps 
                        text = data[stamps]
                        srt_data += f"{starter}{i+1}\n{start} --> {end}\n{text}".encode('utf-8')
                        starter = "\n\n"
                    f.write(srt_data)
                    print(srt_data)


    def to_timestamps(self, sample_index, sample_rate):
        time_in_seconds = sample_index / sample_rate
        hours = int(time_in_seconds // 3600)
        minutes = int((time_in_seconds % 3600) // 60)
        seconds = math.ceil(time_in_seconds % 60)
        milliseconds = int(round((time_in_seconds - int(time_in_seconds)) * 1000))
        timestamp = f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"
        return timestamp
    def detect(self,data: np.ndarray, sample_rate, text):
        def save_json(data:dict):    
            with open('temp/json_data.json', 'w') as f:
                f.write(str(data))

        def save_audio_segment(data, sample_rate, start_sample, end_sample, filename):
            # Determine the sample width based on the dtype of the data
            if data.dtype == np.int16:
                sample_width = 2  # 16-bit audio
            elif data.dtype == np.int32:
                sample_width = 4  # 32-bit audio
            elif data.dtype == np.uint8:
                sample_width = 1  # 8-bit audio
            else:
                raise ValueError("Unsupported sample width")

            # Convert data to bytes and create an AudioSegment
            audio_segment = AudioSegment(
                data[start_sample:end_sample].tobytes(),
                frame_rate=sample_rate,
                sample_width=sample_width,
                channels=1
            )
            audio_segment.export(filename, format="wav")

        
        # AAHA ARMADAM!
        text = text.split()
        peaks, _ = find_peaks(data, height=0, prominence=len(text))
        threshold_distance = 0.020 * sample_rate
        groups = np.split(peaks, np.where(np.diff(peaks) > threshold_distance)[0] + 1)
        # segments = [(group[0] / sample_rate, group[-1] / sample_rate) for group in groups if len(group) > 1]    
        # print("Groups of peaks: ", groups)

        segments = []
        for group in groups:
            if len(groups) > 1:
                start_time = group[0] / sample_rate
                end_time = group[-1] / sample_rate
                segments.append((start_time, end_time))

        extracted_data = {}
        for i, (start, end) in enumerate(segments):
            start_sample = int(start * sample_rate)
            end_sample = int(end * sample_rate)
            print("start: ", start_sample, "end : ", end_sample)
            start_timestamp = self.to_timestamps(start_sample, sample_rate)
            end_timestamp = self.to_timestamps(end_sample, sample_rate)
            if end_sample - start_sample >= 8_000:
                # word_data = data[start_sample:end_sample]
                filename = f"words/word_{i}.wav"
                save_audio_segment(data, sample_rate, start_sample, end_sample, filename)
                words = self.recognize_words(filename)
                if words:
                    extracted_data[(start_timestamp, end_timestamp)] = words
                    sleep(1)
            else:
                filename = f"words/discarded_word_{i}.wav"
                save_audio_segment(data, sample_rate, start_sample, end_sample, filename)
        print(extracted_data)
        save_json(extracted_data)
        self.save_captions(extracted_data)

    def from_cloudtts(self, text, filename):
        print('dowlnloading to', filename)
        gen_v = GenerateVoices()
        gen_v.generate_cloudtts(text=text, filename=filename)
    

    def split_audio(self, secs: int, text, filename: str, _skip_download=False):
        milli_seconds = secs * 1000
        print(milli_seconds)
        if not _skip_download:
            print('dowlnloading to', filename)
            print(secs)
            gen_v = GenerateVoices()
            gen_v.generate_cloudtts(text=text, filename=filename)

        AudioSegment.from_file(filename, "mp3").export("output.wav", format="wav")
        audio = AudioSegment.from_file("output.wav", "wav")
        sample_rate, _ = wavfile.read("output.wav")
        total = len(audio)
        num_segments = total // milli_seconds


        sample_filename = {}
        extracted_data = {}

        for i in range(num_segments):
            start_ms = i * milli_seconds
            end_ms = start_ms + milli_seconds
            segment = audio[start_ms: end_ms] if i != num_segments else audio[start_ms:]
            chunk_name = "words/chunk_%d.wav"%i
            segment.export(chunk_name, format="wav")
            start_sample = int(start_ms * audio.frame_rate / 1000)
            end_sample = int(end_ms * audio.frame_rate / 1000)
            sample_filename[chunk_name] = (start_sample, end_sample)
        print(sample_filename)
        words_chunks = []
        for file in sample_filename:
            words = self.recognize_words(file)
            if words:
                words_chunks.append(words)
                start_sample, end_sample = sample_filename[file]
                start_timestamp = self.to_timestamps(start_sample, sample_rate)
                end_timestamp = self.to_timestamps(end_sample, sample_rate)
                extracted_data[(start_timestamp, end_timestamp)] = words

        print("extracted_data = ", extracted_data)
        self.save_captions(extracted_data)



    def start_process(self, text, filename):
        print('dowlnloading to', filename)
        gen_v = GenerateVoices()
        gen_v.generate_voice(text=text, filename=filename, voice="en_us_007")
        audio = AudioSegment.from_mp3(filename)
        audio.export("output.wav", format="wav")

        sample_rate, data = wavfile.read('output.wav')

        if len(data.shape) > 1:
            data = data[:,0]

        return self.detect(data, sample_rate, text)

if __name__ == '__main__':
    text = "Iron Man and the Missing CoffeeIt was a typical Tuesday morning at Stark Tower. Tony Stark, aka Iron Man, was in his lab, tinkering with his latest invention—a coffee machine that would brew the perfect cup every time. He called it the “Espresso Mark 1.” After a long night of debugging and fine-tuning, Tony was excited to try it out.“JARVIS, initiate the Espresso Mark 1,” Tony commanded.“As you wish, sir,” JARVIS responded in his smooth British accent.The machine whirred to life, lights blinking, gears turning. A few moments later, it produced a cup of coffee that smelled divine. Tony took a sip, and his eyes widened with pleasure. “Perfect,” he murmured.Just as he was about to take another sip, an alarm blared. “Sir, there's an urgent situation downtown,” JARVIS announced.Tony groaned. “It's always something. Alright, suit up.”As the Iron Man suit assembled around him, Tony reluctantly put down his coffee and flew out of the lab. The situation downtown turned out to be a minor skirmish between two rival gangs. It didn't take long for Iron Man to subdue them and hand them over to the police. He was back at Stark Tower in less than an hour.“Okay, where was I?” Tony said to himself as he walked back into the lab. He reached for his coffee cup, but it was gone. “JARVIS, where's my coffee?”“I'm afraid I don't know, sir,” JARVIS replied. “Perhaps it's been misplaced?”Tony frowned. He searched the lab but found no trace of his coffee. “Who would take my coffee?”At that moment, Pepper Potts walked in. “Hey, Tony, have you seen—”“Pepper! Did you take my coffee?” Tony interrupted.Pepper raised an eyebrow. “Your coffee? No, I haven't seen it. Why would I take your coffee?”“Because it's the best coffee ever made, that's why,” Tony replied, slightly annoyed.Pepper sighed. “Tony, it's just a cup of coffee. You can make another one.”“It's not just any coffee, it's the first cup from the Espresso Mark 1. It's irreplaceable,” Tony insisted.Pepper rolled her eyes. “Fine, I'll help you find it. Let's split up.”As they searched the tower, Tony couldn't help but feel a bit paranoid. Who could have taken it? He checked with Happy Hogan, who was busy monitoring security. “Happy, have you seen my coffee?”“Your coffee? No, I haven't seen it. Are you sure you didn't just misplace it?” Happy asked.Tony scowled. “I didn't misplace it. Someone took it.”Their search led them to Bruce Banner, who was deep in thought, scribbling equations on a whiteboard. “Bruce, did you take my coffee?” Tony asked.Bruce looked up, confused. “Your coffee? No, I've been here all morning. Why would I take your coffee?”Tony sighed. “Never mind.”Feeling frustrated, Tony decided to check the security footage. He and Pepper watched the recordings intently. Suddenly, they saw a blur of motion. “Pause it there,” Tony said.They zoomed in and enhanced the image. It was Rocket Raccoon, sneaking into the lab and grabbing the coffee cup. “Rocket!” Tony exclaimed. “That little thief!”Tony quickly donned his suit and flew to the Guardians of the Galaxy's temporary quarters in New York. He found Rocket lounging on a couch, sipping the coffee.“Hey, Stark! Great coffee!” Rocket said, grinning.“Rocket, that's my coffee!” Tony said, exasperated.“Finders keepers,” Rocket replied, taking another sip.Tony groaned. “Rocket, that was the first cup from my new machine. It's special.”Rocket shrugged. “Well, it's really good. You should be proud.”Tony sighed. “Alright, alright. Enjoy it. But next time, ask.”Rocket chuckled. “Sure thing, Stark. No hard feelings?”Tony couldn't help but laugh. “No hard feelings, Rocket. Just don't make a habit of it.”As Tony flew back to Stark Tower, he couldn't help but smile. Sure, he lost his perfect cup of coffee, but he gained a funny story to tell. And besides, he could always make another cup with the Espresso Mark 1.Back at the tower, Pepper greeted him. “Did you find it?”“Yeah, Rocket took it,” Tony replied, shaking his head. “That raccoon has good taste.”Pepper laughed. “Only you, Tony. Only you.”And with that, Tony set about brewing another perfect cup of coffee, knowing that in the world of superheroes, even the smallest things could lead to the most unexpected adventures."
    d = Detection()
    d.start_process(text, f"voices\\voice_{int(time())}.mp3")
