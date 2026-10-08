## Typical scenarios
- Updating face replacements in edited content
- Testing different face options
- Correcting visual artifacts

## Tool-call workflow
1. Prepare existing deepfake video
2. Prepare new face image
3. Specify output location
4. Call tool with all three parameters

## Parameters
**Required:**
- `input_video_path`: Path to existing deepfake (e.g., "/video/current_deepfake.mp4")
- `new_target_face_image_path`: Path to new face image (e.g., "/images/new_face.jpg")
- `output_video_path`: Path to save updated version (e.g., "/output/updated_video.mp4")

## Parameter aliases
- input/existing/current deepfake
- new/replacement/updated face
- output/result/save location

## Call examples
1. "Replace the face in this deepfake with another"
2. "Update synthetic video with better face match"
3. "Modify existing video deepfake face"
4. "Swap faces in this synthetic video"
