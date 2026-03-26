import { useState } from "react";
import "./ImagePreview.css";

interface ImagePreviewProps {
  src: string;
}

export default function ImagePreview({ src }: ImagePreviewProps) {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        className="image-thumbnail"
        onClick={() => setOpen(true)}
        title="View uploaded image"
      >
        <img src={src} alt="Blood test" />
        <span className="thumbnail-label">View image</span>
      </button>

      {open && (
        <div className="lightbox-overlay" onClick={() => setOpen(false)}>
          <div
            className="lightbox-content"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              className="lightbox-close"
              onClick={() => setOpen(false)}
              aria-label="Close preview"
            >
              &times;
            </button>
            <img src={src} alt="Blood test full preview" />
          </div>
        </div>
      )}
    </>
  );
}
