import React, { useEffect, useMemo, useRef, useState } from "react";
import { AnimatePresence, motion, useScroll, useTransform } from "framer-motion";
import { FaCheck, FaFileAlt, FaImage, FaMicrophone, FaUndo } from "react-icons/fa";

import forgeVideo from "../assets/videos/forge-intelligence-core.mp4";
import textVideo from "../assets/videos/text-engine.mp4";
import imageVideo from "../assets/videos/image-engine.mp4";
import audioVideo from "../assets/videos/audio-engine.mp4";

const ENGINES = [
  {
    id: "text",
    number: "01",
    eyebrow: "LANGUAGE INTELLIGENCE",
    title: "Text Forensics",
    icon: FaFileAlt,
    video: textVideo,
    stack: ["SBERT", "STYLOMETRY", "TF-IDF", "N-GRAM"],
    description:
      "Detect synthetic language through semantic behaviour, vocabulary fingerprints and sentence-level evidence.",
    features: [
      "Semantic intelligence",
      "Sentence attribution",
      "Confidence analysis",
      "Explainable reasoning",
    ],
  },
  {
    id: "image",
    number: "02",
    eyebrow: "VISUAL INTELLIGENCE",
    title: "Image Forensics",
    icon: FaImage,
    video: imageVideo,
    stack: ["CNN", "HEATMAPS", "REGIONS", "METADATA"],
    description:
      "Expose manipulated regions, synthetic textures and visual inconsistencies through explainable image evidence.",
    features: [
      "Regional evidence",
      "Synthetic texture analysis",
      "Forensic heatmaps",
      "Visual explainability",
    ],
  },
  {
    id: "audio",
    number: "03",
    eyebrow: "ACOUSTIC INTELLIGENCE",
    title: "Audio Forensics",
    icon: FaMicrophone,
    video: audioVideo,
    stack: ["LFCC", "SPECTRUM", "TIMELINE", "VOICE DNA"],
    description:
      "Investigate acoustic signatures, temporal irregularities and synthetic voice traces across the recording.",
    features: [
      "Voice authenticity",
      "Temporal evidence",
      "Spectral analysis",
      "Acoustic explainability",
    ],
  },
];

function BootSequence({ onComplete }) {
  const [step, setStep] = useState(0);
  const messages = useMemo(
    () => [
      "INITIALIZING FORENSIC CORE",
      "TEXT INTELLIGENCE / READY",
      "VISION INTELLIGENCE / READY",
      "ACOUSTIC INTELLIGENCE / READY",
      "EXPLAINABILITY LAYER / READY",
      "F.O.R.G.E ONLINE",
    ],
    []
  );

  useEffect(() => {
    const timers = messages.map((_, index) =>
      window.setTimeout(() => setStep(index), 280 + index * 280)
    );
    const finish = window.setTimeout(onComplete, 2050);
    return () => {
      timers.forEach(window.clearTimeout);
      window.clearTimeout(finish);
    };
  }, [messages, onComplete]);

  return (
    <motion.div
      className="forge-boot"
      initial={{ opacity: 1 }}
      exit={{ opacity: 0, filter: "blur(12px)" }}
      transition={{ duration: 0.55 }}
    >
      <div className="forge-boot-mark">F.O.R.G.E</div>
      <div className="forge-boot-terminal">
        {messages.slice(0, step + 1).map((message, index) => (
          <motion.div
            key={message}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <span>{String(index + 1).padStart(2, "0")}</span>
            <p>{message}</p>
            <i>{index === step ? "RUN" : "OK"}</i>
          </motion.div>
        ))}
      </div>
      <div className="forge-boot-line"><i style={{ width: `${((step + 1) / messages.length) * 100}%` }} /></div>
    </motion.div>
  );
}

function MetricCounter({ value, suffix = "+", label, index }) {
  const ref = useRef(null);
  const [count, setCount] = useState(0);
  const [started, setStarted] = useState(false);

  useEffect(() => {
    const node = ref.current;
    if (!node) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setStarted(true);
          observer.disconnect();
        }
      },
      { threshold: 0.45 }
    );
    observer.observe(node);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (!started) return;
    const duration = 1450 + index * 180;
    const start = performance.now();
    let frame;
    const tick = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 4);
      setCount(Math.round(value * eased));
      if (progress < 1) frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [started, value, index]);

  return (
    <motion.article
      ref={ref}
      className="forge-metric"
      initial={{ opacity: 0, y: 28 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.45 }}
      transition={{ duration: 0.75, delay: index * 0.12 }}
    >
      <strong>{count}{suffix}</strong>
      <span>{label}</span>
    </motion.article>
  );
}

function EngineCard({ engine, index, onLaunch }) {
  const [flipped, setFlipped] = useState(false);
  const cardRef = useRef(null);
  const Icon = engine.icon;

  function handleMove(event) {
    const node = cardRef.current;
    if (!node || flipped) return;
    const rect = node.getBoundingClientRect();
    const x = (event.clientX - rect.left) / rect.width;
    const y = (event.clientY - rect.top) / rect.height;
    node.style.setProperty("--rx", `${(0.5 - y) * 8}deg`);
    node.style.setProperty("--ry", `${(x - 0.5) * 10}deg`);
    node.style.setProperty("--mx", `${x * 100}%`);
    node.style.setProperty("--my", `${y * 100}%`);
  }

  function resetMove() {
    const node = cardRef.current;
    if (!node) return;
    node.style.setProperty("--rx", "0deg");
    node.style.setProperty("--ry", "0deg");
  }

  return (
    <motion.article
      className="forge-engine-shell"
      initial={{ opacity: 0, y: 80 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 0.9, delay: index * 0.12, ease: [0.16, 1, 0.3, 1] }}
    >
      <button
        ref={cardRef}
        type="button"
        className={`forge-engine-card ${flipped ? "is-flipped" : ""}`}
        onMouseMove={handleMove}
        onMouseLeave={resetMove}
        onClick={() => onLaunch(engine)}
        aria-label={`Enter ${engine.title}`}
      >
        <span className="forge-engine-tilt">
          <span className="forge-engine-inner">
            <span className="forge-engine-face forge-engine-front">
              <video autoPlay muted loop playsInline preload="metadata">
                <source src={engine.video} type="video/mp4" />
              </video>
              <span className="forge-engine-shade" />
              <span className="forge-engine-card-grid" />
              <span className="forge-engine-reflection" />
              <span className="forge-engine-head">
                <b>{engine.number}</b>
                <em><i /> ENGINE ONLINE</em>
              </span>
              <span className="forge-engine-icon"><Icon /></span>
              <span className="forge-engine-copy">
                <small>{engine.eyebrow}</small>
                <strong>{engine.title}</strong>
                <span>{engine.stack.map((item) => <i key={item}>{item}</i>)}</span>
                <em>CLICK TO ENTER</em>
              </span>
            </span>

            <span className="forge-engine-face forge-engine-back">
              <span className="forge-engine-backlight" />
              <span className="forge-engine-head">
                <b>{engine.number}</b>
                <em>{engine.eyebrow}</em>
              </span>
              <span className="forge-engine-backcopy">
                <Icon />
                <small>HOW F.O.R.G.E THINKS</small>
                <strong>{engine.title}</strong>
                <p>{engine.description}</p>
                <span>
                  {engine.features.map((feature) => (
                    <i key={feature}><FaCheck /> {feature}</i>
                  ))}
                </span>
                <em>CLICK ANYWHERE TO ENTER</em>
              </span>
            </span>
          </span>
        </span>
      </button>

      <button
        type="button"
        className="forge-flip-external"
        onClick={() => setFlipped((current) => !current)}
      >
        <FaUndo /> {flipped ? "Show engine" : "Flip card"}
      </button>
    </motion.article>
  );
}

export default function CinematicCommandCentre({ openPage }) {
  const [booting, setBooting] = useState(true);
  const [launching, setLaunching] = useState(null);
  const [scrolled, setScrolled] = useState(false);
  const heroRef = useRef(null);
  const { scrollYProgress } = useScroll({ target: heroRef, offset: ["start start", "end start"] });
  const heroScale = useTransform(scrollYProgress, [0, 1], [1.03, 1.18]);
  const heroOpacity = useTransform(scrollYProgress, [0, 0.86], [1, 0]);
  const heroY = useTransform(scrollYProgress, [0, 1], [0, -120]);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 70);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    document.documentElement.classList.add("forge-cinematic-scroll");
    return () => {
      window.removeEventListener("scroll", onScroll);
      document.documentElement.classList.remove("forge-cinematic-scroll");
    };
  }, []);

  function goTo(id) {
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function launch(engine) {
    if (launching) return;
    setLaunching(engine);
    window.setTimeout(() => openPage(engine.id), 1450);
  }

  function handleNavGlow(event) {
    const rect = event.currentTarget.getBoundingClientRect();
    event.currentTarget.style.setProperty("--nav-x", `${event.clientX - rect.left}px`);
    event.currentTarget.style.setProperty("--nav-y", `${event.clientY - rect.top}px`);
  }

  return (
    <main className="forge-cinematic-home">
      <AnimatePresence>{booting && <BootSequence onComplete={() => setBooting(false)} />}</AnimatePresence>

      <nav className={`forge-glow-nav ${scrolled ? "is-scrolled" : ""}`} onMouseMove={handleNavGlow}>
        <button type="button" className="forge-word-brand" onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}>
          <strong>F.O.R.G.E</strong>
          <small>DIGITAL FORENSIC INTELLIGENCE</small>
        </button>
        <div>
          <button type="button" onClick={() => goTo("forge-about")}>About</button>
          <button type="button" onClick={() => goTo("forge-engines")}>Engines</button>
          <button type="button" onClick={() => goTo("forge-mission")}>Mission</button>
        </div>
      </nav>

      <section ref={heroRef} className="forge-cinematic-hero">
        <motion.video style={{ scale: heroScale }} autoPlay muted loop playsInline preload="metadata">
          <source src={forgeVideo} type="video/mp4" />
        </motion.video>
        <div className="forge-hero-black" />
        <div className="forge-hero-grid" />
        <div className="forge-hero-noise" />
        <motion.div className="forge-hero-copy" style={{ opacity: heroOpacity, y: heroY }}>
          <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 2.15, duration: 0.8 }}>
            MULTIMODAL FORENSIC INTELLIGENCE
          </motion.p>
          <motion.h1 initial={{ opacity: 0, y: 60, filter: "blur(18px)" }} animate={{ opacity: 1, y: 0, filter: "blur(0px)" }} transition={{ delay: 2.08, duration: 1.15, ease: [0.16, 1, 0.3, 1] }}>
            F.O.R.G.E
          </motion.h1>
          <motion.div className="forge-hero-definition" initial={{ opacity: 0, y: 25 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 2.55, duration: 0.9 }}>
            <strong>Forensic Observation &amp; Recognition Gateway</strong>
            <span>for Emerging Generative Exploits</span>
          </motion.div>
        </motion.div>
        <div className="forge-hero-scroll"><span>SCROLL TO INVESTIGATE</span><i /></div>
      </section>

      <section className="forge-metrics-section" aria-label="Platform analytics">
        <div className="forge-metrics-intro">
          <small>LIVE PLATFORM SIGNALS</small>
          <p>Growing forensic intelligence across evidence, reporting and multimodal analysis.</p>
        </div>
        <div className="forge-metrics-grid">
          <MetricCounter value={500} label="Evidence items analysed" index={0} />
          <MetricCounter value={100} label="Forensic reports generated" index={1} />
          <MetricCounter value={3} suffix="" label="Multimedia engines supported" index={2} />
        </div>
      </section>

      <section id="forge-about" className="forge-story forge-story-language">
        <div className="forge-story-orbit" />
        <motion.div initial={{ opacity: 0, y: 80 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.35 }} transition={{ duration: 1 }}>
          <small>THE FORENSIC PREMISE</small>
          <h2>Artificial intelligence<br /><em>cannot erase</em><br />its fingerprints.</h2>
          <p>F.O.R.G.E turns invisible generative patterns into evidence an investigator can understand.</p>
        </motion.div>
      </section>

      <section className="forge-evidence-sequence">
        <article>
          <video autoPlay muted loop playsInline><source src={textVideo} type="video/mp4" /></video>
          <div />
          <motion.h3 initial={{ opacity: 0, x: -70 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true, amount: 0.5 }} transition={{ duration: 0.9 }}>
            Every generated sentence<br /><em>contains measurable evidence.</em>
          </motion.h3>
        </article>
        <article>
          <video autoPlay muted loop playsInline><source src={imageVideo} type="video/mp4" /></video>
          <div />
          <motion.h3 initial={{ opacity: 0, x: 70 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true, amount: 0.5 }} transition={{ duration: 0.9 }}>
            Every manipulated pixel<br /><em>leaves a visual trace.</em>
          </motion.h3>
        </article>
        <article>
          <video autoPlay muted loop playsInline><source src={audioVideo} type="video/mp4" /></video>
          <div />
          <motion.h3 initial={{ opacity: 0, y: 70 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.5 }} transition={{ duration: 0.9 }}>
            Every synthetic voice<br /><em>carries an acoustic signature.</em>
          </motion.h3>
        </article>
      </section>

      <section className="forge-explainability">
        <motion.div initial={{ opacity: 0, scale: 0.94 }} whileInView={{ opacity: 1, scale: 1 }} viewport={{ once: true, amount: 0.4 }} transition={{ duration: 1.05 }}>
          <small>EXPLAINABLE INTELLIGENCE</small>
          <h2>Detection is only<br />the beginning.</h2>
          <p>Understanding is the evidence.</p>
        </motion.div>
      </section>

      <section id="forge-engines" className="forge-engines-section">
        <div className="forge-engines-heading">
          <div className="forge-engines-kicker">
            <small>FORENSIC INTELLIGENCE SYSTEMS</small>
            <span>03 ENGINES · ONE INVESTIGATION LAYER</span>
          </div>
          <div className="forge-engines-title-row">
            <h2>Choose your<br /><em>forensic engine.</em></h2>
            <p>Analyse language, visual media and acoustic signals through three specialised forensic systems.</p>
          </div>
        </div>
        <div className="forge-engine-grid">
          {ENGINES.map((engine, index) => (
            <EngineCard key={engine.id} engine={engine} index={index} onLaunch={launch} />
          ))}
        </div>
      </section>

      <section id="forge-mission" className="forge-mission-section">
        <video autoPlay muted loop playsInline preload="metadata"><source src={forgeVideo} type="video/mp4" /></video>
        <div className="forge-mission-shade" />
        <motion.div initial={{ opacity: 0, y: 70 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.4 }} transition={{ duration: 1 }}>
          <small>THE MISSION</small>
          <h2>Truth is not guessed.<br /><em>It is proven.</em></h2>
          <p>F.O.R.G.E — Forensic Observation &amp; Recognition Gateway for Emerging Generative Exploits.</p>
        </motion.div>
        <footer><strong>F.O.R.G.E</strong><span>DIGITAL FORENSIC INTELLIGENCE PLATFORM DESIGNED BY ASHISH RANJAN CDAC CINE</span></footer>
      </section>

      <AnimatePresence>
        {launching && (
          <motion.div className="forge-launch-overlay" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <motion.div initial={{ opacity: 0, scale: 0.92 }} animate={{ opacity: 1, scale: 1 }}>
              <small>INITIALIZING</small>
              <h2>{launching.title}</h2>
              <div className="forge-launch-progress"><i /></div>
              <p>Loading neural models · Evidence pipeline · Explainability layer</p>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}
