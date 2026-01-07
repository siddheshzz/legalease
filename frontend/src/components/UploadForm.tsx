import React, { useState } from "react";
import axios from "axios";
import type { AnalysisResponse } from "../App";

interface Props {
  onStart: () => void;
  onError: (message: string) => void;
  onComplete: (data: AnalysisResponse) => void;
}

export const UploadForm: React.FC<Props> = ({ onStart, onError, onComplete }) => {
  const [file, setFile] = useState<File | null>(null);
  const [question, setQuestion] = useState(
    "Highlight any risky clauses and tell me if there is a 3-month notice period."
  );

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!file) {
      onError("Please select a PDF contract to analyze.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("question", question);

    try {
      onStart();
      const response = await axios.post<AnalysisResponse>(
        "/api/v1/documents/analyze",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" }
        }
      );
      onComplete(response.data);
    } catch (err: any) {
      const detail =
        err?.response?.data?.detail ??
        err?.message ??
        "An unexpected error occurred while analyzing the document.";
      onError(detail);
    }
  };

  return (
    <section className="card card--primary">
      <h2 className="card-title">Analyze a contract</h2>
      <p className="card-subtitle">
        Upload a PDF contract or agreement and ask a natural language question about it. LegalEase
        AI will search the document and answer based on the actual text.
      </p>

      <form className="form" onSubmit={handleSubmit}>
        <div className="field">
          <label className="field-label">Contract PDF</label>
          <input
            type="file"
            accept="application/pdf"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            className="field-input field-input--file"
          />
          <p className="field-helper">
            We read the document in memory; nothing is persisted in the demo setup.
          </p>
        </div>

        <div className="field">
          <label className="field-label">Question</label>
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            rows={3}
            className="field-textarea"
            placeholder="e.g. Is there a 3 month notice period? Can the landlord increase rent without notice?"
          />
        </div>

        <button
          type="submit"
          className="btn btn--primary"
        >
          Analyze document
        </button>
      </form>
    </section>
  );
};


