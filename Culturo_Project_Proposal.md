# Culturo Project Proposal

## Project Overview
Culturo is an educational desktop application designed to introduce primary and lower secondary students to the diversity and richness of world cultures through interactive and gamified experiences. The project aims to spark curiosity, deepen cultural understanding, and foster creative learning about the traditions, arts, and customs of different countries.

## Objective
Create an engaging and accessible software that inspires young learners to explore global cultures in fun and creative ways. By combining interactivity, multimedia content, and gamification, the project encourages active participation and experiential learning.

## Target Audience
Primary and lower secondary school students (ages approximately 7–16) interested in exploring global cultures through interactive play and creative activities.

## Platform
Desktop application (Windows and macOS)

## Countries Featured
- Vietnam
- Hong Kong
- China

Each country includes four cultural aspects:
1. Animals
2. Language
3. Performing Arts
4. Food

## Core Features & Interactivity
1. **Animals**  
   Students are given reference images of animals symbolic of each country. They can draw their own versions within the app. Completing the task successfully earns 3 stars.

2. **Language**  
   Students listen to a traditional greeting from each country, then record and playback their own imitation. Correct pronunciation and rhythm earn 3 stars.

3. **Performing Arts**  
   Students watch a short clip (30 seconds to 1 minute) of a traditional performance. Afterward, they take a short quiz identifying the performance type. Correct answers earn 3 stars, while incorrect answers earn none.

4. **Food**  
   Students answer three questions about the country’s cuisine, earning 1 star for each correct response. Upon completion, a short introduction video reveals more about the food and its cultural significance.

## Scoring & Progression
- Each activity contributes to a total star score per country.
- Accumulating stars unlocks small cultural collectibles or badges.
- This system motivates exploration across all four cultural aspects.

## Design Direction
- **Visual Style:** Playful, colorful, and culturally diverse, highlighting key motifs from each country.
- **User Interface:** Intuitive layout suitable for young learners; large buttons, clear icons, minimal text.
- **Sound Design:** Incorporates ambient cultural sounds, greetings, and traditional music elements.

## Educational Value
- Develops visual creativity (drawing task).
- Enhances listening and pronunciation skills (language task).
- Promotes cultural literacy and critical thinking (quiz components).
- Provides fun, multi-sensory learning experiences.

## Tools & Technologies
- Python (using frameworks such as PyQt5 or Kivy for UI development).
- Multimedia Integration: Audio (WAV/MP3), Video (MP4), and Drawing (Canvas API equivalents).
- Optional database or JSON structure for storing user progress and star scores.

## Expected Outcome
A user-friendly, visually engaging educational desktop application that motivates students to appreciate cultural diversity through creativity, interaction, and exploration.

## Project Timeline

| Phase                  | Duration | Key Activities                                                                                   |
|------------------------|----------|------------------------------------------------------------------------------------------------|
| Planning & Research    | 3 days   | Finalize project scope and features; research cultural content; gather multimedia resources    |
| UI/UX Design           | 4 days   | Design interface mockups; prototype drawing and recording features                             |
| Core Development       | 10 days  | Develop app framework; implement multimedia playback, drawing canvas, recording, star system  |
| Content Integration    | 5 days   | Integrate country-specific data: images, greetings, videos, quiz questions                     |
| Testing & Refinement   | 3 days   | Usability testing with sample users; debug and refine UI and interactions                      |
| Finalization & Delivery| 1 week   | Package apps for Windows/macOS; prepare documentation and usage guide; submit deliverables     |

Total Duration: Approximately 4 weeks

## Technical Implementation Plan

1. **Development Environment**
   - Python as primary language for flexibility and prototyping.
   - Desktop UI Framework: PyQt5 (rich GUI) or Kivy (cross-platform, touch-friendly).

2. **Multimedia Handling**
   - Drawing: Custom drawing canvas for tracing or freehand drawing.
   - Audio: Libraries like PyAudio or PyDub for recording, playback, sound processing.
   - Video: Embed short clips (MP4) using PyQt or Kivy multimedia components.

3. **Interactive Features**
   - Drawing completion detection.
   - Recording and playback UI with feedback for pronunciation imitation.
   - Quiz system with immediate scoring and star allocation.

4. **Data Management**
   - Store content and progress data in JSON files.
   - Save user progress locally to continue sessions and view achievements.

5. **User Interface**
   - Child-friendly navigation with large buttons, minimal text, icons, and images.
   - Feedback for correct/incorrect answers, star awards, encouragement messages.

6. **Deployment**
   - Package with PyInstaller or similar for Windows and macOS distribution.
   - Provide installation guides for schools or individual users.
