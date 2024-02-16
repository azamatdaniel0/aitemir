from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json
from openai import OpenAI
from decouple import config
import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from datetime import datetime
from .models import Media, RequestMedia
from django.core.files.base import ContentFile


url = "http://tts.ulut.kg/api/tts"
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer hyrtgvxvuTKC75c5JuxXMr1qH1MBlesYZgAGhJz09x2ro1GTTeEB2yJXPdFL5yDd'
}
# Assuming you have already loaded or defined your processor and model
processor = Wav2Vec2Processor.from_pretrained("anton-l/wav2vec2-large-xlsr-53-kyrgyz")
model = Wav2Vec2ForCTC.from_pretrained("anton-l/wav2vec2-large-xlsr-53-kyrgyz")
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
        audio = self.request.FILES.get("audio")
        
        if audio is None: 
             return Response('Повторите попытку еще раз')
        media2 = RequestMedia(audios = audio)
        media2.save()
        audio = media2.audios


        def process_audio_file(audio):
            resampler = torchaudio.transforms.Resample(orig_freq=48_000, new_freq=16_000)
            speech_array, sampling_rate = torchaudio.load(audio)
            speech = resampler(speech_array).squeeze().numpy()
            return speech, sampling_rate

        def predict_text_from_audio(audio):
            speech, sampling_rate = process_audio_file(audio)
            inputs = processor(speech, sampling_rate=16_000, return_tensors="pt", padding=True)
            
            with torch.no_grad():
                logits = model(inputs.input_values, attention_mask=inputs.attention_mask).logits
            
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = processor.batch_decode(predicted_ids)
            print(transcription)
            return transcription

        transcription = predict_text_from_audio(audio)
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
            content=transcription[0],
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
                        ass = message.content[0].text.value
                        # The payload and headers remain the same
                        payload = {
                        "text": ass, 
                        "speaker_id": "1"
                        }
                        # Make the POST request using the requests library
                        response = requests.post(url, data=json.dumps(payload), headers=headers)
                        audio_content = ContentFile(response.content)
                        audio_model_instance = Media()
                        time_ident = datetime.now()
                        time_ident = str(time_ident)
                        audio_model_instance.audios.save(f'{time_ident}_output.wav', audio_content)
                        audio_model_instance.save()
                        client.beta.assistants.delete(assistant.id)
                        return Response(data={"audio": audio_model_instance.audios.url, "text": ass, 'question': transcription[0]})
                    
                    else:
                        return Response(data={"message": "something went wrong"})