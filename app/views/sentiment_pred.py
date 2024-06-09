import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from app.log.app_logger import logger

def download_nltk_words():
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
        logger.info("NLTK VADER lexicon data is already present.")
    except LookupError:
        
        logger.info("Downloading NLTK words data...")
        nltk.download('vader_lexicon')
        logger.info("NLTK words data downloaded successfully.")

download_nltk_words()

def sentiment_analysis(data):
    sia = SentimentIntensityAnalyzer()
    logger.info(f"Getting sentiment score for comments")
    
    final_output = []
    for val in range(len(data)):
        result = {}
        text = data[val]["text"]
        sentiment_scores = sia.polarity_scores(text)
        result["comment_id"] = data[val]["id"]
        result["text"] = data[val]["text"]
        result["polarity_score"] = sentiment_scores['compound']
        result["sentiment"] = 'positive' if result["polarity_score"] > 0 else 'negative' if result["polarity_score"] < 0 else 'neutral'
        if result:
            final_output.append(result)
    return final_output