import cv2
import os
import asyncio.subprocess
import uuid
from fastapi import File, HTTPException, UploadFile, APIRouter
import numpy as np
import pandas as pd
import requests
import asyncio
import aiofiles
from sklearn.preprocessing import StandardScaler
from api.routers.model.voiceModel.audioCut import audio_cut
from .schemas import emotion_Result, stt_Result
from .model.voiceModel.audioTextModel import Audio_text_model
from .model.stt.sttModel import get_sample_rate, stt
from .model.voiceModel.textEmbedding import text_embedding
from .model.stt.saveTempFile import save_temp_file
from .model.imageModel import faceDetection, faceExtraction, imageModel

router = APIRouter()

async def convert_webm_to_mp3(input_path: str, output_path: str):
    command = ['ffmpeg', '-y', '-i', input_path, '-q:a', '0', '-map', 'a', output_path]
    process = await asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        raise HTTPException(status_code=500, detail=f"Error converting to mp3: {stderr.decode()}")

async def convert_webm_to_mp4(input_path: str, output_path: str):
    command = ['ffmpeg', '-y', '-i', input_path, '-c:v', 'libx264', '-c:a', 'aac', output_path]
    process = await asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        raise HTTPException(status_code=500, detail=f"Error converting to mp4: {stderr.decode()}")

@router.post("/upload-video/{roomID}/{userID}/{count}")
async def upload_video(roomID: float, userID: float, count: int, audiofile: UploadFile = File(...), videofile: UploadFile = File(...)):
    base_url = "http://43.203.209.38:8080"
    
    unique_id = uuid.uuid4().hex
    temp_audio_file_path = await save_temp_file(audiofile)
    temp_video_file_path = await save_temp_file(videofile)
    
    temp_mp3_path = temp_audio_file_path.replace(".webm", f"_{unique_id}.mp3")
    temp_mp4_path = temp_video_file_path.replace(".webm", f"_{unique_id}.mp4")

    await convert_webm_to_mp3(temp_audio_file_path, temp_mp3_path)
    await convert_webm_to_mp4(temp_video_file_path, temp_mp4_path)
    
    try:
        if temp_mp3_path and os.path.exists(temp_mp3_path):  # 파일 경로 확인
            sr = get_sample_rate(temp_mp3_path)  # 파일 샘플 레이트 추출
            df = stt(temp_mp3_path)  # 음성 인식

    except Exception as e:
        print(f"An error occurred: {str(e)}")  # 로그에 오류 메시지 출력
        if temp_mp3_path and os.path.exists(temp_mp3_path):
            os.remove(temp_mp3_path)
        raise HTTPException(status_code=500, detail=str(e))
    
    for i in range(len(df)):
        content = df['text'].iloc[i]
        millisec = df['start'].iloc[i] + 10000 * count
        stt_result = stt_Result.stt_Result(content=content, millisec=millisec)
        save_stt_url = f'{base_url}/live/{int(roomID)}/{int(userID)}/save/content'
        try:
            response = requests.post(save_stt_url, json=stt_result.dict())
            response.raise_for_status()  # 상태 코드가 200이 아니면 예외 발생
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    X_audio = audio_cut(df)
    dfText = pd.DataFrame(df['text'])
    print(X_audio.shape, dfText.shape)
    
    if X_audio.empty or dfText.empty:
        raise HTTPException(status_code=400, detail="Audio or Text data is empty")

    # X_audio와 dfText를 병합하기 전에 2D 배열로 변환
    X_audio = X_audio.values.reshape(-1, 1)
    dfText = dfText.values.reshape(-1, 1)
    
    X = np.concatenate([X_audio, dfText], axis=1)
    
    txt_embed = text_embedding(model_name='jhgan/ko-sbert-multitask')
    X = txt_embed.transform(X)
    
    if X.size == 0:
        raise HTTPException(status_code=400, detail="Transformed text embedding resulted in an empty array")
    
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    model = Audio_text_model()
    dir_path = os.path.dirname(os.path.realpath(__file__))  # 현재 파일의 디렉토리 경로
    weights_path = os.path.join(dir_path, 'audio_text_model_weights.h5')

    model.load_weights(weights_path)
    prediction = model.predict(X)
    prediction = pd.DataFrame(prediction)
    
    s = []
    for i in range(len(prediction)):
        score = (prediction.iloc[i, 0] * 1 +
                 prediction.iloc[i, 1] * 1 +
                 prediction.iloc[i, 2] * 1 +
                 prediction.iloc[i, 3] * 8 +
                 prediction.iloc[i, 4] * 5 +
                 prediction.iloc[i, 5] * 1)
        score = score * 10
        s.append(score)
    audio_final_score = (float)(round(sum(s) / len(s), 2))
    
    img_final_score_list = []
    score = []

    cap = cv2.VideoCapture(temp_mp4_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = 0.2
    frame_interval = int(fps * interval)

    c = 0
    cnt = 0
    success, image = cap.read()
      
    while success:
        if cnt % frame_interval == 0:
            gray, detected_faces, coord = faceDetection.detect_face(image)
            face_zoom = faceExtraction.extract_face_features(gray, detected_faces, coord)
            if len(face_zoom) > 0:
                face_img = np.reshape(face_zoom[0], (48, 48, 1))
                face_img_batch = np.expand_dims(face_img, axis=0)

                imgModel = imageModel.img_model()
                try:
                    predictions = np.array(imgModel.predict(face_img_batch)[0])
                except Exception as e:
                    print(f"Error during prediction: {str(e)}")
                    raise HTTPException(status_code=500, detail="Prediction error")

                s = (predictions[0] * 0 + predictions[1] * 5 + predictions[2] * 10) * 10
                score.append(s)
                c += 1
                print(f'counts : {c}')
                
        success, image = cap.read()
        cnt += 1

    if len(score) > 0:
        d = round(sum(score) / len(score), 2)
    else:
        d = 0
    img_final_score_list.append(d)
    img_final_score = img_final_score_list[0]

    save_emotion_url = f'{base_url}/live/{int(roomID)}/{int(userID)}/save/emotion'
    try:
        audio_final_score = int(round(audio_final_score))
        img_final_score = int(round(img_final_score))
        emotion_result = emotion_Result.emotion_Result(image=img_final_score, voice=audio_final_score)
        response = requests.post(save_emotion_url, json=emotion_result.dict())
        response.raise_for_status()  # 상태 코드가 200이 아니면 예외 발생
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # 임시 파일 삭제
        if temp_mp3_path and os.path.exists(temp_mp3_path):
            os.remove(temp_mp3_path)
            print(f"Deleted temp mp3 file: {temp_mp3_path}")
                
        if temp_mp4_path and os.path.exists(temp_mp4_path):
            os.remove(temp_mp4_path)
            print(f"Deleted temp mp4 file: {temp_mp4_path}")

        score.clear()
        cap.release()

    return
