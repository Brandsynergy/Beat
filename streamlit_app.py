
import streamlit as st
import librosa
import numpy as np
import tempfile
import os
st.set_page_config(
    page_title="🎵 Afrobeat & Amapiano AI Prompt Generator Pro",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# Fix white text problem
st.markdown("""
<style>
    .stTextArea textarea {
        color: black !important;
        background-color: white !important;
    }
    div[data-testid="stMarkdownContainer"] {
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)
# Set page config


# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #ff6b35;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #4ecdc4;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .prompt-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ff6b35;
        margin: 1rem 0;
    }
    .riffusion-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #4ecdc4;
        margin: 1rem 0;
    }
    .results-box {
        background-color: #1e1e1e;
        color: #00ff00;
        padding: 1rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def analyze_audio(audio_file):
    """Analyze audio file and return characteristics"""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_path = tmp_file.name

        # Load audio
        audio_data, sr = librosa.load(tmp_path, duration=60)

        # Basic analysis
        duration = len(audio_data) / sr
        tempo, beats = librosa.beat.beat_track(y=audio_data, sr=sr)

        # Feature extraction
        try:
            spectral_centroids = librosa.feature.spectral_centroid(y=audio_data, sr=sr)[0]
            spectral_centroid_mean = float(np.mean(spectral_centroids))
        except:
            spectral_centroid_mean = 1500.0

        try:
            spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_data, sr=sr)[0]
            spectral_rolloff_mean = float(np.mean(spectral_rolloff))
        except:
            spectral_rolloff_mean = 3000.0

        try:
            zero_crossing_rate = librosa.feature.zero_crossing_rate(audio_data)[0]
            zcr_mean = float(np.mean(zero_crossing_rate))
        except:
            zcr_mean = 0.1

        # Calculate beat characteristics
        tempo_float = float(tempo)

        afro_rhythm = max(0.0, min(1.0, (tempo_float - 80) / 80))
        log_drum_intensity = max(0.0, min(1.0, (spectral_rolloff_mean - 2000) / 4000))
        percussion_richness = max(0.0, min(1.0, zcr_mean * 10))
        vocal_lift = max(0.0, min(1.0, (spectral_centroid_mean - 1000) / 2000))
        danceability = max(0.0, min(1.0, (tempo_float - 100) / 60))

        # Clean up temp file
        os.unlink(tmp_path)

        return {
            'duration': duration,
            'tempo': tempo_float,
            'afro_rhythm': afro_rhythm,
            'log_drum_intensity': log_drum_intensity,
            'percussion_richness': percussion_richness,
            'vocal_lift': vocal_lift,
            'danceability': danceability
        }

    except Exception as e:
        st.error(f"Error analyzing audio: {str(e)}")
        return None

def generate_prompts(analysis):
    """Generate AI prompts based on analysis"""
    primary_genre = "Amapiano" if analysis['log_drum_intensity'] > 0.6 else "Afrobeat" if analysis['afro_rhythm'] > 0.6 else "Afrobeat/Amapiano fusion"

    # Suno prompt
    suno_prompt = f"{primary_genre}, {analysis['tempo']:.0f} BPM, bouncy West African rhythm signature {analysis['afro_rhythm']:.2f}, signature Amapiano log drum bass intensity {analysis['log_drum_intensity']:.2f}, traditional percussion layering {analysis['percussion_richness']:.2f}, vocal lift elements {analysis['vocal_lift']:.2f}, high danceability factor {analysis['danceability']:.2f}, polyrhythmic complexity, authentic African drum patterns, rolling piano melodies, jazz-influenced chord progressions, South African township vibes"

    # Riffusion prompt
    riffusion_prompt = f"{primary_genre.lower()}, {analysis['tempo']:.0f} bpm, log drum bass, west african percussion, polyrhythmic drums, bouncy rhythm, traditional african instruments, piano rolls, vocal chops, jazz chords, township house, authentic african music, dance groove"

    return suno_prompt, riffusion_prompt

# Main app
def main():
    # Header
    st.markdown('<div class="main-header">🎵 Afrobeat & Amapiano AI Prompt Generator Pro</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Professional Music Analysis for Suno AI & Riffusion</div>', unsafe_allow_html=True)

    # File upload
    st.markdown("### 📁 Upload Your Music File")
    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=['mp3', 'wav', 'flac', 'm4a', 'aac'],
        help="Upload your Afrobeat or Amapiano track for analysis"
    )

    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name}")

        # Analyze button
        if st.button("🔍 ANALYZE MUSIC", type="primary"):
            with st.spinner("🎵 Analyzing your music... This may take a moment..."):
                analysis = analyze_audio(uploaded_file)

                if analysis:
                    # Display results
                    st.markdown("### 📊 Analysis Results")

                    results_text = f"""🎵 PROFESSIONAL MUSIC ANALYSIS COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 TRACK INFORMATION:
   Duration: {analysis['duration']:.1f} seconds
   Tempo: {analysis['tempo']:.1f} BPM
   Primary Genre: {"AMAPIANO" if analysis['log_drum_intensity'] > 0.6 else "AFROBEAT" if analysis['afro_rhythm'] > 0.6 else "AFROBEAT/AMAPIANO FUSION"}

🎯 PROFESSIONAL BEAT ANALYSIS:
   Afro Rhythm Signature: {analysis['afro_rhythm']:.3f}
   Log Drum Bass Intensity: {analysis['log_drum_intensity']:.3f}
   Percussion Layer Richness: {analysis['percussion_richness']:.3f}
   Vocal Lift Elements: {analysis['vocal_lift']:.3f}
   Danceability Factor: {analysis['danceability']:.3f}

✅ ANALYSIS STATUS: COMPLETE - AI PROMPTS GENERATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

                    st.markdown(f'<div class="results-box"><pre>{results_text}</pre></div>', unsafe_allow_html=True)

                    # Generate prompts
                    suno_prompt, riffusion_prompt = generate_prompts(analysis)

                    # Display prompts side by side
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### 🎵 Suno AI Prompt")
                        st.markdown(f'<div class="prompt-box">{suno_prompt}</div>', unsafe_allow_html=True)
                        if st.button("📋 Copy Suno Prompt", key="suno"):
                            st.code(suno_prompt, language="text")
                            st.success("✅ Suno prompt ready to copy!")

                    with col2:
                        st.markdown("### 🎸 Riffusion Prompt")
                        st.markdown(f'<div class="riffusion-box">{riffusion_prompt}</div>', unsafe_allow_html=True)
                        if st.button("📋 Copy Riffusion Prompt", key="riffusion"):
                            st.code(riffusion_prompt, language="text")
                            st.success("✅ Riffusion prompt ready to copy!")

                    # Instructions
                    st.markdown("### 🚀 How to Use These Prompts")
                    st.info("""
                    **For Suno AI:**
                    1. Copy the Suno prompt above
                    2. Go to Suno AI
                    3. Paste the prompt in the description field
                    4. Generate your AI music!

                    **For Riffusion:**
                    1. Copy the Riffusion prompt above
                    2. Go to Riffusion
                    3. Paste the prompt in the text field
                    4. Generate your AI music!
                    """)

if __name__ == "__main__":
    main()
