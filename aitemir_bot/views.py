from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json
from openai import OpenAI
from decouple import config
from datetime import datetime
from .models import Media, RequestMedia
from django.core.files.base import ContentFile

API_KEY = config("OPENAI_API_KEY")

class HelloAPIView(APIView):

    def get(self, request, *args, **kwargs):
        answer = audio = ''
        answer = "Салам, менин атым Айтемир. Сизге кандай жардам бере алам?"
        audio = 'greeting.wav'
        return Response({
            "text": answer,
            "audio": str(audio)})



class GetAnswerAPIView(APIView):
    def post(self, request):
        transcription = self.request.get("text")
        
        if transcription is None: 
             return Response('Повторите попытку еще раз')

        print("==============================================")
        print("==============================================")
        print(transcription)
        print("==============================================")
        print("==============================================")

        # Get the transcription from the binary audio data
        # gets API Key from environment variable OPENAI_API_KEY
        client = OpenAI(api_key=API_KEY)

        assistant = client.beta.assistants.create(
            name="Айтемир",
            instructions="Вы - Ассистент в  Центре обслуживания населения. Вас зовут Айтемир. Отвечай так, будто бы к тебе обратились за вопросом внутри ЦОН. Ты можешь смотреть ответы на вопросы в этом сайте. https://grs.gov.kg/ru/faq/. Разговаривай на кыргызском языке и отвечай максимально коротко",
            model="gpt-4-1106-preview",
        )

        thread = client.beta.threads.create()

        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=transcription,
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        while True:
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

            if run.status == "completed":
                messages = client.beta.threads.messages.list(thread_id=thread.id)
                for message in messages:
                    assert message.content[0].type == "text"
                    if message.role == "assistant":
                        answer = message.content[0].text.value
                        client.beta.assistants.delete(assistant.id)
                        return Response(data={"answer": answer})
                    
                    else:
                        return Response(data={"message": "something went wrong"})