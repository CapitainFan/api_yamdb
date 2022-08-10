from review.models import Comment, Review
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
