from .models import Imports, ImportProduct
from .serializers import ImportProductSerializers, ImportsSerializers
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.template.loader import render_to_string
from django.http import HttpResponse


class SalePrint(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        new_import = Imports()
        import_serializer = ImportsSerializers(new_import, data=data)
        if import_serializer.is_valid():
            import_serializer.save()
            if data['products']:
                for import_product in data['products']:
                    import_product_model = ImportProduct(imports=new_import)
                    import_product_serializer = ImportProductSerializers(
                        import_product_model, data=import_product)
                    if import_product_serializer.is_valid():
                        import_product_serializer.save()
                    else:
                        new_import.delete()
                        return Response(import_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            template_path = 'pdf/order/default.html'
            html = render_to_string(
                template_path, {'order': import_serializer.data})
            response = HttpResponse(html, content_type='application/html')
            filename = 'order.html'
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(
                filename)
            return response
        else:
            return Response(import_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
