## Typical scenarios
- Voice cloning for dubbing or localization
- Creating synthetic voiceovers
- Audio content generation for creative projects

## Tool-call workflow
1. Prepare source audio file
2. Prepare target voice sample
3. Specify output location
4. Call tool with all three parameters

## Parameters
**Required:**
- `source_audio_path`: Path to original audio (e.g., "/audio/speech.wav")
- `target_voice_sample_path`: Path to voice sample to clone (e.g., "/samples/celebrity.mp3")
- `output_audio_path`: Path to save result (e.g., "/output/deepfake_audio.wav")

## Parameter aliases
- source/original/input audio
- target/destination/voice to clone
- output/result/save location

## Call examples
1. "Clone my voice onto this podcast recording"
2. "Generate audio deepfake using celebrity sample"
3. "Create synthetic voiceover for this narration"
4. "Make this speech sound like a different person"
