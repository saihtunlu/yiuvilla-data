from .models import File
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from .serializers import FileSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class Files(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        all_medias = File.objects.all()
        media_serializer = FileSerializers(all_medias, many=True)
        return Response(media_serializer.data, status=status.HTTP_200_OK)


class SingleFile(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request, *args, **kwargs):
        length = request.data['length']
        data = request.data
        list = []
        for number in range(int(length)):
            array = {"image": None}
            array['image'] = data['image'+str(number)]
            image_serializer = FileSerializers(data=array)
            if image_serializer.is_valid():
                image_serializer.save()
                list.append(image_serializer.data)
            else:
                return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(list, status=status.HTTP_201_CREATED)


class RemoveFiles(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data['data']
        File.objects.filter(pk__in=data).delete()
        return Response('Success', status=status.HTTP_201_CREATED)
