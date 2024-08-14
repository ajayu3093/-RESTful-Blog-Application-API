from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Blog, Comment
from .serializer import BlogSerializer, CommentSerializer
import logging

logger = logging.getLogger(__name__)

# PublicBlog View
class PublicBlog(APIView):
    def get(self, request):
        try:
            blogs = Blog.objects.all().order_by('?')
            
            # Search functionality
            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search) | Q(text_blog__icontains=search))
            
            # Pagination
            paginator = Paginator(blogs, 5)
            page_number = request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)

            serializer = BlogSerializer(page_obj, many=True)

            return Response(
                {
                    'data': serializer.data,
                    'message': 'Blogs Fetched successfully'
                }, status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.exception('Error fetching blogs')
            return Response(
                {
                    'data': {},
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST
            )


# BlogView for authenticated users
class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        try:
            blogs = Blog.objects.filter(user=request.user)
            
            # Search functionality
            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search) | Q(text_blog__icontains=search))
            
            serializer = BlogSerializer(blogs, many=True)

            return Response(
                {
                    'data': serializer.data,
                    'message': 'Blogs Fetched successfully'
                }, status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.exception('Error fetching user blogs')
            return Response(
                {
                    'data': {},
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST
            )
    
    def post(self, request):
        try:
            data = request.data.copy()  # Make a mutable copy of request data
            data['user'] = request.user.id
            
            serializer = BlogSerializer(data=data)
            
            if not serializer.is_valid():
                logger.debug(f'Serializer errors: {serializer.errors}')
                return Response(
                    {
                        'data': serializer.errors,
                        'message': 'Invalid Data'
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save()
            return Response(
                {
                    'data': serializer.data,
                    'message': 'Blog Created Successfully'
                }, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.exception('Error creating blog')
            return Response(
                {
                    'data': {},
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST
            )
    
    def patch(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid=data['uid'])
           
            if not blog.exists():
                return Response(
                    {
                        'data': {},
                        'message': 'Invalid blog uid'
                    }, status=status.HTTP_404_NOT_FOUND
                )
           
            if request.user.id != blog[0].user.id:
                return Response(
                    {
                        'data': {},
                        'message': 'You are not allowed to edit this blog'
                    }, status=status.HTTP_403_FORBIDDEN
                )
               
            serializer = BlogSerializer(blog[0], data=data, partial=True)
           
            if not serializer.is_valid():
                return Response(
                    {
                        'data': serializer.errors,
                        'message': 'Something Went Wrong'
                    }, status=status.HTTP_400_BAD_REQUEST
                )
           
            serializer.save()
            return Response(
                {
                    'data': serializer.data,
                    'message': 'Blog Updated Successfully'
                }, status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.exception('Error updating blog')
            return Response(
                {
                    'data': {},
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST
            )
               
    def delete(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid=data['uid'])
           
            if not blog.exists():
                return Response(
                    {
                        'data': {},
                        'message': 'Invalid blog uid'
                    }, status=status.HTTP_404_NOT_FOUND
                )
           
            if request.user.id != blog[0].user.id:
                return Response(
                    {
                        'data': {},
                        'message': 'You are not allowed to delete this blog'
                    }, status=status.HTTP_403_FORBIDDEN
                )
               
            blog[0].delete()
            return Response(
                {
                    'data': {},
                    'message': 'Blog deleted Successfully'
                }, status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.exception('Error deleting blog')
            return Response(
                {
                    'data': {},
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST
            )


# CommentView for managing comments
class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, post_id):
        try:
            comments = Comment.objects.filter(post_id=post_id)
            serializer = CommentSerializer(comments, many=True)
            return Response(
                {
                    'data': serializer.data,
                    'message': 'Comments fetched successfully'
                }, status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.exception('Error fetching comments')
            return Response(
                {
                    'data': {},
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request, post_id):
        try:
            data = request.data.copy()  # Make a mutable copy of request data
            data['author'] = request.user.id
            data['post'] = post_id

            serializer = CommentSerializer(data=data)

            if not serializer.is_valid():
                logger.debug(f'Serializer errors: {serializer.errors}')
                return Response(
                    {
                        'data': serializer.errors,
                        'message': 'Invalid data'
                    }, status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()
            return Response(
                {
                    'data': serializer.data,
                    'message': 'Comment created successfully'
                }, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.exception('Error creating comment')
            return Response(
                {
                    'data': {},
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, post_id, comment_id):
        try:
            comment = Comment.objects.filter(uid=comment_id, post_id=post_id, author=request.user)

            if not comment.exists():
                return Response(
                    {
                        'data': {},
                        'message': 'Comment not found or not authorized to delete'
                    }, status=status.HTTP_404_NOT_FOUND
                )

            comment[0].delete()
            return Response(
                {
                    'data': {},
                    'message': 'Comment deleted successfully'
                }, status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.exception('Error deleting comment')
            return Response(
                {
                    'data': {},
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST
            )
