import { useState } from "react";
import ImageUpload from "../components/ImageUpload";
import "./Home.css";

export default function Home() {
  const [uploadedId, setUploadedId] = useState<number | null>(null);

  return (
    <div className="home">
      <h2>Upload a blood test</h2>
      <p>Upload an image of your blood test results to get started.</p>
      <ImageUpload onUploadComplete={(id) => setUploadedId(id)} />
      {uploadedId && (
        <p className="uploaded-id">Blood test ID: {uploadedId}</p>
      )}
    </div>
  );
}
