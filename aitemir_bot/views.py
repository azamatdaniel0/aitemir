from rest_framework.views import APIView
from rest_framework.response import Response
import os
from openai import OpenAI 
from .models import Instructions
class GetAnswerAPIView(APIView):
    def post(self, request, *args, **kwargs):
        transcription = request.data.get('text')

        if transcription is None:
            return Response({'error': 'Повторите попытку еще раз'}, status=400)

        MODEL="gpt-4o"
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "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"))
        latest_instruction = Instructions.objects.first()
        if not latest_instruction:
            return Response({'error': 'Инструкция не найдена. Пожалуйста, добавьте инструкцию.'}, status=500)
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": latest_instruction.instruction},
                {"role": "user", "content": transcription}
            ]
        )
        answer = completion.choices[0].message.content
        total_tokens = str(completion.usage.total_tokens)
        completion_tokens = str(completion.usage.completion_tokens)
        prompt_tokens = str(completion.usage.prompt_tokens)
        return Response(data={"answer": answer, "prompt_tokens":prompt_tokens, "completion_tokens": completion_tokens, "total_tokens": total_tokens})