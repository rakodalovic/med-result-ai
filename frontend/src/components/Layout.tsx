import type { ReactNode } from "react";
import "./Layout.css";

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="layout">
      <header className="header">
        <div className="header-brand">
          <div className="header-logo">M</div>
          <div>
            <h1>MedResult AI</h1>
            <p>Blood test analyst</p>
          </div>
        </div>
      </header>
      <main className="main">{children}</main>
      <footer className="footer">
        <p>
          For educational purposes only. This is not a medical diagnosis.
          Always consult a healthcare professional.
        </p>
      </footer>
    </div>
  );
}
