import subprocess
import numpy as np
import pandas as pd
from api.routers.model.voiceModel.voiceExtraction import get_features

def audio_cut(df):
    audio_features_list = []

    for index, row in df.iterrows():
        file = row['file']
        start = float(row['start'])
        duration = float(row['duration'])
        sr = row['sr']
    
        command = [
            'ffmpeg',
            '-i', str(file),  # 입력 파일(str형태여야함)
            '-f', 's16le',    # PCM 포맷(16비트 리틀 엔디언)
            '-acodec', 'pcm_s16le',
            '-ar', str(sr),   # 샘플 레이트
            '-ac', '1',       # 오디오 채널 수 (모노)
            '-vn',            # 비디오 스트림 무시
            'pipe:1'          # 표준 출력으로 파이프
        ]
        
        # subprocess를 통해 ffmpeg 실행
        process = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=10**8)
        
        # stdout에서 오디오 데이터 읽기
        raw_audio = process.stdout.read()
        audio_array = np.frombuffer(raw_audio, dtype=np.int16)
        audio_array = audio_array.astype(np.float32) / np.iinfo(np.int16).max
        
        # 프로세스 종료
        process.wait()
    
        end = start + duration
    
        start_index = int(start * sr / 1000)
        end_index = int(end * sr / 1000)
    
        segment = audio_array[start_index:end_index]
    
        audio_features = get_features(segment, sr)
        audio_features_list.append(audio_features)
    
    X = pd.DataFrame(audio_features_list)
    return X