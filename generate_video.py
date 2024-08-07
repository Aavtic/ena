from gemini import Gemini
from fetch_gif import GenerateGifs
from process_video import VideoProcessor
import time
import os

gemini = Gemini()
generator = GenerateGifs()
video_processor = VideoProcessor()

transcript =  "Iron Man and the Missing CoffeeIt was a typical Tuesday morning at Stark Tower. Tony Stark, aka Iron Man, was in his lab, tinkering with his latest invention—a coffee machine that would brew the perfect cup every time. He called it the “Espresso Mark 1.” After a long night of debugging and fine-tuning, Tony was excited to try it out.“JARVIS, initiate the Espresso Mark 1,” Tony commanded.“As you wish, sir,” JARVIS responded in his smooth British accent.The machine whirred to life, lights blinking, gears turning. A few moments later, it produced a cup of coffee that smelled divine. Tony took a sip, and his eyes widened with pleasure. “Perfect,” he murmured.Just as he was about to take another sip, an alarm blared. “Sir, there's an urgent situation downtown,” JARVIS announced.Tony groaned. “It's always something. Alright, suit up.”As the Iron Man suit assembled around him, Tony reluctantly put down his coffee and flew out of the lab. The situation downtown turned out to be a minor skirmish between two rival gangs. It didn't take long for Iron Man to subdue them and hand them over to the police. He was back at Stark Tower in less than an hour.“Okay, where was I?” Tony said to himself as he walked back into the lab. He reached for his coffee cup, but it was gone. “JARVIS, where's my coffee?”“I'm afraid I don't know, sir,” JARVIS replied. “Perhaps it's been misplaced?”Tony frowned. He searched the lab but found no trace of his coffee. “Who would take my coffee?”At that moment, Pepper Potts walked in. “Hey, Tony, have you seen—”“Pepper! Did you take my coffee?” Tony interrupted.Pepper raised an eyebrow. “Your coffee? No, I haven't seen it. Why would I take your coffee?”“Because it's the best coffee ever made, that's why,” Tony replied, slightly annoyed.Pepper sighed. “Tony, it's just a cup of coffee. You can make another one.”“It's not just any coffee, it's the first cup from the Espresso Mark 1. It's irreplaceable,” Tony insisted.Pepper rolled her eyes. “Fine, I'll help you find it. Let's split up.”As they searched the tower, Tony couldn't help but feel a bit paranoid. Who could have taken it? He checked with Happy Hogan, who was busy monitoring security. “Happy, have you seen my coffee?”“Your coffee? No, I haven't seen it. Are you sure you didn't just misplace it?” Happy asked.Tony scowled. “I didn't misplace it. Someone took it.”Their search led them to Bruce Banner, who was deep in thought, scribbling equations on a whiteboard. “Bruce, did you take my coffee?” Tony asked.Bruce looked up, confused. “Your coffee? No, I've been here all morning. Why would I take your coffee?”Tony sighed. “Never mind.”Feeling frustrated, Tony decided to check the security footage. He and Pepper watched the recordings intently. Suddenly, they saw a blur of motion. “Pause it there,” Tony said.They zoomed in and enhanced the image. It was Rocket Raccoon, sneaking into the lab and grabbing the coffee cup. “Rocket!” Tony exclaimed. “That little thief!”Tony quickly donned his suit and flew to the Guardians of the Galaxy's temporary quarters in New York. He found Rocket lounging on a couch, sipping the coffee.“Hey, Stark! Great coffee!” Rocket said, grinning.“Rocket, that's my coffee!” Tony said, exasperated.“Finders keepers,” Rocket replied, taking another sip.Tony groaned. “Rocket, that was the first cup from my new machine. It's special.”Rocket shrugged. “Well, it's really good. You should be proud.”Tony sighed. “Alright, alright. Enjoy it. But next time, ask.”Rocket chuckled. “Sure thing, Stark. No hard feelings?”Tony couldn't help but laugh. “No hard feelings, Rocket. Just don't make a habit of it.”As Tony flew back to Stark Tower, he couldn't help but smile. Sure, he lost his perfect cup of coffee, but he gained a funny story to tell. And besides, he could always make another cup with the Espresso Mark 1.Back at the tower, Pepper greeted him. “Did you find it?”“Yeah, Rocket took it,” Tony replied, shaking his head. “That raccoon has good taste.”Pepper laughed. “Only you, Tony. Only you.”And with that, Tony set about brewing another perfect cup of coffee, knowing that in the world of superheroes, even the smallest things could lead to the most unexpected adventures."


queries_suggestion = gemini.generate_gif_queries(transcript=transcript)
print('suggestions: ', queries_suggestion)

query_list =  gemini.parse_gemini(queries_suggestion)
print(query_list)

files = []
for query in query_list:
    time.sleep(5)
    filename=f"gifs\\{query}{int(time.time())}.mp4"
    files.append(filename)
    generator.generate_gif(query=query, filename=filename, debug=True)


arg_files = ['"' + os.path.join('gifs\\', i) + '"' for i in os.listdir('./gifs')]

video_processor.merge(input_files=arg_files, output_file="output\\merged.mp4")

# ffmpeg  -i "gifs\brainwashing gif1719661268.mp4" -i "gifs\Dr. Maiken Nedergaard funny gif1719661282.mp4" -i "gifs\glymphatic system  funny gif1719661288.mp4" -i "gifs\ILiff funny gif1719661274.mp4" -i "gifs\Jonathan Kipnis gif1719661306.mp4" -i "gifs\lymphatic system gif1719661299.mp4" -i "gifs/plumbing in a house gif1719661314.mp4" -filter_complex "[0:v]scale='if(gt(a,3/4),480,-1)':'if(gt(a,3/4),-1,640)',pad=480:640:(ow-iw)/2:(oh-ih)/2[v0];[1:v]scale='if(gt(a,3/4),480,-1)':'if(gt(a,3/4),-1,640)',pad=480:640:(ow-iw)/2:(oh-ih)/2[v1];[2:v]scale='if(gt(a,3/4),480,-1)':'if(gt(a,3/4),-1,640)',pad=480:640:(ow-iw)/2:(oh-ih)/2[v2];[3:v]scale='if(gt(a,3/4),480,-1)':'if(gt(a,3/4),-1,640)',pad=480:640:(ow-iw)/2:(oh-ih)/2[v3];[4:v]scale='if(gt(a,3/4),480,-1)':'if(gt(a,3/4),-1,640)',pad=480:640:(ow-iw)/2:(oh-ih)/2[v4];[5:v]scale='if(gt(a,3/4),480,-1)':'if(gt(a,3/4),-1,640)',pad=480:640:(ow-iw)/2:(oh-ih)/2[v5];[6:v]scale='if(gt(a,3/4),480,-1)':'if(gt(a,3/4),-1,640)',pad=480:640:(ow-iw)/2:(oh-ih)/2[v6];[7:v]scale='if(gt(a,3/4),480,-1)':'if(gt(a,3/4),-1,640)',pad=480:640:(ow-iw)/2:(oh-ih)/2[v7]; [v0][v1][v2][v3][v4][v5][v6][v7] concat=n=8:v=1:a=0[out]" -map "[out]" merged.mp4 -y'