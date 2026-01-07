import React, { useState } from "react";
import { UploadForm } from "./components/UploadForm";
import { AnalysisResult } from "./components/AnalysisResult";

export interface AnalysisResponse {
  question: string;
  answer: string;
  chunks_used: string[];
  num_chunks: number;
}

const App: React.FC = () => {
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  return (
    <div className="app">
      <header className="app-header">
        <div className="app-header-inner">
          <div>
            <h1 className="app-title">LegalEase AI</h1>
            <p className="app-subtitle">
              Smart contract analyzer. Upload a contract and get AI-powered risk insights.
            </p>
          </div>
          <div className="badge">Groq · RAG · FastAPI</div>
        </div>
      </header>

      <main className="app-main">
        <div className="layout-grid">
          <UploadForm
            onStart={() => {
              setIsLoading(true);
              setError(null);
              setResult(null);
            }}
            onError={(msg) => {
              setIsLoading(false);
              setError(msg);
            }}
            onComplete={(data) => {
              setIsLoading(false);
              setResult(data);
            }}
          />

          <AnalysisResult isLoading={isLoading} error={error} result={result} />
        </div>
      </main>
    </div>
  );
};

export default App;


