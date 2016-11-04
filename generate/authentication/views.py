from rest_framework import parsers, renderers
from rest_framework import viewsets, exceptions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

# Django REST Authentication
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission

from utils.helpers import success_response, error_response
from serializers import UserSerializer
from authentication.models import User
from utils.decorators import api_key_checker


SAFE_METHODS = ['POST']

class IsAuthenticatedOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated()):
            return True
        return False

class UserList(APIView):
    """
    Creates a new user.
    """
    authentication_classes = (BasicAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @api_key_checker
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(success_response(serializer.data))

    @api_key_checker
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            if not 'password' in request.data:
                return Response(error_response('Password not provided.'),
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                user = serializer.save()
                user.set_password(request.data['password'])
            return Response(success_response(serializer.data),
                            status=status.HTTP_201_CREATED)
        return Response(error_response(serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)

    @api_key_checker
    def put(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(success_response(serializer.data),
                            status=status.HTTP_201_CREATED)
        return Response(error_response(serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)

    """
    @api_key_checker
    def delete(self, request, format=None):
        user = self.get_object(pk, request.user)
        user.delete()
        return Response(success_response("null"),
                        status=status.HTTP_204_NO_CONTENT)
    """

class ObtainAuthToken(APIView):
    """
    Overriding this Django REST class
    to also return the User.
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    @api_key_checker
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            user_serialized = UserSerializer(user)
            return Response(success_response(user_serialized.data))
        else:
            return Response(error_response("User or password incorrect."))


class CheckSession(APIView):
    """
    Validates if the session is still valid.
    """
    permission_classes = (IsAuthenticated,)

    @api_key_checker
    def get(self, request, *args, **kwargs):
        try:
            provided_token = request.META['HTTP_AUTHORIZATION']
            provided_token = provided_token.replace('Token ', '')
            token = Token.objects.select_related('user').get(key=provided_token)
        except self.model.DoesNotExist:
            # modify the original exception response
            raise exceptions.APIException("Token not valid.")

        if not token.user.is_active:
            # can also modify this exception message
            return Response(error_response("User inactive or deleted."))

        user_serialized = UserSerializer(request.user)
        return Response(success_response(user_serialized.data))

