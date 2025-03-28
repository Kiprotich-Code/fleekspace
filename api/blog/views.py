from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

from blog.models import Category, Comment, Post
from blog.serializers import (
    CategoryReadSerializer,
    CommentReadSerializer,
    CommentWriteSerializer,
    PostReadSerializer,
    PostWriteSerializer,
)

from .permissions import IsAuthorOrReadOnly

# Category is going to be read-only, so we use ReadOnlyModelViewSet
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and Retrieve post categories
    """

    queryset = Category.objects.all()
    serializer_class = CategoryReadSerializer
    permission_classes = (permissions.AllowAny,)

class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD posts
    """

    queryset = Post.objects.all()

    # get_serializer_class(self) method
    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return PostWriteSerializer

        return PostReadSerializer

    # get_permissions(self) method helps you separate 
    # permissions for different actions inside the same view.
    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()


    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def my_posts(self, request):
        """
        Custom action to fetch posts belonging to the logged-in user.
        """
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        posts = Post.objects.filter(author=request.user)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    

    def perform_create(self, serializer):
        """
        Automatically set the author to the currently logged in user when creating posts.
        """
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD comments for a particular post
    """

    queryset = Comment.objects.all()

    def get_queryset(self):
        res = super().get_queryset()
        post_id = self.kwargs.get("post_id")
        return res.filter(post__id=post_id)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return CommentWriteSerializer

        return CommentReadSerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()

# Here, we are using the normal APIView class
class LikePostAPIView(APIView):
    """
    Like, Dislike a post
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        user = request.user
        post = get_object_or_404(Post, pk=pk)

        if user in post.likes.all():
            post.likes.remove(user)

        else:
            post.likes.add(user)

        return Response(status=status.HTTP_200_OK)