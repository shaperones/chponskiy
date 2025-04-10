from django.shortcuts import render
from django.http import HttpResponse

def game(request, slug):
    slug = slug.lower()
    match slug:
        case 'practice' | 'easy' | 'medium' | 'nightmare':
            return render(request, 'game.html', {'difficulty': slug})
        case _:
            response = HttpResponse()
            response.status_code = 404
            return response
