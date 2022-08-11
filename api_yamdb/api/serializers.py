from review.models import Comment, Review
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ['title']

    def validate_score(self, value):
        if 0 >= value > 10:
            raise serializers.ValidationError('Проверьте оценку')
        return value
