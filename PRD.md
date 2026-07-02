# PRD.md - Product Requirements Document
# Project: Vibe Coding Multimedia Presentation Engine (Reveal.js)
# Group Code: biu-rl07

## 1. Executive Summary & Goals
This project delivers a fully automated, code-based interactive presentation consisting of exactly 20 slides using Reveal.js, driven by Python and structured JSON specifications. The content serves as an executive pedagogical guide to "Multimedia Architecture via Vibe Coding," aligning with the course curriculum. The ultimate goal is to separate content intent from visual execution while ensuring 100% stable Right-to-Left (RTL) layout consistency for Hebrew text.

## 2. Target Audience & Tone
*   **Audience:** Academic evaluators, executive managers, and students of AI-native engineering.
*   **Tone:** Professional, highly structured, academic, and inspiring.

## 3. Scope & Key Requirements
*   **Slide Count:** Exactly 20 sequential slides.
*   **Language Distribution:** At least 50% of the slides (10+ slides) will be written in Hebrew. 
*   **RTL Architecture Compliance:** All Hebrew lists will utilize custom CSS Flexbox or layout tables matching `display: table` structure to anchor bullets properly.
*   **Bidi Control:** Text boxes containing mixed language elements will apply explicit `unicode-bidi: embed` and `<span dir="ltr">` wrap for foreign acronyms (e.g., AI, LLM, BPM, JSON).
*   **Visual Effects & Transitions:** Implementation of slide-specific transition effects configured globally or per-slide within the JSON contract.
*   **Audio Soundtrack:** A fully synthesized background theme produced via Suno V5, integrated programmatically via background sound controllers, utilizing slant rhyme lyrical strategies.

## 4. Technical Stack
*   **Frontend Engine:** Reveal.js (HTML5/CSS3/JavaScript).
*   **Build Pipeline:** Python automation script for parsing JSON input configurations and injecting data chunks into HTML templates.
*   **Version Control:** Git repository with semantic commit logs shared with rmisegal@gmail.com.
