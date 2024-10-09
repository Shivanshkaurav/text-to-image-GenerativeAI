from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Summary 
from .serializers import *
from django.conf import settings
from rest_framework import status
import google.generativeai as genai
from PyPDF2 import PdfReader
from django.core.files.storage import default_storage
from django.conf import settings
from PIL import Image
import io
import requests
from django.core.files.base import ContentFile

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": "Bearer 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"}

model = genai.GenerativeModel('gemini-1.5-flash')
       
class SummaryView(APIView):
    def post(self, request):
        
        reader = PdfReader(request.FILES.get('file'))  
        data = ""
        for i in range(len(reader.pages)):
            data = data + reader.pages[i].extract_text()        
        
        if data:
            prompt = "Please provide Title and summary of 500 words for the following content without \n." + data
            response = model.generate_content(prompt)
            a = response.text
            str_ing = " ".join(a.split())
            
            data = str_ing.split("## Summary: ")
            t = data[0]
            s = data[1]
            temp = t.split("## Title: ")
            title = " ".join(temp[1].split())
            summary = " ".join(s.split())
            
            def query(payload):
                response = requests.post(API_URL, headers=headers, json=payload)
                return response.content
            
            image_bytes = query({
            "inputs": title,
            })
            image = Image.open(io.BytesIO(image_bytes))
            image_format = image.format.lower()
            image_name = f"{title}.{image_format}"
            image_path = default_storage.save(f'summaries/{image_name}', ContentFile(image_bytes))
            
            Summary.objects.create(title=title, summary=summary, image=image_path)
            data = Summary.objects.all()
            serializer = SummarySerializer(data, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        
        return Response({"Error":"Some Error"}, status=status.HTTP_400_BAD_REQUEST)

class SummaryList(APIView):
    def get(self, request):
        summaries = Summary.objects.all()
        if summaries:
            serializer = SummarySerializer(summaries, many=True)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"No Content":"No Data is Present"}, status=status.HTTP_204_NO_CONTENT)