import { useState } from 'react';
import UploadForm from './components/UploadForm';

function App() {
  const [resume, setResume] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [resumeId, setResumeId] = useState(null);
  const [score, setScore] = useState(null);
  const [matchedSkills, setMatchedSkills] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [suggestions, setSuggestions] = useState([]);

  const handleUpload = (data) => {
    console.log('Upload response:', data);
    setResume(data.resume);
    setJobDescription(data.job_description);
    setResumeId(data.resume_id);};

  const handleAnalyze = async () => {
  try {
    const res = await fetch('http://localhost:8000/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        resume_id: resumeId, // you'll need to track this in state
        jd_text: jobDescription,}),
    });


    const data = await res.json();
    console.log('Analysis response:',data);
    setAnalysis(data);
  } catch (err) {
    console.error('Failed to analyze:', err);
  };
 };

   const handleSuggest = async () => {
     const res = await fetch('http://localhost:8000/suggest', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ resume_id: resumeId, jd_text: jobDescription }),
      });
     const data = await res.json();
     setSuggestions(data.suggestions);
   };



  return (
    <div className="p-8 max-w-3xl mx-auto">
      <h1>Resume Coach</h1>
      <UploadForm onUpload={handleUpload} />

      <label className="block text-sm font-medium text-gray-700 mt-4">Resume:</label>
        <textarea
        className="w-full border border-gray-300 rounded p-2 mt-1"
        rows="8"
        value={resume}
        onChange={(e) => setResume(e.target.value)}
       />

    <label className="block text-sm font-medium text-gray-700 mt-4">Job Description:</label>
        <textarea
        className="w-full border border-gray-300 rounded p-2 mt-1"
        rows="8"
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
    />

      <button
        className="mt-4 bg-purple-600 text-white px-4 py-2 rounded"
        onClick={handleAnalyze}>
        Analyze My Resume
      </button>

      <button onClick={handleSuggest} className="bg-green-600 text-white px-4 py-2 rounded mt-4">
        Get Resume Suggestions
      </button>


     {resumeId && (
        <p className="text-gray-500 text-sm mt-2">Resume ID: {resumeId}</p>
     )}

     {analysis && (
        <div className="mt-6 space-y-2 border p-4 rounded shadow">
        <h2 className="text-xl font-bold">Analysis Results</h2>

        <p><strong>Score:</strong> {analysis.score}</p>

        <div>
         <p className="font-semibold">Matched Skills:</p>
        <ul className="list-disc list-inside text-green-700">
            {analysis.matched?.map((skill) => (
             <li key={skill}>{skill}</li>
            ))}
        </ul>
        </div>

    <div>
      <p className="font-semibold">Missing Skills:</p>
      <ul className="list-disc list-inside text-red-700">
        {analysis.missing?.map((skill) => (
          <li key={skill}>{skill}</li>
        ))}
      </ul>
    </div>

    {analysis.recommendations?.length > 0 && (
      <div>
        <p className="font-semibold">Recommendations:</p>
        <ul className="list-disc list-inside text-blue-700">
          {analysis.recommendations.map((tip, idx) => (
            <li key={idx}>{tip}</li>
          ))}
        </ul>
      </div>
    )}
    </div>
   )}

   {suggestions.length > 0 && (
  <div className="mt-6 space-y-2 border p-4 rounded shadow">
    <h2 className="text-xl font-bold">Suggestions to Improve Resume</h2>
    <ul className="list-disc list-inside text-blue-800">
      {suggestions.map((s) => (
        <li key={s.skill}>
          <strong>{s.skill}:</strong> {s.suggestion}
        </li>
      ))}
    </ul>
  </div>
)}

    </div>
  );

}

export default App;

