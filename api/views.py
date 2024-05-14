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
                    "content": """
            You will be asked to analyze the sentiment of a text. Please provide your analysis in a structured format using Markdown as specified below:
            - **Overall Sentiment**: **Positive** (Score: `0.85`)
            - **Key Phrases**:
                - ![#00FF00](https://via.placeholder.com/15/00FF00/000000?text=+) "enjoyed the service" (Positive)
                - ![#00FF00](https://via.placeholder.com/15/00FF00/000000?text=+) "will recommend to others" (Positive)
            - **Specific Emotions**:
                - **Happiness**: "enjoyed"
                - **Satisfaction**: "recommend"
            - **Additional Details**:
                - The text displays a consistently positive tone, particularly emphasizing satisfaction and happiness.
                    """
                },
                {"role": "user", "content": text},
                {
                    "role": "system",
                    "content": """
            Please summarize the key points regarding the sentiment of the text in a bullet point list using Markdown. Make sure to include the following elements:
            - **Overall Sentiment**: Indicate the sentiment as **Positive**, **Negative**, or **Neutral** along with the sentiment score (e.g., Score: `0.75`).
            - **Key Phrases**: Highlight specific phrases that contribute to the sentiment. Use colored indicators for emphasis:
                - Positive phrases in green: ![#00FF00](https://via.placeholder.com/15/00FF00/000000?text=+) "example positive phrase"
                - Negative phrases in red: ![#FF0000](https://via.placeholder.com/15/FF0000/000000?text=+) "example negative phrase"
                - Neutral phrases in yellow: ![#FFFF00](https://via.placeholder.com/15/FFFF00/000000?text=+) "example neutral phrase"
            - **Specific Emotions**: Identify specific emotions or reactions mentioned in the text with examples.
            - **Additional Details**: Any other relevant sentiment details that provide more context or insight.
            
            Here's an example of the expected format:
            
            ```markdown
            - **Overall Sentiment**: **Positive** (Score: `0.85`)
            - **Key Phrases**:
                - ![#00FF00](https://via.placeholder.com/15/00FF00/000000?text=+) "enjoyed the service" (Positive)
                - ![#00FF00](https://via.placeholder.com/15/00FF00/000000?text=+) "will recommend to others" (Positive)
            - **Specific Emotions**:
                - **Happiness**: "enjoyed"
                - **Satisfaction**: "recommend"
            - **Additional Details**:
                - The text displays a consistently positive tone, particularly emphasizing satisfaction and happiness.
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
