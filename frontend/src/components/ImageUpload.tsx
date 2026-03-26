import { useCallback, useRef, useState } from "react";
import type { DragEvent, ChangeEvent } from "react";
import "./ImageUpload.css";

type Status = "idle" | "uploading" | "success" | "error";

interface UploadResult {
  id: number;
}

interface ImageUploadProps {
  onUploadComplete: (id: number) => void;
}

const ALLOWED_TYPES = ["image/jpeg", "image/png"];
const MAX_SIZE = 10 * 1024 * 1024;

export default function ImageUpload({ onUploadComplete }: ImageUploadProps) {
  const [status, setStatus] = useState<Status>("idle");
  const [preview, setPreview] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const reset = () => {
    setStatus("idle");
    setPreview(null);
    setError(null);
  };

  const validate = (file: File): string | null => {
    if (!ALLOWED_TYPES.includes(file.type)) {
      return "Invalid file type. Only JPEG and PNG are allowed.";
    }
    if (file.size > MAX_SIZE) {
      return "File too large. Maximum size is 10 MB.";
    }
    return null;
  };

  const upload = useCallback(
    async (file: File) => {
      const validationError = validate(file);
      if (validationError) {
        setError(validationError);
        setStatus("error");
        return;
      }

      setPreview(URL.createObjectURL(file));
      setError(null);
      setStatus("uploading");

      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch("/api/upload", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.detail || "Upload failed.");
        }

        const result: UploadResult = await response.json();
        setStatus("success");
        onUploadComplete(result.id);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Upload failed.");
        setStatus("error");
      }
    },
    [onUploadComplete]
  );

  const handleFile = (file: File | undefined) => {
    if (file) {
      void upload(file);
    }
  };

  const handleDrop = (e: DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    handleFile(e.dataTransfer.files[0]);
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    handleFile(e.target.files?.[0]);
  };

  return (
    <div className="image-upload">
      <div
        className={`drop-zone ${dragOver ? "drag-over" : ""} ${status}`}
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
      >
        {preview ? (
          <img src={preview} alt="Preview" className="preview" />
        ) : (
          <div className="drop-zone-text">
            <p className="drop-zone-title">
              Drag and drop an image here, or click to select
            </p>
            <p className="drop-zone-hint">JPEG or PNG, max 10 MB</p>
          </div>
        )}

        <input
          ref={inputRef}
          type="file"
          accept="image/jpeg,image/png"
          onChange={handleChange}
          hidden
        />
      </div>

      {status === "uploading" && (
        <div className="status-message uploading-message">Uploading...</div>
      )}

      {status === "success" && (
        <div className="status-message success-message">
          Upload complete!
          <button className="upload-another" onClick={reset}>
            Upload another
          </button>
        </div>
      )}

      {status === "error" && (
        <div className="status-message error-message">
          {error}
          <button className="upload-another" onClick={reset}>
            Try again
          </button>
        </div>
      )}
    </div>
  );
}
