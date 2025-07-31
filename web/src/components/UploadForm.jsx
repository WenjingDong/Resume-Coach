import { useState } from 'react';

function UploadForm({ onUpload }) {
  const [resumeFile, setResumeFile] = useState(null);
  const [jdFile, setJdFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!resumeFile || !jdFile) return;

    const formData = new FormData();
    formData.append('resume', resumeFile);
    formData.append('job_description', jdFile);

    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        throw new Error('Upload failed');
      }

      const data = await res.json();
      onUpload({
        resume: data.resume,
        job_description: data.job_description,
        resume_id: data.resume_id,
        });
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4 border p-4 rounded-lg shadow">
      <h2 className="text-xl font-semibold">Upload Resume and JD (PDF)</h2>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setResumeFile(e.target.files[0])}
      />
      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setJdFile(e.target.files[0])}
      />

      <button
        onClick={handleUpload}
        className="bg-blue-600 text-white px-4 py-2 rounded"
        disabled={loading}
      >
        {loading ? 'Uploading...' : 'Upload'}
      </button>
    </div>
  );
}

export default UploadForm;

