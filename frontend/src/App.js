import React, { useState } from "react";
import "./App.css";

import {
  FaShieldAlt,
  FaFileAlt,
  FaImage,
  FaMicrophone,
  FaChartBar,
  FaUpload,
  FaBolt,
  FaBrain,
  FaDownload,
  FaWaveSquare,
  FaExclamationTriangle,
  FaLock,
  FaSatelliteDish,
  FaFingerprint,
  FaDatabase,
  FaServer,
  FaCube,
  FaCrosshairs,
  FaLayerGroup,
  FaBug,
  FaNetworkWired
} from "react-icons/fa";

const API = "http://127.0.0.1:8000";

function App() {
  const [page, setPage] = useState("dashboard");
  const [analyticsTab, setAnalyticsTab] = useState("overview");

  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [audioFile, setAudioFile] = useState(null);

  const [result, setResult] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(false);

  const resetInputs = () => {
    setText("");
    setFile(null);
    setAudioFile(null);
    setResult(null);
  };

  const openPage = (nextPage) => {
    resetInputs();
    setPage(nextPage);
  };

  const riskClass = (risk) => {
    if (!risk) return "low";
    const r = String(risk).toLowerCase();
    if (r.includes("high")) return "high";
    if (r.includes("medium")) return "medium";
    return "low";
  };

  const formatKey = (key) => {
    return String(key).replaceAll("_", " ").toUpperCase();
  };

  const submitAnalysis = async (type) => {
    setLoading(true);
    setResult(null);

    const formData = new FormData();

    if (type === "text") {
      if (file) {
        formData.append("file", file);
      } else if (text.trim()) {
        formData.append("text", text);
      }
    }

    if (type === "image" && file) {
      formData.append("file", file);
    }

    if (type === "audio" && audioFile) {
      formData.append("file", audioFile);
    }

    try {
      const response = await fetch(`${API}/analyze`, {
        method: "POST",
        body: formData
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({
        error: error.message
      });
    }

    setLoading(false);
  };

  const loadAnalytics = async (tab = "overview") => {
    setPage("analytics");
    setAnalyticsTab(tab);
    setResult(null);

    try {
      const response = await fetch(`${API}/analytics`);
      const data = await response.json();
      setAnalytics(data);
    } catch (error) {
      setAnalytics({
        error: error.message
      });
    }
  };

  const Sidebar = () => (
    <aside className="forge-sidebar">
      <div className="forge-brand">
        <div className="forge-logo">
          <FaShieldAlt />
          <span></span>
        </div>

        <div>
          <h2>F.O.R.G.E.</h2>
          <p>Forensic Observation & Recognition Gateway</p>
        </div>
      </div>

      <nav className="forge-nav">
        <button
          className={page === "dashboard" ? "active" : ""}
          onClick={() => openPage("dashboard")}
        >
          <FaServer />
          <span>Command Center</span>
        </button>

        <button
          className={page === "text" ? "active" : ""}
          onClick={() => openPage("text")}
        >
          <FaFileAlt />
          <span>Text Forensics</span>
        </button>

        <button
          className={page === "image" ? "active" : ""}
          onClick={() => openPage("image")}
        >
          <FaImage />
          <span>Image Forensics</span>
        </button>

        <button
          className={page === "audio" ? "active" : ""}
          onClick={() => openPage("audio")}
        >
          <FaMicrophone />
          <span>Audio Forensics</span>
        </button>

        <button
          className={page === "analytics" ? "active" : ""}
          onClick={() => loadAnalytics("overview")}
        >
          <FaChartBar />
          <span>Analytics Grid</span>
        </button>
      </nav>

      <div className="secure-panel">
        <p>Security Channel</p>

        <div>
          <span className="pulse-dot green"></span>
          Backend API Online
        </div>

        <div>
          <span className="pulse-dot green"></span>
          Report Generator Active
        </div>

        <div>
          <span className="pulse-dot amber"></span>
          Image Model Online
        </div>

        <div>
          <span className="pulse-dot cyan"></span>
          XAI Layer Enabled
        </div>
      </div>
    </aside>
  );

  const Header = ({ icon, title, subtitle }) => (
    <header className="forge-header page-snap">
      <div>
        <p className="forge-eyebrow">
          <FaLock /> Secure AI Forensic Workstation
        </p>

        <h1>
          {icon}
          {title}
        </h1>

        <span>{subtitle}</span>
      </div>

      <div className="header-control-cluster">
        <div className="control-pill">
          <FaSatelliteDish />
          Local API
        </div>

        <div className="control-pill">
          <FaNetworkWired />
          Multi-Modal
        </div>

        <div className="control-pill hot">
          <FaCrosshairs />
          Live Triage
        </div>
      </div>
    </header>
  );

  const Loader = () => (
    <section className="scan-console">
      <div className="scan-cube">
        <FaFingerprint />
        <span></span>
      </div>

      <div>
        <h2>Running Forensic Scan</h2>
        <p>
          Extracting features, executing detection models, generating explainable
          evidence and risk profile.
        </p>
      </div>

      <div className="scan-bars">
        <i></i>
        <i></i>
        <i></i>
      </div>
    </section>
  );

  const ResultPanel = () => {
    if (!result || result.error) return null;

    const confidence = Number(result.confidence || 0);

    return (
      <section className={`result-command ${riskClass(result.risk_level)}`}>
        <div className="result-holo">
          <div className="holo-ring">
            <svg viewBox="0 0 120 120">
              <circle cx="60" cy="60" r="52" />
              <circle
                className="progress"
                cx="60"
                cy="60"
                r="52"
                style={{
                  strokeDashoffset: 327 - (327 * confidence) / 100
                }}
              />
            </svg>

            <div>
              <strong>{confidence.toFixed(2)}%</strong>
              <span>confidence</span>
            </div>
          </div>
        </div>

        <div className="result-data">
          <p className="forge-eyebrow">Forensic Verdict</p>

          <h2>{result.prediction}</h2>

          <div className="result-metrics">
            <div>
              <span>Risk Level</span>
              <strong>{result.risk_level || "N/A"}</strong>
            </div>

            <div>
              <span>Risk Score</span>
              <strong>{result.risk_score ?? "N/A"}</strong>
            </div>

            <div>
              <span>Modality</span>
              <strong>{result.modality || result.file_type || "Analysis"}</strong>
            </div>

            <div>
              <span>Decision Strength</span>
              <strong>{result.decision_strength || "Computed"}</strong>
            </div>
          </div>

          {result.recommendation && (
            <p className="result-note">{result.recommendation}</p>
          )}

          {result.pdf_report && (
            <a
              className="forge-primary"
              href={`${API}${result.pdf_report}`}
              target="_blank"
              rel="noreferrer"
            >
              <FaDownload /> Export Legal Evidence Report
            </a>
          )}
        </div>
      </section>
    );
  };

  const ProbabilityMatrix = () => {
    if (!result || result.error) return null;

    const ai =
      Number(result.raw_ai_probability) ||
      Number(result.risk_score) ||
      0;

    const human =
      Number(result.raw_human_probability) ||
      Math.max(0, 100 - ai);

    return (
      <section className="forge-card">
        <div className="section-title">
          <FaCrosshairs />
          <div>
            <h2>Probability Matrix</h2>
            <p>Binary confidence split generated by the forensic engine.</p>
          </div>
        </div>

        <div className="probability-matrix">
          <div className="probability-row">
            <div>
              <span>AI / Fake Probability</span>
              <b>{ai.toFixed(2)}%</b>
            </div>

            <div className="prob-track">
              <i className="ai" style={{ width: `${Math.min(ai, 100)}%` }}></i>
            </div>
          </div>

          <div className="probability-row">
            <div>
              <span>Human / Real Probability</span>
              <b>{human.toFixed(2)}%</b>
            </div>

            <div className="prob-track">
              <i className="human" style={{ width: `${Math.min(human, 100)}%` }}></i>
            </div>
          </div>
        </div>

        {Number(result.confidence || 0) < 65 && (
          <div className="forge-warning">
            <FaExclamationTriangle />
            Low-confidence result detected. Use secondary evidence or manual
            forensic validation.
          </div>
        )}
      </section>
    );
  };

  const ParameterGraph = () => {
    if (!result?.parameter_contribution) return null;

    return (
      <section className="forge-card">
        <div className="section-title">
          <FaLayerGroup />
          <div>
            <h2>Parameter Intelligence Grid</h2>
            <p>Forensic signal groups contributing to the final decision.</p>
          </div>
        </div>

        <div className="forge-graph">
          {Object.entries(result.parameter_contribution).map(([key, value]) => {
            const score = Math.min(Number(value.score || 0), 100);

            return (
              <div className="forge-graph-row" key={key}>
                <div>
                  <span>{formatKey(key)}</span>
                  <b>{score.toFixed(2)}%</b>
                </div>

                <section>
                  <i
                    className={riskClass(value.risk)}
                    style={{ width: `${score}%` }}
                  ></i>
                </section>
              </div>
            );
          })}
        </div>
      </section>
    );
  };

  const ParameterCards = () => {
    if (!result?.parameter_contribution) return null;

    return (
      <section className="forge-card">
        <div className="section-title">
          <FaBrain />
          <div>
            <h2>XAI Reasoning Console</h2>
            <p>Human-readable model explanation for the forensic decision.</p>
          </div>
        </div>

        <div className="xai-grid">
          {Object.entries(result.parameter_contribution).map(([key, value]) => (
            <div className={`xai-card ${riskClass(value.risk)}`} key={key}>
              <span className="xai-glow"></span>

              <div className="xai-head">
                <h3>{formatKey(key)}</h3>
                <b>{value.risk}</b>
              </div>

              <strong>{value.score}</strong>

              <p>{value.reason}</p>
            </div>
          ))}
        </div>
      </section>
    );
  };

  const TextHeatmap = () => {
    const highlighted =
      result?.highlighted_document ||
      result?.full_document ||
      result?.highlighted_sentences;

    if (!Array.isArray(highlighted)) return null;

    return (
      <section className="forge-card">
        <div className="section-title">
          <FaFileAlt />
          <div>
            <h2>Text Heatmap Evidence</h2>
            <p>Sentence-level suspiciousness mapping.</p>
          </div>
        </div>

        <div className="forge-text-heatmap">
          {highlighted.map((item, index) => {
            const sentence = item.sentence || item.text || item.content || String(item);
            const risk = item.risk || item.level || "LOW";

            return (
              <span key={index} className={`heat-token ${riskClass(risk)}`}>
                {sentence}
              </span>
            );
          })}
        </div>
      </section>
    );
  };

  const ImageVisuals = () => {
    if (!result?.heatmap || String(result.heatmap).includes("Error")) return null;

    return (
      <section className="forge-card">
        <div className="section-title">
          <FaImage />
          <div>
            <h2>Visual Heatmap Evidence</h2>
            <p>Highlighted visual zones affecting the image decision.</p>
          </div>
        </div>

        <div className="media-evidence">
          <img src={`${API}${result.heatmap}`} alt=" forensic heatmap" />
        </div>
      </section>
    );
  };

  const AudioVisuals = () => {
    if (!result?.waveform && !result?.spectrogram && !result?.audio_heatmap) {
      return null;
    }

    return (
      <section className="forge-card">
        <div className="section-title">
          <FaWaveSquare />
          <div>
            <h2>Acoustic Evidence Viewer</h2>
            <p>Waveform, spectrogram and audio heatmap outputs.</p>
          </div>
        </div>

        <div className="audio-grid">
          {result.waveform && (
            <div className="media-evidence">
              <h3>Waveform Timeline</h3>
              <img src={`${API}${result.waveform}`} alt="waveform" />
            </div>
          )}

          {result.spectrogram && (
            <div className="media-evidence">
              <h3>Spectral Fingerprint</h3>
              <img src={`${API}${result.spectrogram}`} alt="spectrogram" />
            </div>
          )}

          {result.audio_heatmap && (
            <div className="media-evidence">
              <h3>Audio Heatmap</h3>
              <img src={`${API}${result.audio_heatmap}`} alt="audio heatmap" />
            </div>
          )}
        </div>
      </section>
    );
  };

  const SuspiciousSegments = () => {
    if (!result?.suspicious_segments?.length) return null;

    return (
      <section className="forge-card">
        <div className="section-title">
          <FaBug />
          <div>
            <h2>Suspicious Timeline Segments</h2>
            <p>Timestamp-level acoustic anomaly interpretation.</p>
          </div>
        </div>

        <div className="segment-grid">
          {result.suspicious_segments.map((seg, index) => (
            <div className={`segment-box ${riskClass(seg.risk)}`} key={index}>
              <span>{seg.start} → {seg.end}</span>
              <b>{seg.risk}</b>
              <p>{seg.reason}</p>
            </div>
          ))}
        </div>
      </section>
    );
  };

  const ResultStack = ({ type }) => (
    <>
      {loading && <Loader />}

      {result?.error && (
        <section className="forge-error">
          <FaExclamationTriangle />
          {result.error}
        </section>
      )}

      <ResultPanel />
      <ProbabilityMatrix />

      {type === "text" && <TextHeatmap />}
      {type === "image" && <ImageVisuals />}
      {type === "audio" && <AudioVisuals />}

      <ParameterGraph />
      <ParameterCards />

      {type === "audio" && <SuspiciousSegments />}
    </>
  );

  const Dashboard = () => (
    <main className="forge-workspace page-snap">
      <Header
        icon={<FaShieldAlt />}
        title="FORGE Command Center"
        subtitle="Forensic Observation and Recognition Gateway for Emerging Generative Exploits."
      />
  
      <section className="soc-hero">
        <div className="soc-left">
          <p className="forge-eyebrow">National Cyber Forensics Console</p>
  
          <h2>
            Real-Time Deepfake Threat Intelligence & Evidence Reconstruction
          </h2>
  
          <p>
            FORGE analyzes suspicious text, image and audio evidence using
            explainable AI, forensic parameters, visual heatmaps and automated
            legal report generation.
          </p>
  
          <div className="soc-actions">
            <button className="forge-primary" onClick={() => openPage("text")}>
              <FaBolt /> Begin Investigation
            </button>
  
            <button className="forge-secondary" onClick={() => loadAnalytics("overview")}>
              <FaChartBar /> Open Threat Analytics
            </button>
          </div>
        </div>
  
        <div className="forge-core">
          <div className="core-ring ring-one"></div>
          <div className="core-ring ring-two"></div>
          <div className="core-ring ring-three"></div>
  
          <div className="core-center">
            <FaShieldAlt />
            <span>FORGE</span>
          </div>
  
          <div className="core-scan-line"></div>
        </div>
      </section>
  
      <section className="threat-stats">
        <div className="threat-stat-card">
          <FaFileAlt />
          <span>Text Engine</span>
          <strong>ONLINE</strong>
          <p>Stylometry • TF-IDF • SBERT • SHAP</p>
        </div>
        <div className="threat-stat-card">
  <FaMicrophone />
  <span>Audio Engine</span>
  <strong>ONLINE</strong>
  <p>LFCC • CNN-BiLSTM • Spectrogram</p>
</div>
        <div className="threat-stat-card">
  <FaImage />
  <span>Image Engine</span>
  <strong>ONLINE</strong>
  <p>CNN • RF Fusion • Metadata • Heatmap</p>
</div>
  
        <div className="threat-stat-card danger">
          <FaCrosshairs />
          <span>Threat Mode</span>
          <strong>ACTIVE</strong>
          <p>Live evidence triage enabled</p>
        </div>
      </section>
  
      <section className="forensic-timeline">
        <h2>FORGE Investigation Pipeline</h2>
  
        <div className="timeline-track">
          <div>
            <span>01</span>
            <b>Evidence Intake</b>
            <p>Upload text, image or audio evidence.</p>
          </div>
  
          <div>
            <span>02</span>
            <b>Feature Extraction</b>
            <p>Extract forensic and ML-based signals.</p>
          </div>
  
          <div>
            <span>03</span>
            <b>XAI Reasoning</b>
            <p>Generate explainable parameter evidence.</p>
          </div>
  
          <div>
            <span>04</span>
            <b>Threat Verdict</b>
            <p>Classify as AI/Fake or Human/Real.</p>
          </div>
  
          <div>
            <span>05</span>
            <b>Legal Report</b>
            <p>Export forensic PDF report.</p>
          </div>
        </div>
      </section>
  
      <section className="mission-grid">
        <div className="mission-card" onClick={() => openPage("text")}>
          <FaFileAlt />
          <h3>Text Forensics</h3>
          <p>Detect AI-written text using linguistic, semantic and stylometric evidence.</p>
          <span>Launch Text Module</span>
        </div>
  
        <div className="mission-card" onClick={() => openPage("image")}>
          <FaImage />
          <h3>Image Forensics</h3>
          <p>Analyze AI-generated faces, manipulated images and metadata traces.</p>
          <span>Launch Image Module</span>
        </div>
  
        <div className="mission-card" onClick={() => openPage("audio")}>
          <FaMicrophone />
          <h3>Audio Forensics</h3>
          <p>Detect synthetic voice using acoustic, spectral and temporal evidence.</p>
          <span>Launch Audio Module</span>
        </div>
      </section>
    </main>
  );
  const TextPage = () => (
    <main className="forge-workspace page-snap">
      <Header
        icon={<FaFileAlt />}
        title="Text Forensics"
        subtitle="Analyze raw text, DOCX, PDF and TXT evidence with explainable sentence-level tracing."
      />

      <section className="analysis-grid">
        <div className="evidence-input">
          <h2>Evidence Intake</h2>

          <textarea
            placeholder="Paste suspicious text evidence here..."
            value={text}
            onChange={(e) => {
              setText(e.target.value);
              if (file) setFile(null);
            }}
          />

          <label className="forge-upload">
            <FaUpload />
            Upload DOCX / PDF / TXT
            <input
              type="file"
              accept=".docx,.pdf,.txt"
              onChange={(e) => {
                setFile(e.target.files[0]);
                setText("");
              }}
            />
          </label>

          {file && (
            <div className="file-chip">
              Selected Evidence: <b>{file.name}</b>
            </div>
          )}

          <button
            className="forge-primary full"
            disabled={loading || (!text.trim() && !file)}
            onClick={() => submitAnalysis("text")}
          >
            <FaBolt /> Execute Text Scan
          </button>
        </div>

        <div className="module-intel">
          <h2>Text Signal Stack</h2>
          <p>Stylometric variance</p>
          <p>TF-IDF vocabulary fingerprint</p>
          <p>N-Gram phrase patterning</p>
          <p>SBERT semantic behavior</p>
          <p>SHAP-based explanation layer</p>
        </div>
      </section>

      <ResultStack type="text" />
    </main>
  );

  const ImagePage = () => (
    <main className="forge-workspace page-snap">
      <Header
        icon={<FaImage />}
        title="Image Forensics"
        subtitle="Analyze image evidence for generated faces, tampering traces, artifacts and metadata inconsistencies."
      />

      <section className="analysis-grid">
        <div className="evidence-input">
          <h2>Image Evidence Intake</h2>

          <label className="forge-upload large">
            <FaUpload />
            Upload PNG / JPG / JPEG / WEBP
            <input
              type="file"
              accept=".png,.jpg,.jpeg,.webp"
              onChange={(e) => setFile(e.target.files[0])}
            />
          </label>

          {file && (
            <>
              <div className="file-chip">
                Selected Evidence: <b>{file.name}</b>
              </div>

              <img
                className="preview-frame"
                src={URL.createObjectURL(file)}
                alt="preview"
              />
            </>
          )}

          <button
            className="forge-primary full"
            disabled={loading || !file}
            onClick={() => submitAnalysis("image")}
          >
            <FaBolt /> Execute Image Scan
          </button>
        </div>

        <div className="module-intel">
          <h2>Image Signal Stack</h2>
          <p>Visual artifact scoring</p>
          <p>GAN fingerprint estimation</p>
          <p>Metadata authenticity trace</p>
          <p>Face anatomy analysis</p>
          <p>Heatmap evidence renderer</p>
        </div>
      </section>

      <ResultStack type="image" />
    </main>
  );

  const AudioPage = () => (
    <main className="forge-workspace page-snap">
      <Header
        icon={<FaMicrophone />}
        title="Audio Forensics"
        subtitle="Analyze synthetic voice and forged audio using LFCC, CNN-BiLSTM and acoustic XAI."
      />

      <section className="analysis-grid">
        <div className="evidence-input">
          <h2>Audio Evidence Intake</h2>

          <label className="forge-upload large">
            <FaUpload />
            Upload WAV / FLAC / MP3 / M4A
            <input
              type="file"
              accept=".wav,.flac,.mp3,.m4a"
              onChange={(e) => setAudioFile(e.target.files[0])}
            />
          </label>

          {audioFile && (
            <div className="audio-chip">
              <p>{audioFile.name}</p>
              <audio controls src={URL.createObjectURL(audioFile)} />
            </div>
          )}

          <button
            className="forge-primary full"
            disabled={loading || !audioFile}
            onClick={() => submitAnalysis("audio")}
          >
            <FaBolt /> Execute Audio Scan
          </button>
        </div>

        <div className="module-intel">
          <h2>Audio Signal Stack</h2>
          <p>LFCC spectral feature extraction</p>
          <p>CNN-BiLSTM fusion model</p>
          <p>Pitch, prosody and phase analysis</p>
          <p>Waveform and spectrogram renderer</p>
          <p>27 acoustic forensic parameters</p>
        </div>
      </section>

      <ResultStack type="audio" />
    </main>
  );

  const AnalyticsPage = () => {
    const data = analytics || {};

    const cards = Object.entries(data).filter(([key]) => key !== "error");

    const filteredCards = cards.filter(([key]) => {
      if (analyticsTab === "overview") return true;
      return key.toLowerCase().includes(analyticsTab);
    });

    return (
      <main className="forge-workspace page-snap">
        <Header
          icon={<FaChartBar />}
          title="Analytics Grid"
          subtitle="Mission-level operational statistics across text, image and audio forensic modules."
        />

        <section className="analytics-switcher">
          <button
            className={analyticsTab === "overview" ? "active" : ""}
            onClick={() => setAnalyticsTab("overview")}
          >
            <FaDatabase /> Overview
          </button>

          <button
            className={analyticsTab === "text" ? "active" : ""}
            onClick={() => setAnalyticsTab("text")}
          >
            <FaFileAlt /> Text Analytics
          </button>

          <button
            className={analyticsTab === "image" ? "active" : ""}
            onClick={() => setAnalyticsTab("image")}
          >
            <FaImage /> Image Analytics
          </button>

          <button
            className={analyticsTab === "audio" ? "active" : ""}
            onClick={() => setAnalyticsTab("audio")}
          >
            <FaMicrophone /> Audio Analytics
          </button>
        </section>

        {analytics?.error && (
          <section className="forge-error">
            <FaExclamationTriangle />
            {analytics.error}
          </section>
        )}

        {!analytics?.error && (
          <section className="analytics-grid">
            {filteredCards.map(([key, value]) => (
              <div className="analytics-card" key={key}>
                <span>{formatKey(key)}</span>
                <strong>{value}</strong>
              </div>
            ))}
          </section>
        )}
      </main>
    );
  };

  return (
    <div className="forge-app">
      <div className="forge-bg-grid"></div>
      <div className="forge-noise"></div>
      <div className="orb orb-a"></div>
      <div className="orb orb-b"></div>
      <div className="orb orb-c"></div>

      <Sidebar />

      {page === "dashboard" && <Dashboard />}
      {page === "text" && <TextPage />}
      {page === "image" && <ImagePage />}
      {page === "audio" && <AudioPage />}
      {page === "analytics" && <AnalyticsPage />}
    </div>
  );
}

export default App;