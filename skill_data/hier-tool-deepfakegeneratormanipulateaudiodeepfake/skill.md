## Typical scenarios
- Updating voice clones in production pipelines
- Experimenting with different voice options
- Correcting voice matching issues

## Tool-call workflow
1. Prepare existing deepfake audio
2. Prepare new voice sample
3. Specify output location
4. Call tool with all three parameters

## Parameters
**Required:**
- `input_audio_path`: Path to existing deepfake (e.g., "/audio/current_deepfake.wav")
- `new_target_voice_sample_path`: Path to new voice sample (e.g., "/samples/new_voice.mp3")
- `output_audio_path`: Path to save updated version (e.g., "/output/updated_audio.wav")

## Parameter aliases
- input/existing/current deepfake
- new/replacement/updated voice
- output/result/save location

## Call examples
1. "Change this synthetic voice to a different actor"
2. "Update the voice clone with better sample"
3. "Modify existing audio deepfake voice"
4. "Swap voices in this synthetic recording"
