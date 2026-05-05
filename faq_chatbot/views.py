from django.shortcuts import render
from django.http import JsonResponse
from .ml_model import FAQBot

bot = FAQBot()

def chatbot_page(request):
    return render(request, 'faq_chatbot/chatbot.html')

def get_response(request):
    if request.method == "POST":
        user_message = request.POST.get("message")
        response = bot.get_response(user_message)
        return JsonResponse({"response": response})