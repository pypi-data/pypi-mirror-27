from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, permissions, status, views
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from apollo.models import Form, FormFieldTemplate, FormField, FormSubmission, Layout
from .serializers import *
from .permissions import FormSubmissionsPermission
import pdb


class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    @detail_route(['POST'])
    def clone(self, request, pk=None):
        form = self.get_object()
        clone = form.clone()

        return Response(FormSerializer(clone).data, status=status.HTTP_201_CREATED)


class FormFieldTemplateViewSet(viewsets.ModelViewSet):
    queryset = FormFieldTemplate.objects.all()
    serializer_class = FormFieldTemplateSerializer
    permission_classes = (permissions.DjangoModelPermissions,)


class FormFieldViewSet(viewsets.ModelViewSet):
    queryset = FormField.objects.all()
    serializer_class = FormFieldSerializer
    permission_classes = (permissions.DjangoModelPermissions,)


class FormSubmissionViewSet(viewsets.ModelViewSet):
    queryset = FormSubmission.objects.all()
    serializer_class = FormSubmissionSerializer
    permission_classes = (FormSubmissionsPermission,)

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('form_id',)

    def create(self, request, *args, **kwargs):
        try:
            return super(FormSubmissionViewSet, self).create(request, *args, **kwargs)
        except ValidationError as exc:
            return Response({'error': exc.message}, status=status.HTTP_400_BAD_REQUEST)


class LayoutViewSet(viewsets.ModelViewSet):
    queryset = Layout.objects.all()
    serializer_class = LayoutSerializer
    permission_classes = (permissions.DjangoModelPermissions,)


class FormFieldOptionsAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        serializer = FieldOptionsSerializer({
            'widget_types': [_[0] for _ in FormFieldTemplate.FIELD_TYPES],
            'validation_rules': [_[0] for _ in FormFieldTemplate.VALIDATION_RULES],
            'label_positions': [_[0] for _ in FormFieldTemplate.LABEL_POSITIONS]
        })

        return Response(serializer.data)


