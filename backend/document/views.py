import math
import re
from collections import Counter

from django.shortcuts import render, redirect
from django.views import View

from .forms import DocumentForm
from .models import Document, WordStat


class UploadDocumentView(View):
    template_name = 'upload.html'

    def get(self, request):
        form = DocumentForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            self.process_document(document)
            return redirect('results', doc_id=document.id)
        return render(request, self.template_name, {'form': form})

    def process_document(self, document):
        # Чтение файла
        text = document.file.read().decode('utf-8').lower()

        # Токенизация и очистка слов
        words = re.findall(r'\b\w+\b', text)

        # Подсчет частоты слов
        word_counts = Counter(words)
        total_words = len(words)

        # Расчет TF (Term Frequency)
        word_stats = []
        for word, count in word_counts.most_common(50):
            tf = count / total_words
            word_stat = WordStat(document=document, word=word, tf=tf)
            word_stats.append(word_stat)

        # Массовое создание записей для эффективности
        WordStat.objects.bulk_create(word_stats)

        # Расчет IDF (Inverse Document Frequency)
        self.calculate_idf(document)

        document.processed = True
        document.save()

    @staticmethod
    def calculate_idf(document):
        all_docs_count = Document.objects.count()
        for word_stat in document.word_stats.all():
            # Количество документов, содержащих это слово
            docs_with_word = WordStat.objects.filter(
                word=word_stat.word
            ).values('document').distinct().count()
            word_stat.idf = math.log(
                (all_docs_count + 1) / (docs_with_word + 1)
                ) + 1  # smoothing
            word_stat.save()


class ResultsView(View):
    template_name = 'results.html'

    def get(self, request, doc_id):
        document = Document.objects.get(id=doc_id)
        word_stats = document.word_stats.all().order_by("-idf")[:50]

        context = {
            'document': document,
            'word_stats': word_stats,
        }
        return render(request, self.template_name, context)
