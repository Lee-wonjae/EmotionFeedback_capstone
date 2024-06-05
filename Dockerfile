# 베이스 이미지 설정
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    gcc \
    g++ \
    python3-dev \
    libhdf5-dev \
    pkg-config \
    libglib2.0-dev \
    build-essential \
    ffmpeg \
    libvpx-dev \
    libvorbis0a \
    libopus0 \
    libx264-dev \
    libx265-dev \
    libwebp-dev \
    libass-dev \
    libfreetype6-dev \
    libfribidi-dev \
    libmp3lame-dev \
    libopenjp2-7-dev \
    libopus-dev \
    libtheora-dev \
    libvorbis-dev \
    libxvidcore-dev \
    libaom-dev \
    libdav1d-dev \
    libsvtav1-dev \
    && apt-get clean

# ffmpeg와 ffprobe가 설치되었는지 확인
RUN ffmpeg -version && ffprobe -version

# 종속성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 포트 설정
EXPOSE 8000

# 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]