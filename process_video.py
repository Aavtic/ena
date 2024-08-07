import subprocess

class VideoProcessor:
    def __init__(self):
        self.set_aspet_ratio_merge_cmd = """ffmpeg %s -filter_complex "%s %s concat=n=%d:v=1:a=0[out]" -map "[out]" %s -y"""
        self.set_aspet_ratio_cmd1 = "[%d:v]scale='if(gt(a,3/4),480,-1)':'if(gt(a,3/4),-1,640)',pad=480:640:(ow-iw)/2:(oh-ih)/2, setsar=1[v%d];"
        self.set_aspet_ratio_cmd2 = "[v%d]"
        self.merge_aud_vid =  "ffmpeg -i %s -i %s -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest %s"

    def merge(self, input_files, output_file):
        input_command = " -i " + " -i ".join(input_files)
        cmd1 = ""
        cmd2 = ""
        for i in range(len(input_files)):
            cmd1 += self.set_aspet_ratio_cmd1%(i, i)
            cmd2 += self.set_aspet_ratio_cmd2%(i)
        print(f"{cmd1=}")
        print(f"{cmd2=}")
        final_cmd = self.set_aspet_ratio_merge_cmd%(input_command, cmd1, cmd2, len(input_files), output_file)
        print(f"final_cmd ", final_cmd)
        
        subprocess.run(final_cmd)
    
    def merge_audio_video(self, video_file, audio_file, output_file):
        cmd = self.merge_aud_vid%(video_file, audio_file, output_file)
        subprocess.Popen(cmd)

# ffmpeg  -i "gifs/brainwashing gif1719661268.mp4" -i "gifs/Dr. Maiken Nedergaard funny gif1719661282.mp4" -i "gifs/glymphatic system  funny gif1719661288.mp4" -i "gifs/ILiff funny gif1719661274.mp4" -i "gifs/Jonathan Kipnis gif1719661306.mp4" -i "gifs/lymphatic system gif1719661299.mp4" -i "gifs/plumbing in a house gif1719661314.mp4" -filter_complex "[0:v]scale=\'if(gt(a,3/4),480,-1)\':\'if(gt(a,3/4),-1,640)\',pad=480:640:(ow-iw)/2:(oh-ih)/2[v0];[1:v]scale=\'if(gt(a,3/4),480,-1)\':\'if(gt(a,3/4),-1,640)\',pad=480:640:(ow-iw)/2:(oh-ih)/2[v1];[2:v]scale=\'if(gt(a,3/4),480,-1)\':\'if(gt(a,3/4),-1,640)\',pad=480:640:(ow-iw)/2:(oh-ih)/2[v2];[3:v]scale=\'if(gt(a,3/4),480,-1)\':\'if(gt(a,3/4),-1,640)\',pad=480:640:(ow-iw)/2:(oh-ih)/2[v3];[4:v]scale=\'if(gt(a,3/4),480,-1)\':\'if(gt(a,3/4),-1,640)\',pad=480:640:(ow-iw)/2:(oh-ih)/2[v4];[5:v]scale=\'if(gt(a,3/4),480,-1)\':\'if(gt(a,3/4),-1,640)\',pad=480:640:(ow-iw)/2:(oh-ih)/2[v5];[6:v]scale=\'if(gt(a,3/4),480,-1)\':\'if(gt(a,3/4),-1,640)\',pad=480:640:(ow-iw)/2:(oh-ih)/2[v6]; [v0][v1][v2][v3][v4][v5][v6] concat=n=7:v=1:a=0[out]" -map "[out]" merged.mp4 -y
