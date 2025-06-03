# QuickRead Book Summarizer

QuickRead Book Summarizer is a web application that allows users to upload a book cover or page image and a description of the book. The app uses OCR (Optical Character Recognition) to extract text from the image, then leverages OpenAI's GPT to generate a detailed summary of the book in 4-5 paragraphs. Additionally, the app provides an instant audio download of the summary using text-to-speech (gTTS), making it accessible for users who prefer listening.

## Features
- Upload a book cover or page image (supports most image formats)
- Enter a description of the book
- Automatic OCR to extract text from the image
- AI-powered detailed summary generation (OpenAI GPT-3.5 Turbo)
- Instant audio download of the summary (MP3)
- Modern, responsive UI (works on desktop and mobile)

## How it Works
1. **Upload**: User uploads an image and provides a description.
2. **OCR & Summarization**: The backend extracts text from the image and combines it with the description. OpenAI generates a detailed summary.
3. **Audio Generation**: The summary is converted to speech and saved as an MP3 file.
4. **Download**: User can instantly download the audio summary.

## Tech Stack
- **Frontend**: React, Bootstrap
- **Backend**: Django, Django REST, OpenAI API, pytesseract, gTTS
- **OCR**: Tesseract
- **AI**: OpenAI GPT-3.5 Turbo
- **Audio**: gTTS (Google Text-to-Speech)

## How to Run
1. Clone the repository.
2. Install backend and frontend dependencies.
3. Start the Django backend server.
4. Start the React frontend server.
5. Visit `http://localhost:3000` in your browser.

## Is this app unique?
While there are other book summarizer tools and OCR-based apps, QuickRead Book Summarizer is unique in that it:
- Combines OCR, AI summarization, and instant audio download in a single, seamless workflow.
- Allows users to upload any book image and get a detailed, multi-paragraph summary powered by OpenAI.
- Instantly provides an audio version of the summary, making it accessible for visually impaired users or those who prefer listening.
- Has a modern, mobile-friendly UI for a smooth user experience.

## License
This project is for educational and demonstration purposes.
