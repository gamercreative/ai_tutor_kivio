# Kivio — topic → narrated lesson video

Type a topic ("derivative of MSE"), get a 13-slide narrated MP4. Fully local, no paid APIs.

**How it works:** a 4-bit Mistral-7B is constrained to a strict JSON schema of
rendering calls (`text`, `render_latex`, `plot_graph`). A dispatcher routes each
block to a hand-written Pillow slide engine (word-wrap, vertical flow layout,
LaTeX and plots rasterized via matplotlib and auto-scaled to fit). Coqui TTS
narrates each slide; MoviePy derives every slide's duration from its own audio,
so narration and visuals stay in sync.

The LLM decides *what* to show. Deterministic code decides *how*.

▶ [Demo: MSE derivative lesson](examples/demo_mse_derivative.mp4)

Status: working MVP, single developer, ~1 month. RAG grounding stubbed.
