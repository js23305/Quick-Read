import os
import json
from openai import OpenAI
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import JsonResponse, FileResponse
import pytesseract
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Specify the Tesseract executable path explicitly
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from gtts import gTTS
from django.template import loader

# Load OpenAI API key from keys.json
KEYS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../keys.json'))
with open(KEYS_PATH, 'r') as f:
    keys = json.load(f)

OPENAI_API_KEY = keys.get('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

def preprocess_image(image_path):
    # Open the image
    img = Image.open(image_path)
    # Convert to grayscale
    img = ImageOps.grayscale(img)
    # Increase contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    # Apply a slight blur to reduce noise
    img = img.filter(ImageFilter.MedianFilter())
    # Optionally, binarize (threshold)
    img = img.point(lambda x: 0 if x < 128 else 255, '1')
    return img

def book_summarizer(request):
    if request.method == 'POST':
        book_file = request.FILES.get('book_file')
        description = request.POST.get('description', '')

        if not book_file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        fs = FileSystemStorage()
        filename = fs.save(book_file.name, book_file)
        file_path = fs.path(filename)

        # Debugging: Log the uploaded file and description
        print(f"Uploaded file: {book_file}")
        print(f"Description: {description}")
        print(f"Saved file path: {file_path}")


        # Debugging: Log the file path after saving
        print(f"Saved file path: {file_path}")

        # Debugging: Log OCR output with preprocessing
        try:
            preprocessed_img = preprocess_image(file_path)
            text = pytesseract.image_to_string(preprocessed_img)
            print(f"OCR output: {text}")
        except Exception as e:
            print(f"OCR failed: {e}")
            return JsonResponse({'error': f'OCR failed: {str(e)}'}, status=500)

        # Debugging: Log combined text before summarization
        combined_text = f"{description}\n{text}"
        print(f"Combined text for summarization: {combined_text}")

        # Handle short or meaningless input gracefully
        if len(combined_text) < 30:
            summary = "The uploaded image doesn't seem to contain enough text to summarize. Please try uploading a full page."
            audio_filename = filename.split('.')[0] + '.mp3'
            audio_path = fs.path(audio_filename)
            # Start audio generation in background
            import threading
            def generate_audio():
                tts = gTTS(summary)
                tts.save(audio_path)
            threading.Thread(target=generate_audio).start()
            return JsonResponse({
                'summary': summary,
                'audio_file_url': fs.url(audio_filename),
                'audio_pending': True
            })  
        
        # Request a detailed 4-5 paragraph summary
        prompt = f"""Write a detailed summary of the following book in 4 to 5 paragraphs. Be as comprehensive as possible, covering the main plot, characters, and key events: {combined_text}"""

        # Debugging: Log OpenAI API response
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You summarize scanned book text for general understanding."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            summary = response.choices[0].message.content
            print(f"OpenAI API response: {summary}")
        except Exception as e:
            print(f"AI Summarization failed: {e}")
            return JsonResponse({'error': f'AI Summarization failed: {str(e)}'}, status=500)

        # If OCR output is too short, try to get a detailed summary from OpenAI using the title and description
        if len(text.strip()) < 30:
            book_title = text.strip().replace('\n', ' ').replace('By ', '').strip()
            user_desc = description.strip()
            if book_title or user_desc:
                prompt = (
                    f"The user uploaded a book image and provided this description: '{user_desc}'. "
                    f"The OCR detected the book title as: '{book_title}'. "
                    "Please give a detailed summary of the first chapter of this book, and provide as many details as possible about the story, main characters, and setting. "
                    "If you know the book, include chapter-by-chapter details and any interesting facts. Provide me at least four to five paragraphs."
                )
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a book summarizer."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                    )
                    summary = response.choices[0].message.content
                except Exception as e:
                    summary = "The uploaded image and description did not provide enough information to generate a detailed summary. Please try uploading a full page or a more detailed description."
            else:
                summary = "The uploaded image and description did not provide enough information to generate a summary. Please try uploading a full page and a detailed description."
            audio_filename = filename.split('.')[0] + '.mp3'
            audio_path = fs.path(audio_filename)
            # Start audio generation in background
            import threading
            def generate_audio():
                tts = gTTS(summary)
                tts.save(audio_path)
            threading.Thread(target=generate_audio).start()
            return JsonResponse({
                'summary': summary,
                'audio_file_url': fs.url(audio_filename),
                'audio_pending': True
            })

        # Start audio generation in background for normal case
        audio_filename = filename.split('.')[0] + '.mp3'
        audio_path = fs.path(audio_filename)
        import threading
        def generate_audio():
            tts = gTTS(summary)
            tts.save(audio_path)
        threading.Thread(target=generate_audio).start()
        return JsonResponse({
            'summary': summary,
            'audio_file_url': fs.url(audio_filename),
            'audio_pending': True
        })

    return JsonResponse({'detail': 'Only POST allowed'}, status=405)

@csrf_exempt
@require_POST
def generate_audio(request):
    import tempfile
    from io import BytesIO
    summary = request.POST.get('summary', '')
    if not summary or len(summary.strip()) < 5:
        return JsonResponse({'error': 'No summary provided.'}, status=400)
    try:
        tts = gTTS(summary)
        audio_io = BytesIO()
        tts.write_to_fp(audio_io)
        audio_io.seek(0)
        response = FileResponse(audio_io, as_attachment=True, filename='summary.mp3', content_type='audio/mpeg')
        return response
    except Exception as e:
        return JsonResponse({'error': f'Audio generation failed: {str(e)}'}, status=500)