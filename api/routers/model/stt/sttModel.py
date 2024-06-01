
import pandas as pd
import json
import time
import requests
import subprocess

def get_sample_rate(filename):
  command = [
      'ffprobe',
      '-v', 'error',
      '-select_streams', 'a:0',
      '-show_entries', 'stream=sample_rate',
      '-of', 'default=noprint_wrappers=1:nokey=1',
      filename
  ]

  # subprocess를 통해 ffprobe 실행
  result = subprocess.run(command, text=True, capture_output=True)
  if result.returncode != 0:
      raise Exception("ffprobe 실행 실패: ", result.stderr)

  # 샘플링 레이트 반환
  return int(result.stdout.strip())
  
def stt(file):
  client_id = 'Uetw0UUphzGLvbJCpb4H'
  client_secret = 'z7RhSVsBhN0CmZrPZ6STuVb-bOsM27o-6KyqTu_R'
  
  resp = requests.post(
      'https://openapi.vito.ai/v1/authenticate',
      data={'client_id': client_id,
            'client_secret': client_secret}
  )
  resp.raise_for_status()
  data = resp.json()
  access_token = data['access_token']

  config = {
      "use_diarization": True,
      "diarization": {
      "spk_count": 2
      },
      "domain": 'CALL', #전화임을 명시
      "use_multi_channel": False,
      "use_itn": True, #영어/숫자/단위 변환
      "use_disfluency_filter": False,
    "use_profanity_filter": False,
      "use_paragraph_splitter": True,
      "paragraph_splitter": {
      "max": 50
      },
      "us_word_timestamp":True #발화시간 
  }

  resp = requests.post(
  'https://openapi.vito.ai/v1/transcribe',
  headers={'Authorization': 'bearer '+ access_token},
  data={'config': json.dumps(config)},
  files={'file': open(file, 'rb')}
  )

  resp.raise_for_status()
  data = resp.json()
  transcribe_id = data['id']

  time.sleep(8)
  
  resp = requests.get(
  'https://openapi.vito.ai/v1/transcribe/'+transcribe_id,
  headers={'Authorization': 'bearer '+ access_token}
  )
  resp.raise_for_status()
  text = resp.json()
  df = pd.DataFrame({
    'speaker': pd.Series(dtype='str'),
    'text': pd.Series(dtype='str'),
    'start': pd.Series(dtype='int'),
    'duration': pd.Series(dtype='int'),
    'file': pd.Series(dtype='str'),
    'sr': pd.Series(dtype='int')
    })
  
  for utterance in text['results']['utterances']:
      spk = utterance['spk']
      msg = utterance['msg']
      start = utterance['start_at']
      duration = utterance['duration']
      sr = get_sample_rate(file)
      file = file
      df.loc[len(df)] = [spk, msg, start, duration, file, sr]
    
  df['sr'] = df['sr'].astype(int)
  return df
