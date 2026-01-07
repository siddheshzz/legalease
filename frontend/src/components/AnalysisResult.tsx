import React from "react";
import ReactMarkdown from "react-markdown";
import type { AnalysisResponse } from "../App";

interface Props {
  isLoading: boolean;
  error: string | null;
  result: AnalysisResponse | null;
}

export const AnalysisResult: React.FC<Props> = ({ isLoading, error, result }) => {
  return (
    <section className="card card--secondary">
      <h2 className="card-title">Results</h2>

      {isLoading && (
        <div className="loading-row">
          <div className="spinner" />
          Analyzing your document with LegalEase AI...
        </div>
      )}

      {!isLoading && error && (
        <div className="alert alert--error">
          {error}
        </div>
      )}

      {!isLoading && !error && !result && (
        <p className="placeholder-text">
          Upload a contract and ask a question to see the analysis here, including the answer and
          the specific passages the AI used.
        </p>
      )}

      {result && !isLoading && !error && (
        <div className="result-content">
          <div>
            <h3 className="section-title">Question</h3>
            <p className="section-body">{result.question}</p>
          </div>

          <div>
            <h3 className="section-title">Answer</h3>
            <ReactMarkdown className="result-answer-markdown">
              {result.answer}
            </ReactMarkdown>
          </div>

          <div>
            <h3 className="section-title">
              Evidence from the contract ({result.chunks_used.length} of {result.num_chunks} chunks)
            </h3>
            <div className="result-chunks">
              {result.chunks_used.map((chunk, idx) => (
                <article key={idx} className="result-chunk">
                  <div className="result-chunk-title">Excerpt {idx + 1}</div>
                  <p className="result-chunk-body">{chunk}</p>
                </article>
              ))}
            </div>
          </div>
        </div>
      )}
    </section>
  );
};


