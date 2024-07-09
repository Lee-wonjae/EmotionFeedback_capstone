# Emotion Feedback Capstone Project

This project, "Emotion Feedback," aims to recommend conversation topics for video chats based on real-time emotion analysis.

## Project Overview

### Team Members
- 이원재
- 이준범
- 권영우
- 심재호

### Introduction
"Emotion Feedback" is a system designed to alleviate awkward atmospheres and lack of conversation topics during video chats by recommending topics based on real-time emotion analysis.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Problem Statement](#problem-statement)
3. [System Features](#system-features)
4. [Data Sources](#data-sources)
5. [Models and Outputs](#models-and-outputs)
6. [Performance Metrics](#performance-metrics)
7. [Recommendation Types](#recommendation-types)
8. [System Architecture](#system-architecture)
9. [Evaluation and Future Plans](#evaluation-and-future-plans)
10. [Team and Contributions](#team-and-contributions)
11. [License](#license)

## Problem Statement

### Common Issues in Conversations:
- Awkward atmosphere
- Lack of conversation topics

### Solution:
- Emotion-based conversation topic recommendation

## System Features

- **Real-time Emotion Analysis**: Analyze and store the emotions of the participants in real-time.
- **Emotion-based Topic Recommendation**: Recommend conversation topics based on the stored emotions and conversation content.
- **Understanding Partner’s Favorability**: Analyze and display the favorability graph of the conversation partner post-conversation.

## Data Sources

- **FER-2013 (Kaggle)**: Dataset labeled with seven types of emotions (28,709 samples).
- **Self-Collected Data (Google)**: Dataset labeled from 0 to 9 (597 samples).
- **Multimodal Video Data (AI Hub)**: Labeled data showing conversation and actions in specific situations, including positive/negative emotions, intensity, and dialogues.

## Models and Outputs

### Video Model
- Outputs the probability of favorability based on visual data.

### Audio/Text Model
- Outputs the probability of favorability based on audio and text data.

### Final Favorability Score
- Combines the outputs from the video and audio/text models:
  ```markdown
  Final Favorability = (0.43 * Video Model Score) + (0.57 * Audio/Text Model Score)
## Recommendation Types

- **Profile-Based Recommendation**
- **Favorability and Conversation Content-Based Recommendation**
- **Random Topic Recommendation**

## System Architecture

### Data Collection

1. **Video Call**: Users start a video call through the system.
2. **Data Collection and Analysis**:
   - **Image Analysis**: Analyze the user's facial expressions captured from the video.
   - **Text Analysis**: Convert the conversation into text and analyze the sentiment.
   - **Audio Analysis**: Analyze the tone and speed of the user's voice to determine the emotional state.

### Data Processing

- Preprocessing images to fit CNN models.
- Converting and preprocessing audio and text data for analysis.

### Favorability Detection

- Combining data from text, image, and audio analysis to evaluate the favorability between users.

### Real-time Topic Recommendation

- Using stored data and GPT API to recommend conversation topics in real-time.

### Data Storage and Feedback

- Storing analyzed text data and favorability scores in a database.
- Providing feedback to users based on stored data after the conversation ends.

### Technical Stack

- **Frontend**: React, Figma, WebRTC, MediaStream API
- **Backend**: FastAPI, SpringBoot, WebSocket, PostgreSQL, AWS
- **Modeling**: CNN for image, audio, and text analysis, LangChain for natural language processing

## Evaluation and Future Plans

Despite achieving significant accuracy for emotion detection, continuous improvements are planned, including expanding the dataset, refining models, and exploring additional applications such as enhancing conversational flow and user engagement.

### Challenges and Solutions

- **STT Delay**: Mitigated by adding a 3-second delay to accommodate processing time.
- **Model Accuracy**: Improved by modifying preprocessing steps and model parameters, achieving 78% accuracy for image models and 82% for audio/text models.
- **Real-time Processing**: Achieved using asynchronous processing with FastAPI to handle model server communications.

### Future Plans

- Increase the amount of quality data to improve model performance.
- Explore further applications, such as tracking the ball's trajectory, measuring speed, and predicting match outcomes.

## Team and Contributions

- **이원재**: Model Server API Development and Deployment, Prompt Engineering
- **이준범**: Backend Server API Development, Signaling Server Development
- **권영우**: Frontend Development
- **심재호**: Modeling

## License

This project is licensed under the MIT License.
