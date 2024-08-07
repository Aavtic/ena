import subprocess
import json

class Utils:
    def __init__(self):
        self.iter = []
        self.video_info_cmd = "ffprobe -v quiet -show_streams -select_streams v:0 -of json %s"
        self.audio_info_cmd = "ffprobe -v quiet -print_format compact=print_section=0:nokey=1:escape=csv -show_entries format=duration %s"
        self.reduce_video_len_cmd = 'ffmpeg -i %s -r 16 -filter:v "setpts=%f*PTS" -y %s'
        self.merge_audio_video_cmd = 'ffmpeg.exe -i "%s" -i "%s" -c:v copy -c:a copy  -y %s'
    def Iterator(self, text: str):
        self.iter = text.split()
        return self
    def take(self, n: int):
        if n < len(self.iter):
            ret = self.iter[:n]
            self.iter = self.iter[n:]
            return ret
        else:
            ret = self.iter
            self.iter = []
            return ret
    def get_video_len(self, filename):
        result = subprocess.check_output(self.video_info_cmd%filename, shell=True).decode()
        print(result)
        video_data_json = json.loads(result)
        return int(float(video_data_json['streams'][0]['duration']))

    def get_audio_len(self, filename):
        result = subprocess.check_output(self.audio_info_cmd%filename, shell=True).decode()
        return int(float(result))

    def reduce_video_length(self,v_file:str, v_len: int, a_len: int, o_file: str):
        print(a_len, v_len)
        ratio = round(a_len / v_len, 2)
        cmd = self.reduce_video_len_cmd%(v_file, ratio, o_file)
        print(cmd)
        subprocess.run(cmd, shell=True)

    def merge_video_audio(self,v_file: str, a_file: str, o_file: str):
        command = self.merge_audio_video_cmd%(v_file, a_file, o_file)
        print(command)
        subprocess.run(self.merge_audio_video_cmd%(v_file, a_file, o_file), shell=True)


if __name__ == "__main__":
    utils = Utils()
    v_len = utils.get_video_len("output\\merged1723008819.mp4")
    a_len = utils.get_audio_len("voices\\voice_1722349689.mp3")
    
    utils.reduce_video_length("output\\merged1723008819.mp4", v_len, a_len, "output\\final1.mp4")
    utils.merge_video_audio("output\\final1.mp4", "voices\\voice_1722349689.mp3", "output\\final2.mp4")




