from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import wordnet
import random

# Download required nltk data
nltk.download('punkt')
nltk.download('wordnet')

def extract_mcqs(text):
    """
    A simple function to extract MCQs from the given text.
    This is a basic implementation that selects sentences and replaces a word with a blank.
    """
    sentences = sent_tokenize(text)
    mcqs = []
    for sentence in sentences:
        words = sentence.split()
        if len(words) > 5:
            # Select a random word to replace with a blank
            word_to_replace = random.choice(words)
            # Generate options including the correct word and some synonyms or random words
            options = [word_to_replace]
            synonyms = set()
            for syn in wordnet.synsets(word_to_replace):
                for lemma in syn.lemmas():
                    synonym = lemma.name().replace('_', ' ')
                    if synonym.lower() != word_to_replace.lower():
                        synonyms.add(synonym)
            options.extend(list(synonyms)[:3])
            # Fill options to 4 if less than 4
            while len(options) < 4:
                options.append(random.choice(words))
            random.shuffle(options)
            question = sentence.replace(word_to_replace, "_____")
            mcqs.append({
                'question': question,
                'options': options,
                'answer': word_to_replace
            })
    return mcqs

@csrf_exempt
def upload_content(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        mcqs = extract_mcqs(content)
        return render(request, 'quiz/quiz.html', {'mcqs': mcqs})
    return render(request, 'quiz/upload.html')
