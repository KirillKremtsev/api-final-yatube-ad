from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from posts.models import Post, Group, Comment, Follow
from .serializers import (
    PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer
)
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """Работа с публикациями (GET, POST, PUT, PATCH, DELETE)"""
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_queryset(self):
        queryset = Post.objects.all()
        group_id = self.request.query_params.get('group')
        if group_id is not None:
            queryset = queryset.filter(group_id=group_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get', 'post'])
    def comments(self, request, pk=None):
        """Список комментариев и создание нового"""
        post = self.get_object()
        if request.method == 'POST':
            serializer = CommentSerializer(
                data=request.data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=201)
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=['get', 'put', 'patch', 'delete'],
        url_path='comments/(?P<comment_id>[^/.]+)'
    )
    def comment_detail(self, request, pk=None, comment_id=None):
        """Получение, обновление, удаление конкретного комментария"""
        post = self.get_object()
        comment = get_object_or_404(post.comments, id=comment_id)
        if request.method == 'DELETE':
            self.check_object_permissions(request, comment)
            comment.delete()
            return Response(status=204)
        serializer = CommentSerializer(
            comment, data=request.data, partial=True, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        self.check_object_permissions(request, comment)
        serializer.save()
        return Response(serializer.data)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Только чтение списка сообществ и детальной информации"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    Работа с подписками:
    GET    /follow/ - список подписок текущего пользователя (с поиском по following__username)
    POST   /follow/ - подписаться на пользователя
    """
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
