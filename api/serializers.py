from rest_framework import serializers

# using the serializer class to validate the input data
class SentimentAnalysisSerializer(serializers.Serializer):
    text = serializers.CharField(required=True)