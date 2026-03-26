import { useCallback, useState } from "react";
import ImageUpload from "../components/ImageUpload";
import ChatInterface from "../components/ChatInterface";
import "./Home.css";

type Phase = "upload" | "analyzing" | "ready";

export default function Home() {
  const [phase, setPhase] = useState<Phase>("upload");
  const [bloodTestId, setBloodTestId] = useState<number | null>(null);
  const [analysisError, setAnalysisError] = useState<string | null>(null);

  const processBloodTest = useCallback(async (id: number) => {
    setBloodTestId(id);
    setPhase("analyzing");
    setAnalysisError(null);

    try {
      const ocrRes = await fetch(`/api/blood-tests/${id}/ocr`, {
        method: "POST",
      });
      if (!ocrRes.ok) {
        const data = await ocrRes.json();
        throw new Error(data.detail || "OCR failed.");
      }

      const analyzeRes = await fetch(`/api/blood-tests/${id}/analyze`, {
        method: "POST",
      });
      if (!analyzeRes.ok) {
        const data = await analyzeRes.json();
        throw new Error(data.detail || "Analysis failed.");
      }

      setPhase("ready");
    } catch (err) {
      setAnalysisError(
        err instanceof Error ? err.message : "Processing failed."
      );
      setPhase("ready");
    }
  }, []);

  const handleUploadComplete = useCallback(
    (id: number) => {
      void processBloodTest(id);
    },
    [processBloodTest]
  );

  const handleReset = () => {
    setPhase("upload");
    setBloodTestId(null);
    setAnalysisError(null);
  };

  return (
    <div className="home">
      <div className={`upload-section ${phase !== "upload" ? "minimized" : ""}`}>
        {phase === "upload" ? (
          <>
            <h2>Upload a blood test</h2>
            <p>Upload an image of your blood test results to get started.</p>
          </>
        ) : (
          <div className="upload-header-row">
            <span className="upload-done-label">Blood test uploaded</span>
            <button className="new-upload-button" onClick={handleReset}>
              New upload
            </button>
          </div>
        )}
        <ImageUpload onUploadComplete={handleUploadComplete} />
      </div>

      {phase === "analyzing" && (
        <div className="analyzing">
          <div className="spinner" />
          <p>Analyzing your blood test results...</p>
        </div>
      )}

      {analysisError && (
        <div className="analysis-error">{analysisError}</div>
      )}

      <div className="chat-section">
        <ChatInterface
          bloodTestId={bloodTestId ?? 0}
          disabled={phase !== "ready"}
        />
      </div>
    </div>
  );
}
