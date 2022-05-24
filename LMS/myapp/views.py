from ast import Pass
import imp
import json
from django.shortcuts import render


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter

from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import AuthenticationFailed

from . models import *
from .serializers import *
import jwt
import datetime

CREATE_SUCCESS = 'created'


class Login(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = NewUser.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('email  is incorrect!!')

        # if user.password == password:
        #     raise AuthenticationFailed('password is incorrect!!')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password!')
        
        # user1 = NewUser.objects. filter(id = user.id).first()
        serializer = NewUserSerializer(user)

        payload = {
            'id': user.id,
            'user': serializer.data,
            'name': user.user_name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365),
            'iat': datetime.datetime.utcnow()
        }

        print(datetime.timedelta(days=365))

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        return Response({
            'token': token
        })

class Logout(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('token')
        response.data = {
            'massage': 'success'
        }
        return  response


class CustomUser(ListAPIView):
    queryset = NewUser.objects.all()
    serializer_class = NewUserSerializer

    def get_queryset(self):
        user = NewUser.objects.all()
        return user

    def get(self, request, id=None):
        if id:
            user = NewUser.objects.get(id=id)
            serializer = NewUserSerializer(user, context={"request": request})
            return Response(serializer.data)

        user = self.get_queryset()
        serializer = NewUserSerializer(
            user, many=True, context={"request": request})
        # print(serializer.data)
        return Response(serializer.data)

    def post(self, request):
        serializer = NewUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['password'] = make_password(
            serializer.validated_data['password'])
        print(serializer.validated_data['password'])
        serializer.save()

        payload = {
            'user': serializer.data,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365),
            'iat': datetime.datetime.utcnow()
        }

        print(datetime.timedelta(days=365))

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        return Response({
            'token': token
        })
        # return Response(serializer.data)
    
    def put(self, request,id=None):
        if id:
            user = NewUser.objects.get(id=id)
            serializer = NewUserSerializer(user, data=request.data)
            data = {}
            if serializer.is_valid(raise_exception=True):
                serializer.save();
                data["status"] = "sucuess"
                return Response(data)
            else:  
                data['status'] = "error"
                return Response(data)

    def delete(self, request,id=None):
        if id:
            user = NewUser.objects.get(id=id)
            serializer = user.delete()
            data = {}
            if user:
                data["status"] = "sucuess"
                return Response(data)
            else:  
                data['status'] = "error"
                return Response(data)



class bookList(ListAPIView):

    queryset = book.objects.all()
    serializer_class = bookserializer
    filter_backends = [SearchFilter]
    search_fields = ['book_name']

    def get(self, request, id=None):
        if id:
            book1 = book.objects.get(id=id)
            serializer = bookserializer(book1, context={"request": request})
            return Response(serializer.data)

        book1 = book.objects.all()
        serializer = bookserializer(
            book1, many=True, context={"request": request})
        return Response(serializer.data)

        # book1 = book.objects.all()
        #

        # # print(serializer.data)
        # return Response(serializer.data)

    def post(self, request):
        serializer = bookserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def put(self, request,id=None):
        if id:
            book1 = book.objects.get(id=id)
            serializer = bookserializer(book1, data=request.data)
            data = {}
            if serializer.is_valid(raise_exception=True):
                serializer.save();
                data["status"] = "sucuess"
                return Response(data)
            else:  
                data['status'] = "error"
                return Response(data)

    def delete(self, request,id=None):
        if id:
            book1 = book.objects.get(id=id)
            serializer = book1.delete()
            data = {}
            if book1:
                data["status"] = "sucuess"
                return Response(data)
            else:  
                data['status'] = "error"
                return Response(data)



class SearchbookList(ListAPIView):

    queryset = book.objects.all()
    serializer_class = bookserializer
    filter_backends = [SearchFilter]
    search_fields = ['book_name']


class borrowList(ListAPIView):

    queryset = borrow.objects.all()
    serializer_class = borrowserializer

    def get_queryset(self):
        borrow1 = borrow.objects.all()
        return borrow1

    def get(self, request, id=None):
        if id:
            borrow1 = borrow.objects.get(id=id)
            serializer = borrowserializer(
                borrow1, context={"request": request})
            return Response(serializer.data)

        borrow1 = self.get_queryset()
        serializer = borrowserializer(
            borrow1, many=True, context={"request": request})
        # print(serializer.data)
        return Response(serializer.data)

    def post(self, request):
        serializer = borrowserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class BookCatagoryList(ListAPIView):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategoryserializer

    def get_queryset(self):
        book1 = BookCategory.objects.all()
        return book1

    def get(self, request, id=None):
        if id:
            book1 = BookCategory.objects.get(id=id)
            serializer = BookCategoryserializer(
                book1, context={"request": request})
            return Response(serializer.data)

        book1 = self.get_queryset()
        serializer = BookCategoryserializer(
            book1, many=True, context={"request": request})
        # print(serializer.data)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookCategoryserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def put(self, request,id=None):
        if id:
            book1 = BookCategory.objects.get(id=id)
            serializer = BookCategoryserializer(book1, data=request.data)
            data = {}
            if serializer.is_valid(raise_exception=True):
                serializer.save();
                data["status"] = "sucuess"
                return Response(data)
            else:  
                data['status'] = "error"
                return Response(data)

    def delete(self, request,id=None):
        if id:
            book1 = BookCategory.objects.get(id=id)
            serializer = book1.delete()
            data = {}
            if book1:
                data["status"] = "sucuess"
                return Response(data)
            else:  
                data['status'] = "error"
                return Response(data)



class commentList(ListAPIView):
    queryset = comment.objects.all()
    serializer_class = Commentserializer

    def get_queryset(self):
        comment1 = comment.objects.all()
        return comment1

    def get(self, request, id=None):
        if id:
            comment1 = comment.objects.get(id=id)
            serializer = Commentserializer(
            comment1, context={"request": request})
            return Response(serializer.data)

        comment1 = self.get_queryset()
        serializer = Commentserializer(
            comment1, many=True, context={"request": request})
        # print(serializer.data)
        return Response(serializer.data)

    def post(self, request):
        serializer = Commentserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request,id=None):
        if id:
            comment1 =comment.objects.get(id=id)
            serializer = Commentserializer(comment1, data=request.data)
            data = {}
            if serializer.is_valid(raise_exception=True):
                serializer.save();
                data["status"] = "sucuess"
                return Response(data)
            else:  
                data['status'] = "error"
                return Response(data)

    def delete(self, request,id=None):
        if id:
            comment1 =comment.objects.get(id=id)
            serializer = comment1.delete()
            data = {}
            if comment1:
                data["status"] = "sucuess"
                return Response(data)
            else:  
                data['status'] = "error"
                return Response(data)
