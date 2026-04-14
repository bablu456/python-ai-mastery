from transformers import pipeline
import time

print(" Loading local AI model into memory... First time thoda download hoga\n")


classifier = pipeline("sentiment-analysis")

reviews = [
    "Google API limits frustrated me a lot today, it was a terrible experience.",
    "But I did not give up! I built my own local AI model and it works amazingly well! "
]

print("--- AI Analysis Results ---\n")

for review in reviews:
    time.sleep(1) # Bas thoda dramatic effect ke liye
    result = classifier(review)[0]
    
    print(f"Text: '{review}'")
    print(f"Prediction: {result['label']} (Confidence: {round(result['score'] * 100, 2)}%)\n")