
# Echoes of Culture — Project Proposal

**Project Title:** Echoes of Culture  
**Team:** Echoes of Culture Collective (or your chosen team name)  
**Duration:** ~5–6 weeks  
**Tools:** Python (pygame / processing.py / tkinter), pygame.mixer or pyaudio, JSON for data, GitHub for version control  
**Prepared by:** Linh (Project Lead / Creative Director)

---

## 1. Executive Summary
"Echoes of Culture" is an interactive audiovisual installation that celebrates cultural diversity through clickable visual symbols that trigger short sound samples and generative animations. The experience aims to let users co-create a "global symphony" by exploring cultural icons — each interaction contributing a layer of color, motion, and sound. The project balances creative storytelling with technical implementation and is designed to be completed within ~5–6 weeks by a 4-person team.

---

## 2. Objectives
- Showcase cultural diversity and promote understanding via an interactive medium.  
- Leverage creative coding to translate cultural artifacts into audiovisual building blocks.  
- Deliver a polished interactive demo and a clear presentation of the creative & technical process.

---

## 3. Target Audience & Use Case
- Course instructors and classmates (grading/demo).  
- Public demo audience (campus exhibition) — friendly for non-technical users.  
- Use case: short interactive installation or web-like application for live demo (screen + audio).

---

## 4. Core Features (Minimum Viable Product)
1. **Interactive Cultural Map:** A main screen with 6–8 clickable cultural symbols/icons.  
2. **Sound Triggers:** Each symbol plays a short (3–6s) sound clip representative of that culture.  
3. **Generative Visuals:** Clicking a symbol spawns a visual animation (particles, patterns, or shape morph) matching the sound's mood.  
4. **Mixing / Global Symphony:** Multiple active sounds/visuals blend into a cohesive audiovisual output.  
5. **Simple UI:** Title screen, help/instructions popup, credits, and a "reset" button.  
6. **Data File:** A JSON file with cultural elements (id, name, region, audio file path, icon path, color palette, description, credit).

---

## 5. Suggested Technical Stack
- **Language:** Python 3.x  
- **Visuals / Interaction:** `pygame` or `processing.py` (choose based on team familiarity)  
- **Audio:** `pygame.mixer` for simple playback or `pyaudio` for lower-level control; consider `sounddevice` if available.  
- **Data & Assets:** JSON for metadata; store audio (wav/mp3), SVG/PNG icons, and small sample images in `assets/`.  
- **Version Control:** Git + GitHub (branch per feature / per week).  
- **Presentation:** Record demo via screen recorder (OBS or built-in recorder) and create a 4–6 slide deck.

---

## 6. Data Schema (example JSON entry)
```
{
  "id": "jp_taiko",
  "name": "Taiko Drum — Japan",
  "region": "East Asia",
  "audio": "assets/audio/japan_taiko.wav",
  "icon": "assets/icons/taiko.png",
  "colors": ["#DCR14A", "#E63946", "#2B2D42"],
  "animation_type": "pulse_rings",
  "description": "Short taiko drum rhythm representing festival energy.",
  "credit": "Sourced from [source], licensed under CC-BY"
}
```

---

## 7. UX / Interaction Flow
1. **Landing Screen:** Project title, short instructions ("Click symbols to play sounds and paint the screen. Press Reset to clear.").  
2. **Main Canvas:** Grid or circular map with 6–8 symbols representing cultures. Hover shows short tooltip; click triggers sound + animation.  
3. **Symphony Mode:** As multiple symbols are triggered, the system mixes audio tracks and layers visuals. Visual intensity corresponds to audio amplitude or number of active tracks.  
4. **Reset & Credits:** Reset returns to idle state. Credits screen lists cultural sources and team roles.

---

## 8. Art Direction & Sound Design
- **Visual Style:** Minimal, symbolic icons with generative patterns inspired by each culture's traditional motifs. Use simple palettes per culture (2–4 main colors). Animations should be smooth and not overly CPU-heavy (avoid thousands of particles unless optimized).  
- **Sound Style:** Short authentic or inspired audio clips (3–6 seconds) — percussion loops, short melodic phrases, or ambient textures. Normalize volume levels and use simple mixing to avoid clipping.  
- **Accessibility:** Provide captions/short text descriptions for each cultural element and avoid flashing patterns that may trigger discomfort.

---

## 9. Detailed Task List & Weekly Breakdown

### Week 1 — Research & Concept Finalization (Deliverables: moodboard, dataset plan)
- Team meeting: finalize 6–8 cultures to include.  
- Research & collect 2–3 sound candidates per culture (researcher).  
- Create moodboard: color palettes, icon references (designer).  
- Draft JSON schema and project repo skeleton (lead coder).

**Assigned:**  
- Linh: overall creative direction, moodboard, icon style guide.  
- Member B (Research): find sound references + licensing notes.  
- Member A (Lead Coder): repo setup, starter window code.  
- Member C (Visual Designer): rough icon sketches.

---

### Week 2 — Prototype UI & Asset Collection (Deliverables: visual prototype, sample assets)
- Implement a static main canvas with placeholder icons.  
- Implement click detection and simple visual response (placeholder animation).  
- Finalize + convert audio clips to appropriate format (wav recommended).  
- Organize assets in `assets/` and populate initial JSON.

**Assigned:**  
- Lead Coder: implement canvas + interaction detection.  
- Visual Designer: finalize 6–8 icons and export PNGs/SVGs.  
- Sound Integrator: process audio files, normalize, and test playback.  
- Linh: review visual/audio cohesion and update palette.

---

### Week 3 — Core Development: Visuals & Sound Integration (Deliverables: playable beta)
- Integrate audio playback with click events.  
- Implement 2–3 animation types (e.g., pulse, radial particles, pattern growth).  
- Implement audio mixing logic and simple volume control.  
- Add tooltip and simple instruction overlay.

**Assigned:**  
- Lead Coder & Sound Integrator: integrate audio & visuals, implement mixing.  
- Visual Designer: refine animations and transitions.  
- Linh: test experience flow & user clarity.

---

### Week 4 — Polishing & Performance Optimization (Deliverables: near-final build)
- Add more animations and refine timing with audio.  
- Optimize frame rate and reduce CPU usage (limit particle counts, use surfaces).  
- Expand dataset to final 6–8 cultural entries.  
- Conduct internal user testing and document issues.

**Assigned:**  
- Entire team: bug fixes, usability testing, performance tweaks.  
- Member B: ensure proper credits and license documentation.

---

### Week 5 — Finalization & Presentation (Deliverables: final build, slides, demo video)
- Final polish: UI, transitions, credits screen.  
- Record a 2–3 minute demo video showing core interactions.  
- Prepare a 4–6 slide presentation: concept, process, demo, reflection.  
- Final testing and packaging (zip repository with README).

**Assigned:**  
- Linh: finalize presentation & script.  
- Lead Coder & Sound Integrator: produce final build and ensure portability.  
- Visual Designer & Researcher: finalize credits and asset list.

---

## 10. Quality Assurance & Testing Plan
- Weekly playtest sessions (30–60 mins) with at least 2 external testers.  
- Test on the target hardware (laptop with standard CPU) to check performance.  
- Accessibility check: provide alt-text descriptions and ensure no high-frequency flashing.  
- Sound balancing: normalize audio and test with headphones & speakers.

---

## 11. Repo Structure (suggestion)
```
/echoes-of-culture
  /assets
    /audio
    /icons
    /images
  /src
    main.py
    visuals.py
    audio.py
    data_loader.py
  /docs
    proposal.md
    LICENSES.md
  README.md
```

---

## 12. Risks & Mitigations
- **Risk:** Licensing issues for authentic cultural sounds.  
  **Mitigation:** Use CC-licensed sounds, public domain resources, or create short inspired loops; document sources carefully.  
- **Risk:** Performance issues with many audio tracks/particles.  
  **Mitigation:** Limit concurrent tracks, use lightweight animations, and optimize code.  
- **Risk:** Conflict on creative direction.  
  **Mitigation:** Weekly check-ins, clear task ownership, and Linh to mediate design decisions.

---

## 13. Deliverables & Assessment Criteria
- Working interactive application with 6–8 cultural elements.  
- Short demo video (2–3 minutes).  
- Presentation slides (4–6 slides) and final documentation (README + credits).  
- Reflection on design choices and cultural research.

---

## 14. Next Steps (Immediate)
1. Share this proposal with the team and agree on roles.  
2. Kick-off meeting: confirm cultures list and assign Week 1 tasks.  
3. Create GitHub repo and push a starter branch (Lead Coder).  
4. Linh to prepare the moodboard and visual references.

---

**Appendix: Example Cultures to Consider (mix of regions & sound types)**  
- Japan (taiko/percussive rhythm)  
- Ghana (kpanlogo / percussion)  
- Vietnam (dan tranh or traditional motif)  
- India (tabla or short melodic phrase)  
- Mexico (maracas / short trumpet motif)  
- Ireland (bodhrán or fiddle motif)

---

**Contact / Questions**  
If the team wants, I can also:  
- Produce a 1-page visual timeline (Gantt-like) as a PDF.  
- Generate a short slide deck (4 slides) for presentation.  
- Draft the initial GitHub README and repo skeleton.

