import streamlit as st
import streamlit.components.v1 as components
import base64
import os

def create_audio_player(audio_file_path, text="Audio", autoplay=False, show_clear_button=True, on_clear_callback=None):
    """Create a custom audio player with waveform visualization and enhanced controls"""
    
    # Read the audio file and encode it
    with open(audio_file_path, "rb") as f:
        audio_bytes = f.read()
        audio_b64 = base64.b64encode(audio_bytes).decode()
    
    # Get file extension
    file_ext = os.path.splitext(audio_file_path)[1][1:]  # Remove the dot
    
    # HTML for custom audio player
    audio_player_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                margin: 0;
                padding: 20px;
                background: transparent;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            }}
            
            .audio-container {{
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                border-radius: 1rem;
                padding: 1.5rem;
                border: 1px solid #404040;
                box-shadow: inset 0 1px 0 0 rgba(255,255,255,0.1), 0 4px 20px rgba(0,0,0,0.3);
                max-width: 100%;
            }}
            
            .audio-header {{
                display: flex;
                align-items: center;
                gap: 0.75rem;
                margin-bottom: 1rem;
                color: #e0e0e0;
            }}
            
            .audio-icon {{
                width: 24px;
                height: 24px;
                background: linear-gradient(135deg, #00d4ff, #0099cc);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
            }}
            
            .audio-title {{
                font-weight: 600;
                font-size: 0.95rem;
                color: #f0f0f0;
            }}
            
            .audio-controls {{
                display: flex;
                align-items: center;
                gap: 1rem;
                margin-bottom: 1rem;
            }}
            
            .control-buttons {{
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }}
            
            .clear-btn {{
                width: 36px;
                height: 36px;
                border-radius: 50%;
                border: none;
                background: linear-gradient(135deg, #ff4757, #ff3838);
                color: white;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 0.9rem;
                box-shadow: 0 2px 8px rgba(255, 71, 87, 0.3);
            }}
            
            .clear-btn:hover {{
                transform: scale(1.05);
                box-shadow: 0 4px 15px rgba(255, 71, 87, 0.4);
            }}
            
            .loading-spinner {{
                width: 20px;
                height: 20px;
                border: 2px solid #404040;
                border-top: 2px solid #00d4ff;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin-left: 0.5rem;
            }}
            
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
            
            .status-indicator {{
                color: #00d4ff;
                font-size: 0.8rem;
                margin-left: 0.5rem;
                display: flex;
                align-items: center;
                gap: 0.25rem;
            }}
            
            .play-btn {{
                width: 48px;
                height: 48px;
                border-radius: 50%;
                border: none;
                background: linear-gradient(135deg, #00d4ff, #0099cc);
                color: white;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.2rem;
                box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
            }}
            
            .play-btn:hover {{
                transform: scale(1.05);
                box-shadow: 0 6px 20px rgba(0, 212, 255, 0.4);
            }}
            
            .progress-container {{
                flex: 1;
                position: relative;
                height: 6px;
                background: #404040;
                border-radius: 3px;
                cursor: pointer;
            }}
            
            .progress-bar {{
                height: 100%;
                background: linear-gradient(90deg, #00d4ff, #0099cc);
                border-radius: 3px;
                width: 0%;
                transition: width 0.1s ease;
                box-shadow: 0 0 8px rgba(0, 212, 255, 0.5);
            }}
            
            .time-display {{
                color: #b0b0b0;
                font-size: 0.8rem;
                font-weight: 500;
                min-width: 80px;
                text-align: right;
            }}
            
            .waveform {{
                height: 60px;
                background: #2a2a2a;
                border-radius: 0.5rem;
                margin-top: 1rem;
                position: relative;
                overflow: hidden;
                border: 1px solid #404040;
            }}
            
            .wave-bars {{
                display: flex;
                align-items: center;
                height: 100%;
                padding: 0 1rem;
                gap: 2px;
            }}
            
            .wave-bar {{
                width: 3px;
                background: linear-gradient(to top, #404040, #606060);
                border-radius: 2px;
                transition: background 0.3s ease;
            }}
            
            .wave-bar.active {{
                background: linear-gradient(to top, #00d4ff, #0099cc);
                box-shadow: 0 0 6px rgba(0, 212, 255, 0.6);
            }}
        </style>
    </head>
    <body>
        <div class="audio-container">
            <div class="audio-header">
                <div class="audio-icon">🔊</div>
                <div class="audio-title">{text}</div>
            </div>
            
            <div class="audio-controls">
                <div class="control-buttons">
                    <button class="play-btn" id="playBtn">▶</button>
                    {('<button class="clear-btn" id="clearBtn" title="Clear Audio">🗑️</button>' if show_clear_button else '')}
                </div>
                <div class="progress-container" id="progressContainer">
                    <div class="progress-bar" id="progressBar"></div>
                </div>
                <div class="time-display" id="timeDisplay">0:00 / 0:00</div>
                <div class="status-indicator" id="statusIndicator"></div>
            </div>
            
            <div class="waveform">
                <div class="wave-bars" id="waveBars"></div>
            </div>
            
            <audio id="audioPlayer" style="display: none;" {"autoplay" if autoplay else ""}>
                <source src="data:audio/{file_ext};base64,{audio_b64}" type="audio/{file_ext}">
            </audio>
        </div>
        
        <script>
            const audio = document.getElementById('audioPlayer');
            const playBtn = document.getElementById('playBtn');
            const clearBtn = document.getElementById('clearBtn');
            const progressBar = document.getElementById('progressBar');
            const progressContainer = document.getElementById('progressContainer');
            const timeDisplay = document.getElementById('timeDisplay');
            const waveBars = document.getElementById('waveBars');
            const statusIndicator = document.getElementById('statusIndicator');
            
            let isPlaying = false;
            let isLoading = false;
            
            // Generate fake waveform bars
            function generateWaveform() {{
                const numBars = 80;
                waveBars.innerHTML = '';
                for (let i = 0; i < numBars; i++) {{
                    const bar = document.createElement('div');
                    bar.className = 'wave-bar';
                    const height = Math.random() * 40 + 10;
                    bar.style.height = height + 'px';
                    waveBars.appendChild(bar);
                }}
            }}
            
            // Update waveform animation
            function updateWaveform() {{
                const bars = waveBars.children;
                const progress = audio.currentTime / audio.duration;
                const activeBarIndex = Math.floor(progress * bars.length);
                
                for (let i = 0; i < bars.length; i++) {{
                    if (i <= activeBarIndex) {{
                        bars[i].classList.add('active');
                    }} else {{
                        bars[i].classList.remove('active');
                    }}
                }}
            }}
            
            // Update status indicator
            function updateStatus(message, showSpinner = false) {{
                statusIndicator.innerHTML = showSpinner ? 
                    `<div class="loading-spinner"></div> ${{message}}` : message;
            }}
            
            // Clear audio function
            function clearAudio() {{
                audio.pause();
                audio.currentTime = 0;
                playBtn.textContent = '▶';
                isPlaying = false;
                progressBar.style.width = '0%';
                updateStatus('Audio cleared');
                
                // Reset waveform
                const bars = waveBars.children;
                for (let bar of bars) {{
                    bar.classList.remove('active');
                }}
                
                // Notify parent about clear action
                if (window.parent && window.parent.postMessage) {{
                    window.parent.postMessage({{
                        type: 'audio_cleared',
                        source: 'qtranslate_audio_player'
                    }}, '*');
                }}
            }}
            
            // Format time
            function formatTime(seconds) {{
                const mins = Math.floor(seconds / 60);
                const secs = Math.floor(seconds % 60);
                return `${{mins}}:${{secs.toString().padStart(2, '0')}}`;
            }}
            
            // Play/pause toggle
            playBtn.addEventListener('click', () => {{
                if (isPlaying) {{
                    audio.pause();
                    playBtn.textContent = '▶';
                    isPlaying = false;
                    updateStatus('Paused');
                }} else {{
                    updateStatus('Playing...', false);
                    audio.play();
                    playBtn.textContent = '⏸';
                    isPlaying = true;
                }}
            }});
            
            // Clear button event listener
            if (clearBtn) {{
                clearBtn.addEventListener('click', clearAudio);
            }}
            
            // Progress bar click
            progressContainer.addEventListener('click', (e) => {{
                const rect = progressContainer.getBoundingClientRect();
                const percent = (e.clientX - rect.left) / rect.width;
                audio.currentTime = percent * audio.duration;
            }});
            
            // Audio time update
            audio.addEventListener('timeupdate', () => {{
                if (audio.duration) {{
                    const progress = (audio.currentTime / audio.duration) * 100;
                    progressBar.style.width = progress + '%';
                    timeDisplay.textContent = `${{formatTime(audio.currentTime)}} / ${{formatTime(audio.duration)}}`;
                    updateWaveform();
                }}
            }});
            
            // Audio ended
            audio.addEventListener('ended', () => {{
                playBtn.textContent = '▶';
                isPlaying = false;
                progressBar.style.width = '0%';
                updateStatus('Finished');
                
                // Reset waveform
                const bars = waveBars.children;
                for (let bar of bars) {{
                    bar.classList.remove('active');
                }}
            }});
            
            // Audio loading events
            audio.addEventListener('loadstart', () => {{
                isLoading = true;
                updateStatus('Loading audio...', true);
            }});
            
            audio.addEventListener('canplaythrough', () => {{
                isLoading = false;
                updateStatus('Ready to play');
            }});
            
            audio.addEventListener('error', () => {{
                isLoading = false;
                updateStatus('Error loading audio');
            }});
            
            // Initialize
            generateWaveform();
            updateStatus('Initializing...');
            
            audio.addEventListener('loadedmetadata', () => {{
                timeDisplay.textContent = `0:00 / ${{formatTime(audio.duration)}}`;
                updateStatus('Ready to play');
                
                // Auto-play if enabled
                if ({str(autoplay).lower()}) {{
                    setTimeout(() => {{
                        audio.play();
                        playBtn.textContent = '⏸';
                        isPlaying = true;
                        updateStatus('Auto-playing...');
                    }}, 500);
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    # Render the audio player
    components.html(audio_player_html, height=250)