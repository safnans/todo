from multiprocessing import context
from django.shortcuts import render
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from api import serializers
from api.models import Todos
from api.serializers import Todoserializer,Registrationserializer
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import permissions
# Create your views here.
class Todoview(ViewSet):
    def list(self,request,*args,**Kw):
        qs=Todos.objects.all()
        serializer=Todoserializer(qs,many=True)
        return Response(data=serializer.data)
    def create(self,request,*args,**kw):
        serializer=Todoserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    def retrieve(self,request,*args,**kw):
        id=kw.get("pk")
        qs=Todos.objects.get(id=id)
        serializer=Todoserializer(qs,many=False)
        return Response(data=serializer.data)
    def destroy(self,request,*args,**kw):
        id=kw.get("pk")
        Todos.objects.get(id=id).delete()
        return Response(data="deleted")
    def update(self,request,*args,**kw):
        id=kw.get("pk")
        obj=Todos.objects.get(id=id)
        serializer=Todoserializer(data=request.data,instance=obj)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class TodoModelview(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=Todoserializer
    queryset=Todos.objects.all()
    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)
    def create(self,request,*args,**kw):
        serializer=Todoserializer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    # def list(self,request,*args,**kw):
    #     qs=Todos.objects.filter(user=request.data)
    #     serializer=Todoserializer(qs,many=True)
    #     return Response(data=serializer.data)
    # def create(self,request,*args,**kw):
    #     serializer=Todoserializer(data=request.data)
    #     if serializer.is_valid():
    #         Todos.objects.create(**serializer.validated_data,user=request.user)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)

#localhost:8000/api/v1/todos/pending_todos/
#get
    @action(methods=["GET"],detail=False)
    def pending_todos(self,request,*args,**kw):
        qs=Todos.objects.filter(status=False)
        serializer=Todoserializer(qs,many=True)
        return Response(data=serializer.data)
#localhost:8000/api/v1/todos/completed_todos/
#get
    @action(methods=["GET"],detail=False)
    def complete_tudos(self,request,*args,**kw):
        qs=Todos.objects.filter(status=True)
        serializer=Todoserializer(qs,many=True)
        return Response(data=serializer.data)
#localhost:8000/api/v1/todos/mark_as_todos/
#post
    @action(methods=["post"],detail=True)
    def mark_as_done(self,request,*args,**kw):
        id=kw.get("pk")
        #Todos.objects.filter(id=id).update(status=True)
        obj=Todos.objects.get(id=id)
        obj.status=True
        obj.save()
        serializer=Todoserializer(obj,many=False)
        return Response(data=serializer.data)

class Usersview(ModelViewSet):
    serializer_class=Registrationserializer
    queryset=User.objects.all()
    # def create(self,request,*arg,**kw):
    #     serializer=Registrationserializer(data=request.data)
    #     if serializer.is_valid():
    #         usr=User.objects.create_user(**serializer._validated_data)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)

