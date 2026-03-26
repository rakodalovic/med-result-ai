import type { ReactNode } from "react";
import "./Layout.css";

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="layout">
      <header className="header">
        <h1>MedResult AI</h1>
        <p>Blood test result analyst</p>
      </header>
      <main className="main">{children}</main>
      <footer className="footer">
        <p>For educational purposes only. Not a medical diagnosis.</p>
      </footer>
    </div>
  );
}
