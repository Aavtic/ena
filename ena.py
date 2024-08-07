from detect_voice import Detection
from time import time, sleep
from slugify import slugify
from fetch_gif import GenerateGifs
from process_video import VideoProcessor
from utils import Utils
import os
import math
import argparse
import sys

generator = GenerateGifs()
video_processor = VideoProcessor()
detection = Detection()
utils = Utils()

parser = argparse.ArgumentParser(description="Video generation program")
parser.add_argument('--transcript', nargs='+', help='The transcript for the video')

args = parser.parse_args()

if args.transcript:
    text = ' '.join(args.transcript)
else:
    print('No transcript provided.')
    sys.exit()

print(text)
ctime = str(int(time()))
audio_filename = f"voices\\voice_%s.mp3"%ctime
detection.from_cloudtts(text, audio_filename)

files = []
iterator = utils.Iterator(text)
no_query = math.ceil(len(text)/5)
for i in range(no_query):
    query = iterator.take(5)
    if query:
        query_filename = '_'.join(query)
        query_filename = slugify(query_filename)
        query = ' '.join(query)
        print(query)
        filename=f"gifs\\{query_filename}{int(time())}.mp4"
        files.append(filename)
        generator.generate_gif(query=query, filename=filename, debug=True)
        sleep(5)


arg_files = ['"' + os.path.join('gifs\\', i) + '"' for i in os.listdir('./gifs')]
ctime = str(int(time()))
output_file = "output\\merged%s.mp4"%(ctime)

video_processor.merge(input_files=arg_files, output_file=output_file)

v_len = utils.get_video_len(output_file)
a_len = utils.get_audio_len(audio_filename)

utils.reduce_video_length(output_file, v_len, a_len, "output\\reduced.mp4")
utils.merge_video_audio("output\\reduced.mp4", audio_filename, "output\\final%s.mp4"%ctime)



