import datetime

from django.db.models import Avg
from rest_framework import serializers, validators
from rest_framework.serializers import ModelSerializer
from reviews.models import Category, Comments, Genre, Review, Title, User


class UserSerializer(ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User
        lookup_field = 'username'


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Такой пользователь уже существует'
            )
        if value == 'me':
            raise serializers.ValidationError(
                'Имя пользователя недопустимо'
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    def validate(self, data):
        review = Review.objects.filter(title=self.context['title'],
                                       author=self.context['author'])
        if review.exists() and self.context['request.method'] == 'POST':
            raise serializers.ValidationError(
                'Отзыв уже написан.'
            )
        return data

    class Meta:
        exclude = ('title',)
        model = Review


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        exclude = ('review',)
        model = Comments


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitlePOSTSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, title):
        rating = Review.objects.filter(title_id=title.id).aggregate(
            Avg('score'))
        if rating:
            return rating['score__avg']
        return None

    def validate_year(self, value):
        if value > datetime.datetime.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего.'
            )
        if value < 1895:
            raise serializers.ValidationError(
                'Год выпуска не может быть меньше 1895.'
            )
        return value


class TitleGETSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, title):
        rating = Review.objects.filter(title_id=title.id).aggregate(
            Avg('score'))
        if rating:
            return rating['score__avg']
        return None
