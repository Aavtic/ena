import requests
from time import time
from datetime import timedelta
import base64
import json
import os


class GenerateVoices:
    def __init__(self):
        self.voices = {
        "en_uk_001": 	"Narrator (Chris)",
        "en_uk_003": 	"UK Male 2",
        "en_female_emotional": 	"Peaceful",
        "en_au_001": 	"Metro (Eddie)",
        "en_au_002": 	"Smooth (Alex)",
        "en_us_002": 	"Jessie",
        "en_us_006": 	"Joey",
        "en_us_007": 	"Professor",
        "en_us_009": 	"Scientist",
        "en_us_010": 	"Confidence",
        "en_female_samc": 	"Empathetic",
        "en_male_cody": 	"Serious",
        "en_male_narration": 	"Story Teller",
        "en_male_funny": 	"Wacky",
        "en_male_jarvis": 	"Alfred",
        "en_male_santa_narration": 	"Author",
        "en_female_betty": 	"Bae",
        "en_female_makeup": 	"Beauty Guru",
        "en_female_richgirl": 	"Bestie",
        "en_male_cupid": 	"Cupid",
        "en_female_shenna": 	"Debutante",
        "en_male_ghosthost": 	"Ghost Host",
        "en_female_grandma": 	"Grandma",
        "en_male_ukneighbor": 	"Lord Cringe",
        "en_male_wizard": 	"Magician",
        "en_male_trevor": 	"Marty",
        "en_male_deadpool": 	"Mr. GoodGuy (Deadpool)",
        "en_male_ukbutler": 	"Mr. Meticulous",
        "en_male_petercullen": 	"Optimus Prime",
        "en_male_pirate": 	"Pirate",
        "en_male_santa": 	"Santa",
        "en_male_santa_effect": 	"Santa (w/ effect)",
        "en_female_pansino": 	"Varsity",
        "en_male_grinch": 	"Trickster (Grinch)",
        "en_us_ghostface": 	"Ghostface (Scream)",
        "en_us_chewbacca": 	"Chewbacca (Star Wars)",
        "en_us_c3po": 	"C-3PO (Star Wars)",
        "en_us_stormtrooper": 	"Stormtrooper (Star Wars)",
        "en_us_stitch": 	"Stitch (Lilo & Stitch)",
        "en_us_rocket": 	"Rocket (Guardians of the Galaxy)",
        "en_female_madam_leota": 	"Madame Leota (Haunted Mansion)",
        "en_male_sing_deep_jingle": 	"Song: Caroler",
        "en_male_m03_classical": 	"Song: Classic Electric",
        "en_female_f08_salut_damour": 	"Song: Cottagecore (Salut d'Amour)",
        "en_male_m2_xhxs_m03_christmas": 	"Song: Cozy",
        "en_female_f08_warmy_breeze": 	"Song: Open Mic (Warmy Breeze)",
        "en_female_ht_f08_halloween": 	"Song: Opera (Halloween)",
        "en_female_ht_f08_glorious": 	"Song: Euphoric (Glorious)",
        "en_male_sing_funny_it_goes_up": 	"Song: Hypetrain (It Goes Up)",
        "en_male_m03_lobby": 	"Song: Jingle (Lobby)",
        "en_female_ht_f08_wonderful_world": 	"Song: Melodrama (Wonderful World)",
        "en_female_ht_f08_newyear": 	"Song: NYE 2023",
        "en_male_sing_funny_thanksgiving": 	"Song: Thanksgiving",
        "en_male_m03_sunshine_soon": 	"Song: Toon Beat (Sunshine Soon)",
        "en_female_f08_twinkle": 	"Song: Pop Lullaby",
        "en_male_m2_xhxs_m03_silly": 	"Song: Quirky Time",

        }
        self.clean_wd()

    def generate_voice_tiktok_tts(self, text, filename, voice = "en_us_010"):
        session = requests.session()

        burp0_url = "https://tiktok-tts.weilbyte.dev:443/api/generate"
        burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/json", "Origin": "https://tiktok-tts.weilbyte.dev", "Referer": "https://tiktok-tts.weilbyte.dev/", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Priority": "u=1", "Te": "trailers"}
        burp0_json={"base64": True, "text": text, "voice":voice}
        print('sending request...')
        s = session.post(burp0_url, headers=burp0_headers, json=burp0_json)
        print('status code:',s.status_code)
        print('text: ',s.text)


        data = s.content
        decoded = base64.b64decode(data)

        with open("response.dat", "wb") as f:
            f.write(s.content)

        with open(filename, 'wb') as f:
            f.write(decoded)

    def clean_wd(self):
        directory = ['./words', './voices']
        for direct in directory:
            files = os.listdir(direct)
            files = [os.path.join(direct, i) for i in files]
            for file in files:
                    if os.path.isfile(file):
                        os.remove(file)

    def generate_cloudtts(self, text, filename):
        def convert_offset_to_timestamp(offset):
            td = timedelta(milliseconds=offset)
            return str(td)[:-3].replace('.', ',')

        def create_srt(filename: str, speechmarks):
            srt_data = []
            for i, mark in enumerate(speechmarks):
                start_timestamp = convert_offset_to_timestamp(mark['offset'])
                if i + 1 < len(speechmarks):
                    end_timestamp = convert_offset_to_timestamp(speechmarks[i+1]['offset'])
                else:
                    end_timestamp = convert_offset_to_timestamp(mark['offset'] + 1000)
                srt_data.append(str(i+1))
                srt_data.append('\n')
                srt_data.append("%s --> %s"%(start_timestamp, end_timestamp))
                srt_data.append('\n')
                srt_data.append(mark["word"])
                if i+1<len(speechmarks):
                    srt_data.append('\n')
                    srt_data.append('\n')
            with open(filename, 'w') as f:
                f.writelines(srt_data)

        session = requests.session()

        burp0_url = "https://cloudtts.com:443/api/get_audio"
        burp0_cookies = {"_ga_E292ZZXMB9": "", "_ga": ""}
        burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Referer": "https://cloudtts.com/u/index.html", "Content-Type": "application/json", "Origin": "https://cloudtts.com", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Priority": "u=1", "Te": "trailers", "Connection": "keep-alive"}
        burp0_json={"rate": 1, "recording": False, "text": text, "voice": "en-US-AriaNeural", "volume": 1, "with_speechmarks": True}
        s = session.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, json=burp0_json)

        print(s.text)
        data = s.content
        json_data = json.loads(data)

        audio_data = (json_data['data']['audio']).encode("utf-8")
        speechmarks = json_data['data']['speechmarks']
        decoded = base64.b64decode(audio_data)
        with open(filename, "wb") as f:
            f.write(decoded)
        create_srt("subtitle.srt", speechmarks)
