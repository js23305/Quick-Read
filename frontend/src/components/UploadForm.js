import React, {useState} from 'react';

function UploadForm() {
    const [summary, setSummary] = useState('');
    const [audioUrl, setAudioUrl] = useState('');
    const [showResult, setShowResult] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        
        try {
            const response = await fetch("http://localhost:8000/book_summarizer/process-book/", {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            setSummary(data.summary);
            setAudioUrl(data.audio_file_url); // Save audio file URL from backend
            setShowResult(true);
        } catch (error) {
            alert(error.message);
        }
    };

    const handleAudioDownload = () => {
        if (audioUrl) {
            const a = document.createElement('a');
            a.href = audioUrl;
            a.download = 'summary.mp3';
            document.body.appendChild(a);
            a.click();
            a.remove();
            alert('Audio file has been downloaded!');
        } else {
            alert('Audio file is not ready yet.');
        }
    };

return (

        <div className="container my-5">
            <h1 className="display-5 fw-bold text-center mb-4" style={{color: '#3730a3'}}>QuickRead Book Summarizer</h1>
            <form onSubmit={handleSubmit} encType="multipart/form-data" className="p-4 rounded shadow-sm bg-white border">
                <div className="mb-3">
                    <label htmlFor="book_file" className="form-label">Upload Book Cover/Page:</label>
                    <input type="file" className="form-control" id="book_file" name="book_file" accept="image/*" required />
                </div>
                <div className="mb-3">
                    <label htmlFor="description" className="form-label">Description of Book (Required):</label>
                    <textarea className="form-control" id="description" name="description" rows="3" required></textarea>
                </div>
                <div className="d-grid gap-2">
                    <button type="submit" className="btn btn-primary btn-lg">Summarize</button>
                </div>
            </form>
            {showResult && (
                <div id="result" className="mt-5 p-4 rounded shadow-sm bg-light border">
                    <h3 className="fw-bold mb-3" style={{color: '#3730a3'}}>Summary:</h3>
                    {summary.split(/\n\s*\n/).map((para, idx) => (
                        <p key={idx} className="mb-3" style={{fontSize: '1.1rem', color: '#22223b', textAlign: 'justify'}}>{para}</p>
                    ))}
                    <h3 className="fw-bold mt-4 mb-3" style={{color: '#3730a3'}}>Audio File:</h3>
                    <div className="d-grid gap-2">
                        <button 
                          onClick={handleAudioDownload}
                          className="btn btn-secondary btn-lg"
                        >
                          Download Audio
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default UploadForm;