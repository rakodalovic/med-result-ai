import { useCallback, useState } from "react";
import ImageUpload from "../components/ImageUpload";
import ImagePreview from "../components/ImagePreview";
import ChatInterface from "../components/ChatInterface";
import "./Home.css";

type Phase = "upload" | "analyzing" | "ready";

export default function Home() {
  const [phase, setPhase] = useState<Phase>("upload");
  const [bloodTestId, setBloodTestId] = useState<number | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
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
    (id: number, objectUrl: string) => {
      setPreviewUrl(objectUrl);
      void processBloodTest(id);
    },
    [processBloodTest]
  );

  const handleReset = () => {
    setPhase("upload");
    setBloodTestId(null);
    setPreviewUrl(null);
    setAnalysisError(null);
  };

  return (
    <div className="home">
      {phase === "upload" && (
        <div className="upload-hero">
          <div className="upload-hero-content">
            <h2>Analyze your blood test</h2>
            <p>
              Upload an image of your blood test results and chat with AI
              to understand what they mean.
            </p>
            <ImageUpload onUploadComplete={handleUploadComplete} />
          </div>
        </div>
      )}

      {phase === "analyzing" && (
        <div className="analyzing-overlay">
          {previewUrl && (
            <div className="analyzing-thumbnail">
              <img src={previewUrl} alt="Uploaded blood test" />
            </div>
          )}
          <div className="analyzing-card">
            <div className="analyzing-spinner" />
            <p className="analyzing-title">Analyzing your results</p>
            <p className="analyzing-hint">
              Running OCR and AI analysis. This may take a few seconds...
            </p>
          </div>
        </div>
      )}

      {phase === "ready" && (
        <div className="chat-active">
          <div className="chat-topbar">
            <button className="topbar-button" onClick={handleReset}>
              &#43; New analysis
            </button>
            {previewUrl && <ImagePreview src={previewUrl} />}
          </div>
          {analysisError && (
            <div className="analysis-error">{analysisError}</div>
          )}
          <ChatInterface
            bloodTestId={bloodTestId ?? 0}
            disabled={false}
          />
        </div>
      )}

      {phase !== "ready" && (
        <div className="chat-preview">
          <ChatInterface bloodTestId={0} disabled={true} />
        </div>
      )}
    </div>
  );
}
