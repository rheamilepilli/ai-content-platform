import { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [contentType, setContentType] = useState("Instagram");
  const [style, setStyle] = useState("Funny");
  const [customPrompt, setCustomPrompt] = useState("");
  const [generatedContent, setGeneratedContent] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!file) {
      alert("Please select a video file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("content_type", contentType);
    formData.append("style", style);
    formData.append("custom_prompt", customPrompt);

    try {
      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData
      );

      if (response.data.error) {
        setGeneratedContent(response.data.error);
      } else {
        setGeneratedContent(response.data.generated_content);
      }
    } catch (error) {
      console.error("FULL ERROR:", error);

      if (error.response) {
        alert("Backend Error: " + error.response.status);
      } else if (error.request) {
        alert("No response received from backend.");
      } else {
        alert(error.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        maxWidth: "800px",
        margin: "50px auto",
        padding: "20px",
        textAlign: "center",
      }}
    >
      <h1>🚀 AI Content Platform</h1>

      <div style={{ marginTop: "20px" }}>
        <label>Upload Video</label>
        <br />
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
        />
      </div>

      <div style={{ marginTop: "20px" }}>
        <label>Content Type</label>
        <br />
        <select
          value={contentType}
          onChange={(e) => setContentType(e.target.value)}
        >
          <option>Instagram</option>
          <option>LinkedIn</option>
          <option>Twitter</option>
          <option>YouTube</option>
          <option>All</option>
        </select>
      </div>

      <div style={{ marginTop: "20px" }}>
        <label>Style</label>
        <br />
        <select
          value={style}
          onChange={(e) => setStyle(e.target.value)}
        >
          <option>Funny</option>
          <option>Professional</option>
          <option>Motivational</option>
          <option>Gen Z</option>
        </select>
      </div>

      <div style={{ marginTop: "20px" }}>
        <label>Custom Prompt</label>
        <br />
        <textarea
          rows="4"
          cols="50"
          value={customPrompt}
          onChange={(e) => setCustomPrompt(e.target.value)}
          placeholder="Target college students..."
        />
      </div>

      <div style={{ marginTop: "20px" }}>
        <button onClick={handleSubmit}>
          {loading ? "Generating..." : "Generate Content"}
        </button>
      </div>

      <div style={{ marginTop: "40px" }}>
        <h2>Generated Content</h2>

        <pre
          style={{
            whiteSpace: "pre-wrap",
            textAlign: "left",
            border: "1px solid #ccc",
            borderRadius: "10px",
            padding: "15px",
            minHeight: "100px",
          }}
        >
          {generatedContent}
        </pre>
      </div>
    </div>
  );
}

export default App;