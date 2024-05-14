from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from .serializers import SentimentAnalysisSerializer
from .models import SentimentAnalysis
from openai import OpenAI


from utils.utils import get_env_variable
from utils.constants import ENGINE

client = OpenAI(api_key=get_env_variable("OPENAI_API_KEY"))

# rate limit the sentiment analysis endpoint
class SentimentAnalysisThrottle(UserRateThrottle):
    rate = '100/minute'
    
class SentimentAnalysisView(APIView):
    throttle_classes = [SentimentAnalysisThrottle]

    def post(self, request):
        # validate the request data
        serializer = SentimentAnalysisSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        text = serializer.validated_data['text']
        instance, created = SentimentAnalysis.get_or_create(text)

        # if the sentiment is already analyzed, return the result
        if not created and instance.sentiment:
            return Response({'sentiment': instance.sentiment})

        messages = [
            {
                "role": "system",
                "content": "You will be asked to analyze the sentiment of a text. Please provide your analysis in a structured format using HTML. The template below is provided as a starting point, but you must improve and enhance it to deliver a more comprehensive and insightful sentiment analysis."
            },
            {
                "role": "user",
                "content": text
            },
            {
                "role": "system",
                "content": """
        Please provide a sentiment analysis of the text, including the following:

        <ol>
        <li>Overall Sentiment:
            <ul>
            <li>Score: (integer from -5 to 5, where -5 is extremely negative, 0 is neutral, and 5 is extremely positive)</li>
            <li>Label: (Positive, Negative, or Neutral)</li>
            <li>Explanation: (brief explanation of the overall sentiment)</li>
            </ul>
        </li>
        <li>Key Phrases and Their Sentiments:
            <ul>
            <li><span style="background-color: (color code for the sentiment)">Phrase 1: (relevant phrase from the text)</span>
                <ul>
                <li>Sentiment: (Positive, Negative, or Neutral)</li>
                </ul>
            </li>
            <li><span style="background-color: (color code for the sentiment)">Phrase 2: (relevant phrase from the text)</span>
                <ul>
                <li>Sentiment: (Positive, Negative, or Neutral)</li>
                </ul>
            </li>
            ...
            </ul>
        </li>
        <li>Specific Emotions or Reactions Identified:
            <ul>
            <li>Emotion 1: (identified emotion or reaction)</li>
            <li>Emotion 2: (identified emotion or reaction)</li>
            ...
            </ul>
        </li>
        <li>Additional Sentiment Details:
            <ul>
            <li>Detail 1: (any additional relevant sentiment details)</li>
            <li>Detail 2: (any additional relevant sentiment details)</li>
            ...
            </ul>
        </li>
       
        </ol>

        The template above is provided as a starting point, but it is crucial that you improve and enhance it to deliver a more comprehensive and insightful sentiment analysis. You must modify the structure, add or remove sections, and include any additional information or insights that you think would be valuable for the sentiment analysis.

        Please format your response using HTML, including the appropriate tags for ordered lists, unordered lists, and list items. Apply the color to the background of the phrases using the <span> tag with the style attribute.

        Remember, improving and enhancing the template is a requirement, not just a suggestion. Use your intelligence, creativity, and expertise to provide the best possible sentiment analysis.
        """
            }
        ]

        try:
            response = client.chat.completions.create(
                model=ENGINE, 
                messages=messages
            )
            
            sentiment= response.choices[0].message.content

            if sentiment:
                instance.sentiment = sentiment
                instance.save()

            return Response({'sentiment': sentiment})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
