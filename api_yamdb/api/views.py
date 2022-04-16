from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from reviews.models import Category, Comments, Genre, Review, Title, User

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrStaff
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, ReviewSerializer, SignupSerializer,
                          TitleGETSerializer, TitlePOSTSerializer,
                          TokenSerializer, UserSerializer)
from .utils import get_tokens

USER_ERROR = 'Пользователь с таким email уже существует!'
CODE_INFO = 'Код подтверждения отправлен на Ваш email!'
CODE_ERROR = 'Неверный код подтверждения'


class SignupView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        username = serializer.data.get('username')

        if User.objects.filter(email=email).exists():
            return Response(
                USER_ERROR, status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.create_user(
            username=username, email=email, password=None
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Код подтверждения',
            confirmation_code,
            settings.DEFAULT_FROM_EMAIL,
            (email,),
            fail_silently=False,
        )
        return Response({'email': email, 'username': username},
                        status=status.HTTP_200_OK)


class GetJWTTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.data['username']

        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.data['confirmation_code']
        if not default_token_generator.check_token(
            user, confirmation_code
        ):
            return Response(
                CODE_ERROR, status=status.HTTP_400_BAD_REQUEST
            )
        response = get_tokens(user)
        return Response(response, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username', )

    @action(detail=False, methods=('get', 'patch',),
            permission_classes=(IsAuthenticated, IsAuthorOrStaff,))
    def me(self, request):
        user = self.request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            user = get_object_or_404(User, username=request.user.username)
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrStaff]

    def get_queryset(self, *args, **kwargs):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(
            Review, id=self.kwargs['review_id'], title=title
        )
        return Comments.objects.filter(review=review)

    def perform_create(self, serializer, *args, **kwargs):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrStaff]
    serializer_class = ReviewSerializer

    def get_queryset(self, *args, **kwargs):
        title = Title.objects.get(id=self.kwargs['title_id'])
        return Review.objects.filter(title=title)

    def get_serializer_context(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        context = super(ReviewViewSet, self).get_serializer_context()
        context.update({'title': title,
                        'author': self.request.user,
                        'request.method': self.request.method})
        return context

    def perform_create(self, serializer, *args, **kwargs):
        title = Title.objects.get(id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CategoryViewSet(CreateListDestroyViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyViewSet):

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):

    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return TitlePOSTSerializer
        return TitleGETSerializer
