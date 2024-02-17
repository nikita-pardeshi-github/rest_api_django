from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Person
from .serializers import PersonSerializer, LoginSerializer, RegisterSerializer
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.paginator import Paginator


@api_view(['GET', 'POST'])
def home(request):
    course = {
        'course_name' : 'Python',
        'frameworks' : ['flask', 'django', 'fast api'],
        'course_provider': 'scaler'
    }
    if request.method == 'GET':
        print("GET Method called")
        # you can read query param like below : input url
        search_param = request.query_params.get('search', None)
        print(f"--- Search parameter : {search_param}")
        return Response(course)
    elif request.method == 'POST':
        print("POST Method called")
        data = request.data
        print(data)
        print(f"name => {data['name']}")
        print(f"age  => {data['age']}")
        return Response(course)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def person(request):
    if request.method == 'GET':
        objs = Person.objects.filter(color__isnull = False)
        serializer = PersonSerializer(objs, many= True)
        return Response (serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = PersonSerializer(data= data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    # DOESN'T SUPPORT PARTIAL UPDATE
    elif request.method == 'PUT':
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(obj, data= data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    # SUPPORTS PARTIAL UPDATE
    elif request.method == 'PATCH':
        data = request.data
        obj = Person.objects.get(id = data['id'])
        serializer = PersonSerializer(obj, data= data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == "DELETE":
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({
            "status" : "deleted id ("+str(data['id'])+") successfully"
        })


@api_view(['GET', 'POST', 'PATCH', 'PUT'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data= data)

    if serializer.is_valid():
        data = serializer.validated_data
        return Response({"message": "success"})

    return Response(serializer.errors)


class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        print(request.user)
        size = 2
        page = request.GET.get('page', 1)
        objs = Person.objects.filter(color__isnull = False)
        try:
            paginator = Paginator(objs, size)
            print(paginator.page(page))
            serializer = PersonSerializer(paginator.page(page), many=True)
            # serializer = PersonSerializer(objs, many=True)
        except Exception as e:
            print("In exception")
            return Response({
                "message" : "invalid page"
            })

        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = PersonSerializer(data=data)
        print(f"===========> serializer {serializer}")
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def put(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])
        obj.delete()
        return Response({
            "status": "deleted id (" + str(data['id']) + ") successfully"
        })


class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()


    def list(self, request):
        search_param = request.query_params.get('search', None)
        queryset = self.queryset.filter(name__startswith = search_param)
        serializer = PersonSerializer(queryset, many=True)
        return Response({"data": serializer.data }, status=status.HTTP_200_OK)


class RegisterAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data= data)

        if not serializer.is_valid():
            return  Response({
                "status": False,
                "message": serializer.errors
            }, status = status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": True,
            "message": "user created"
        }, status = status.HTTP_201_CREATED)


class LoginAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)

        if not serializer.is_valid():
            return Response({
                "status": False,
                "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        print(serializer.data)
        user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
        if not user:
            return Response({
                "status": False,
                "message": "Invalid credentials"
            }, status=status.HTTP_400_BAD_REQUEST)

        token = Token.objects.get_or_create(user=user)
        return Response({
            "status": 200,
            "message": "user created",
            "token": str(token)
        }, status=status.HTTP_201_CREATED)