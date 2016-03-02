import datetime
import subprocess
import tempfile

from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.core.files.storage import get_storage_class
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from cedict.models import Term, Translation
from texts.models import Phrase, Text

from . import serializers
from . import permissions

_storage = get_storage_class()()


class _BaseModelViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        queryset = super(_BaseModelViewSet, self).get_queryset()
        order = self.request.query_params.get('order')
        if order:
            queryset = queryset.order_by(order)
        return queryset


class TermViewSet(_BaseModelViewSet):
    queryset = Term.objects.all()
    serializer_class = serializers.TermSerializer
    permission_classes = (permissions.ReadOnly,)

    def get_queryset(self):
        queryset = super(TermViewSet, self).get_queryset()
        traditional = self.request.query_params.get('traditional')
        search_query = self.request.query_params.get('q')
        starred = self.request.query_params.get('starred', 'false') != 'false'
        language = self.request.query_params.get('lang', 'zh-tw')
        if language == 'zh':
            language = 'zh-tw'
        if starred:
            queryset = self.request.user.profile.starred_terms.all()
        if search_query is not None:
            if language == 'zh-tw':
                queryset = (queryset.filter(traditional__contains=search_query)
                            .extra(select={'__len': 'Length(traditional)'})
                            .order_by('__len'))
            elif language == 'zh-cn':
                queryset = (queryset.filter(simplified__contains=search_query)
                            .extra(select={'__len': 'Length(simplified)'})
                            .order_by('__len'))
            elif language == 'en':
                queryset = (
                    queryset.filter(
                        translation__translation__icontains=search_query)
                    .extra(
                        select={'__len': 'Length(translation)'})
                    .order_by('__len'))
            else:
                queryset = queryset.exclude(pk__gt=0) # exclude all
        if traditional is not None:
            queryset = queryset.filter(traditional=traditional)
        return queryset

    @list_route(url_path='random', methods=['get'])
    def random(self, request):
        term = Term.objects.order_by('?').first()
        term = serializers.TermSerializer(term)
        return Response(term.data)

    @detail_route(url_path='star', methods=['post', 'delete'],
                  permission_classes=[IsAuthenticatedOrReadOnly])
    def star(self, request, pk=None):
        term = get_object_or_404(Term, pk=pk)
        print request.method
        if request.method == 'POST':
            request.user.profile.starred_terms.add(term)
        elif request.method == 'DELETE':
            request.user.profile.starred_terms.remove(term)
        return Response({'status', 'ok'})


class TranslationViewSet(_BaseModelViewSet):
    queryset = Translation.objects.all()
    serializer_class = serializers.TranslationSerializer
    permission_classes = (permissions.IsOwnerOrReadOnly,)


class TextViewSet(_BaseModelViewSet):
    queryset = Text.objects.all()
    serializer_class = serializers.TextSerializer
    permission_classes = (permissions.IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class PhraseViewSet(_BaseModelViewSet):
    queryset = Phrase.objects.all()
    serializer_class = serializers.PhraseSerializer
    permission_classes = (permissions.IsOwnerOrReadOnly,)
    lookup_field = 'phrase'

    def get_queryset(self):
        queryset = super(PhraseViewSet, self).get_queryset()
        due = self.request.query_params.get('due', False)
        random = self.request.query_params.get('random', False)
        if due:
            now = datetime.datetime.now()
            queryset = queryset.filter(owner=self.request.user).filter(
                Q(level=1)
                |Q(level=2, updated__lt=now-datetime.timedelta(days=1))
                |Q(level=3, updated__lt=now-datetime.timedelta(days=3))
                |Q(level=4, updated__lt=now-datetime.timedelta(days=7)))
        if random:
            queryset = queryset.order_by('?')
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(_BaseModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsOwnerOrReadOnly,)


def audio_view(request, term):
    term = term.lower()
    term = term.replace('u:', 'v')
    term = ' '.join('er' if comp == 'r' else comp for comp in term.split())
    filename = 'audio_files/%s.mp4' % term
    if not _storage.exists(filename):
        with tempfile.NamedTemporaryFile(suffix='.mp4') as audio_file:
            subprocess.call(('say', '--file-format=mp4f', '-o',
                             audio_file.name, '-v', 'Mei-Jia', term))
            with _storage.open(filename, 'wb') as dest:
                dest.write(audio_file.read())
    return HttpResponseRedirect(_storage.url(filename))
