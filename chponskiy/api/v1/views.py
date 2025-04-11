from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from pydantic import BaseModel
from collections.abc import Sequence
from secrets import randbelow
from random import sample, choice

from chponskiy.models import GlossaryItem

class Question(BaseModel):
    question_text: str
    choices: list[str]
    correct_idx: int

    @classmethod
    def from_glossary_items(cls, glossary_items: Sequence[GlossaryItem], column_question: str, column_choices: str) -> 'Question':
        correct_idx = randbelow(len(glossary_items))
        choices: list[str] = [getattr(glossary_item, column_choices) for glossary_item in glossary_items]
        question_text = getattr(glossary_items[correct_idx], column_question)
        return Question(
            question_text=question_text,
            choices=choices,
            correct_idx=correct_idx,
        )

def game(request, slug):
    slug = slug.lower()
    match slug:
        case 'practice' | 'easy' | 'medium' | 'nightmare':
            return render(request, 'game.html', {'difficulty': slug})
        case _:
            response = HttpResponse()
            response.status_code = 404
            return response


def question(request, slug):
    slug = slug.lower()
    match slug:
        case 'practice':
            items = GlossaryItem.get_randoms(4)
            column_question, column_choices = choice((
                ('phrase_english', 'phrase_japanese'),
                ('phrase_english', 'phrase_chinese'),
            ))
        case 'easy':
            items = GlossaryItem.get_randoms(4)
            column_question, column_choices = choice((
                ('phrase_english', 'phrase_japanese'),
                ('phrase_english', 'phrase_chinese'),
                ('phrase_japanese', 'phrase_english'),
                ('phrase_chinese', 'phrase_english'),
            ))
        case 'medium':
            items = GlossaryItem.get_randoms(6)
            column_question, column_choices = choice((
                ('phrase_english', 'phrase_japanese'),
                ('phrase_english', 'phrase_chinese'),
                ('phrase_english', 'phrase_kana'),
                ('phrase_english', 'phrase_pinyin'),
                ('phrase_japanese', 'phrase_english'),
                ('phrase_chinese', 'phrase_english'),
                ('phrase_kana', 'phrase_english'),
                ('phrase_pinyin', 'phrase_english'),
            ))
        case 'nightmare':
            items = GlossaryItem.get_randoms(8)
            column_question, column_choices = sample(
                ('phrase_english', 'phrase_japanese', 'phrase_kana', 'phrase_chinese', 'phrase_pinyin'), 2)
        case _:
            response = HttpResponse()
            response.status_code = 404
            return response

    question_model = Question.from_glossary_items(items, column_question, column_choices)
    return JsonResponse(question_model.model_dump())
