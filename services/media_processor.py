import os
import tempfile
from typing import Dict, Any, Optional, List
import speech_recognition as sr
import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)

# Try to import optional libraries
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    logger.warning("pydub not available. Some audio formats may not work.")

try:
    import ffmpeg
    FFMPEG_AVAILABLE = True
except ImportError:
    FFMPEG_AVAILABLE = False
    logger.warning("ffmpeg-python not available. Video audio extraction will be limited.")

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    logger.warning("mediapipe not available. Advanced body language analysis will be limited.")


class MediaProcessor:
    """Service for processing audio and video files"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Adjust recognition settings for better accuracy
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        
        # Initialize MediaPipe if available
        if MEDIAPIPE_AVAILABLE:
            self.mp_pose = mp.solutions.pose
            self.mp_face_mesh = mp.solutions.face_mesh
            self.mp_hands = mp.solutions.hands
    
    def transcribe_audio(self, audio_file) -> str:
        """Transcribe audio file to text using speech recognition"""
        temp_wav_path = None
        temp_original_path = None
        
        try:
            # Get original filename
            original_filename = getattr(audio_file, 'name', 'audio.mp3')
            file_extension = os.path.splitext(original_filename)[1].lower()
            
            # Save uploaded file to temp location
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
                audio_file.seek(0)
                tmp_file.write(audio_file.read())
                temp_original_path = tmp_file.name
            
            logger.info(f"Processing audio file: {original_filename}")
            
            # Convert to WAV if needed
            if file_extension != '.wav':
                if not PYDUB_AVAILABLE:
                    return f"Audio format conversion requires pydub library.\n\nPlease install: pip install pydub\n\nFor now, please convert your audio to WAV format."
                
                temp_wav_path = self._convert_to_wav(temp_original_path, file_extension)
            else:
                temp_wav_path = temp_original_path
            
            # Transcribe using speech recognition
            with sr.AudioFile(temp_wav_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio_data = self.recognizer.record(source)
                
                # Try Google Speech Recognition
                try:
                    transcript = self.recognizer.recognize_google(audio_data)
                    logger.info(f"Transcription successful: {len(transcript)} characters")
                    return transcript
                except sr.UnknownValueError:
                    logger.warning("Could not understand audio")
                    return "I couldn't understand the audio clearly. Please ensure:\n• Clear speech\n• Minimal background noise\n• Good microphone quality\n• Speak at moderate pace"
                except sr.RequestError as e:
                    logger.error(f"Speech recognition service error: {str(e)}")
                    return f"Speech recognition service unavailable: {str(e)}\n\nPlease check your internet connection and try again."
        
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            return f"Error processing audio file: {str(e)}\n\nPlease ensure the audio file is valid and not corrupted."
        
        finally:
            # Clean up temp files
            if temp_original_path and os.path.exists(temp_original_path):
                try:
                    os.unlink(temp_original_path)
                except:
                    pass
            if temp_wav_path and temp_wav_path != temp_original_path and os.path.exists(temp_wav_path):
                try:
                    os.unlink(temp_wav_path)
                except:
                    pass
    
    def _convert_to_wav(self, input_path: str, file_extension: str) -> str:
        """Convert audio file to WAV format"""
        try:
            logger.info(f"Converting {file_extension} to WAV")
            
            # Determine format
            format_map = {
                '.mp3': 'mp3',
                '.m4a': 'mp4',
                '.ogg': 'ogg',
                '.flac': 'flac',
                '.aac': 'aac'
            }
            
            audio_format = format_map.get(file_extension, file_extension[1:])
            
            # Load audio file
            audio = AudioSegment.from_file(input_path, format=audio_format)
            
            # Convert to mono and set sample rate
            audio = audio.set_channels(1)
            audio = audio.set_frame_rate(16000)
            
            # Export as WAV
            temp_wav_path = tempfile.NamedTemporaryFile(delete=False, suffix='.wav').name
            audio.export(temp_wav_path, format='wav')
            
            logger.info(f"Conversion successful: {temp_wav_path}")
            return temp_wav_path
        
        except Exception as e:
            logger.error(f"Error converting audio: {str(e)}")
            raise Exception(f"Failed to convert audio file. Error: {str(e)}")
    
    def analyze_video(self, video_file) -> Dict[str, Any]:
        """Analyze video for body language and extract audio"""
        temp_video_path = None
        
        try:
            # Get original filename
            original_filename = getattr(video_file, 'name', 'video.mp4')
            file_extension = os.path.splitext(original_filename)[1].lower()
            
            # Save uploaded file to temp location
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
                video_file.seek(0)
                tmp_file.write(video_file.read())
                temp_video_path = tmp_file.name
            
            logger.info(f"Processing video file: {original_filename}")
            
            # Extract frames for body language analysis
            body_language_data = self._analyze_body_language_mediapipe(temp_video_path)
            
            # Extract and transcribe audio from video
            transcript = self._extract_and_transcribe_video_audio(temp_video_path)
            
            return {
                "transcript": transcript,
                "body_language": body_language_data
            }
        
        except Exception as e:
            logger.error(f"Error analyzing video: {str(e)}")
            return {
                "transcript": f"Error processing video file: {str(e)}",
                "body_language": {
                    "posture": "Unable to analyze",
                    "facial_expressions": "Unable to analyze",
                    "gestures": "Unable to analyze",
                    "error": str(e)
                }
            }
        
        finally:
            # Clean up temp files
            if temp_video_path and os.path.exists(temp_video_path):
                try:
                    os.unlink(temp_video_path)
                except:
                    pass
    
    def _analyze_body_language_mediapipe(self, video_path: str) -> Dict[str, Any]:
        """Analyze body language using MediaPipe"""
        if not MEDIAPIPE_AVAILABLE:
            return self._analyze_body_language_basic(video_path)
        
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise Exception("Could not open video file")
            
            # Get video properties
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            duration = frame_count / fps if fps > 0 else 0
            
            # Initialize MediaPipe
            pose = self.mp_pose.Pose(
                static_image_mode=False,
                model_complexity=1,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            
            face_mesh = self.mp_face_mesh.FaceMesh(
                static_image_mode=False,
                max_num_faces=1,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            
            hands = self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=2,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            
            # Analysis metrics
            posture_scores = []
            eye_contact_scores = []
            hand_gesture_counts = []
            slouch_count = 0
            good_posture_count = 0
            frames_analyzed = 0
            
            # Sample frames (analyze every second)
            frame_interval = max(1, fps)
            
            for frame_idx in range(0, frame_count, frame_interval):
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()
                
                if not ret:
                    continue
                
                # Convert BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Process pose
                pose_results = pose.process(rgb_frame)
                face_results = face_mesh.process(rgb_frame)
                hands_results = hands.process(rgb_frame)
                
                # Analyze posture
                if pose_results.pose_landmarks:
                    posture_score = self._analyze_posture(pose_results.pose_landmarks)
                    posture_scores.append(posture_score)
                    
                    if posture_score >= 70:
                        good_posture_count += 1
                    else:
                        slouch_count += 1
                
                # Analyze face (eye contact simulation)
                if face_results.multi_face_landmarks:
                    eye_contact_score = self._analyze_face_direction(face_results.multi_face_landmarks[0])
                    eye_contact_scores.append(eye_contact_score)
                
                # Count hand gestures
                if hands_results.multi_hand_landmarks:
                    hand_gesture_counts.append(len(hands_results.multi_hand_landmarks))
                else:
                    hand_gesture_counts.append(0)
                
                frames_analyzed += 1
                
                if frames_analyzed >= 30:  # Analyze max 30 frames
                    break
            
            cap.release()
            pose.close()
            face_mesh.close()
            hands.close()
            
            # Calculate scores and feedback
            avg_posture = np.mean(posture_scores) if posture_scores else 50
            avg_eye_contact = np.mean(eye_contact_scores) if eye_contact_scores else 50
            avg_gestures = np.mean(hand_gesture_counts) if hand_gesture_counts else 0
            
            # Generate detailed feedback
            posture_feedback = self._generate_posture_feedback(avg_posture, slouch_count, good_posture_count)
            eye_contact_feedback = self._generate_eye_contact_feedback(avg_eye_contact)
            gesture_feedback = self._generate_gesture_feedback(avg_gestures, frames_analyzed)
            
            # Calculate overall body language score
            body_language_score = (avg_posture * 0.4 + avg_eye_contact * 0.35 + min(avg_gestures * 10, 100) * 0.25)
            
            analysis = {
                "duration_seconds": round(duration, 1),
                "frames_analyzed": frames_analyzed,
                "posture_score": round(avg_posture, 1),
                "eye_contact_score": round(avg_eye_contact, 1),
                "gesture_score": round(min(avg_gestures * 10, 100), 1),
                "body_language_score": round(body_language_score, 1),
                "posture": posture_feedback,
                "facial_expressions": eye_contact_feedback,
                "gestures": gesture_feedback,
                "overall_presence": self._generate_overall_feedback(body_language_score, duration)
            }
            
            logger.info(f"MediaPipe analysis complete: Score {body_language_score:.1f}, {frames_analyzed} frames")
            return analysis
        
        except Exception as e:
            logger.error(f"Error in MediaPipe body language analysis: {str(e)}")
            return self._analyze_body_language_basic(video_path)
    
    def _analyze_posture(self, landmarks) -> float:
        """Analyze posture from pose landmarks"""
        try:
            # Get key points
            left_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_hip = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_HIP]
            nose = landmarks.landmark[self.mp_pose.PoseLandmark.NOSE]
            
            # Calculate shoulder alignment (should be level)
            shoulder_diff = abs(left_shoulder.y - right_shoulder.y)
            shoulder_score = max(0, 100 - (shoulder_diff * 500))
            
            # Calculate spine alignment (shoulders should be above hips)
            avg_shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
            avg_hip_y = (left_hip.y + right_hip.y) / 2
            spine_alignment = avg_hip_y - avg_shoulder_y
            
            if spine_alignment > 0.15:  # Good upright posture
                spine_score = 100
            elif spine_alignment > 0.1:  # Acceptable
                spine_score = 75
            elif spine_alignment > 0.05:  # Slight slouch
                spine_score = 50
            else:  # Poor posture
                spine_score = 25
            
            # Calculate head position (should be aligned with spine)
            head_forward = abs(nose.z - left_shoulder.z)
            head_score = max(0, 100 - (head_forward * 300))
            
            # Overall posture score
            posture_score = (shoulder_score * 0.3 + spine_score * 0.5 + head_score * 0.2)
            return max(0, min(100, posture_score))
        
        except Exception as e:
            logger.error(f"Error analyzing posture: {str(e)}")
            return 50
    
    def _analyze_face_direction(self, face_landmarks) -> float:
        """Analyze if person is looking at camera (eye contact simulation)"""
        try:
            # Get face orientation landmarks
            # This is a simplified version - checks if face is generally forward-facing
            nose_tip = face_landmarks.landmark[1]
            left_eye = face_landmarks.landmark[33]
            right_eye = face_landmarks.landmark[263]
            
            # Calculate face symmetry (indicator of forward gaze)
            eye_diff = abs(left_eye.x - right_eye.x)
            
            # Good eye contact if face is relatively symmetric and centered
            if eye_diff > 0.1 and nose_tip.z > -0.1:
                return 85  # Good eye contact
            elif eye_diff > 0.08:
                return 70  # Acceptable
            elif eye_diff > 0.05:
                return 55  # Needs improvement
            else:
                return 40  # Poor eye contact
        
        except Exception as e:
            logger.error(f"Error analyzing face direction: {str(e)}")
            return 50
    
    def _generate_posture_feedback(self, score: float, slouch_count: int, good_count: int) -> str:
        """Generate posture feedback"""
        total = slouch_count + good_count
        slouch_pct = (slouch_count / total * 100) if total > 0 else 0
        
        if score >= 80:
            return f"Excellent posture maintained throughout! ({good_count}/{total} frames with good posture)"
        elif score >= 65:
            return f"Good overall posture. Minor adjustments: Keep shoulders level and spine straight. ({slouch_pct:.0f}% of time showed slight slouching)"
        elif score >= 50:
            return f"Posture needs improvement. You slouched {slouch_pct:.0f}% of the time. Sit up straighter and keep shoulders back."
        else:
            return f"Poor posture detected. Slouching was observed {slouch_pct:.0f}% of the time. Maintain upright position with shoulders back and spine straight."
    
    def _generate_eye_contact_feedback(self, score: float) -> str:
        """Generate eye contact feedback"""
        if score >= 75:
            return "Excellent eye contact maintained with camera. Shows confidence and engagement."
        elif score >= 60:
            return "Good eye contact overall. Try to look directly at the camera more consistently."
        elif score >= 45:
            return "Eye contact needs improvement. Look at the camera more frequently to show engagement."
        else:
            return "Poor eye contact detected. Make sure to look directly at the camera regularly to establish connection."
    
    def _generate_gesture_feedback(self, avg_gestures: float, frames: int) -> str:
        """Generate hand gesture feedback"""
        if avg_gestures >= 1.5:
            return f"Great use of hand gestures! Detected natural movements in {avg_gestures:.1f} gestures per frame on average."
        elif avg_gestures >= 0.8:
            return f"Good use of hand gestures. Consider using slightly more expressive movements to emphasize points."
        elif avg_gestures >= 0.3:
            return f"Limited hand gestures detected. Use your hands more naturally to emphasize key points."
        else:
            return "Very few hand gestures observed. Try to be more expressive with natural hand movements."
    
    def _generate_overall_feedback(self, score: float, duration: float) -> str:
        """Generate overall presence feedback"""
        if score >= 80:
            return f"Outstanding professional presence! ({duration:.1f}s video) You demonstrated excellent body language throughout."
        elif score >= 65:
            return f"Good professional presence overall ({duration:.1f}s video). Minor improvements in posture and eye contact would enhance your performance."
        elif score >= 50:
            return f"Acceptable presence ({duration:.1f}s video), but noticeable areas for improvement in body language and engagement."
        else:
            return f"Body language needs significant improvement ({duration:.1f}s video). Focus on posture, eye contact, and natural gestures."
    
    def _analyze_body_language_basic(self, video_path: str) -> Dict[str, Any]:
        """Basic fallback analysis without MediaPipe"""
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                raise Exception("Could not open video file")
            
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            duration = frame_count / fps if fps > 0 else 0
            
            cap.release()
            
            return {
                "duration_seconds": round(duration, 1),
                "total_frames": frame_count,
                "posture": "MediaPipe not available. Install for detailed analysis: pip install mediapipe",
                "facial_expressions": "Advanced analysis requires MediaPipe library.",
                "gestures": "Install MediaPipe for hand gesture tracking.",
                "overall_presence": f"Video duration: {duration:.1f}s. Install MediaPipe for AI-powered body language analysis."
            }
        
        except Exception as e:
            logger.error(f"Error in basic body language analysis: {str(e)}")
            return {
                "posture": "Unable to analyze",
                "facial_expressions": "Unable to analyze",
                "gestures": "Unable to analyze",
                "error": str(e)
            }
    
    def _extract_and_transcribe_video_audio(self, video_path: str) -> str:
        """Extract audio from video and transcribe using ffmpeg"""
        temp_audio_path = None
        
        try:
            if not FFMPEG_AVAILABLE:
                return "Video audio transcription requires ffmpeg-python library.\n\nPlease install: pip install ffmpeg-python\n\nFor now, please use Audio mode to upload audio separately."
            
            logger.info("Extracting audio from video using ffmpeg")
            
            # Create temporary audio file path
            temp_audio_path = tempfile.NamedTemporaryFile(delete=False, suffix='.wav').name
            
            # Extract audio using ffmpeg-python
            try:
                (
                    ffmpeg
                    .input(video_path)
                    .output(temp_audio_path, acodec='pcm_s16le', ac=1, ar='16000')
                    .overwrite_output()
                    .run(capture_stdout=True, capture_stderr=True, quiet=True)
                )
                
                logger.info(f"Audio extracted successfully to: {temp_audio_path}")
                
            except ffmpeg.Error as e:
                error_message = e.stderr.decode() if e.stderr else str(e)
                logger.error(f"FFmpeg extraction error: {error_message}")
                
                if 'does not contain any stream' in error_message or 'No audio' in error_message:
                    return "No audio track found in video. Please ensure your video recording includes audio."
                
                return f"Error extracting audio from video.\nPlease try uploading audio separately using Audio mode."
            
            # Check if audio file was created
            if not os.path.exists(temp_audio_path) or os.path.getsize(temp_audio_path) == 0:
                return "No audio track found in video. Please ensure your video has audio."
            
            # Transcribe the extracted audio
            with sr.AudioFile(temp_audio_path) as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio_data = self.recognizer.record(source)
                
                try:
                    transcript = self.recognizer.recognize_google(audio_data)
                    logger.info(f"Video audio transcription successful: {len(transcript)} characters")
                    return transcript
                except sr.UnknownValueError:
                    return "Could not understand the audio from video. Please ensure:\n• Clear speech\n• Minimal background noise\n• Good audio quality in video"
                except sr.RequestError as e:
                    return f"Speech recognition service error: {str(e)}\n\nPlease check your internet connection."
        
        except Exception as e:
            logger.error(f"Error extracting video audio: {str(e)}")
            return f"Error processing video audio: {str(e)}\n\nPlease try uploading audio separately using Audio mode."
        
        finally:
            if temp_audio_path and os.path.exists(temp_audio_path):
                try:
                    os.unlink(temp_audio_path)
                except:
                    pass
    
    def validate_file_size(self, file, max_size_mb: int) -> bool:
        """Validate file size"""
        try:
            file.seek(0, 2)
            size_mb = file.tell() / (1024 * 1024)
            file.seek(0)
            return size_mb <= max_size_mb
        except Exception as e:
            logger.error(f"Error validating file size: {str(e)}")
            return False
    
    def validate_file_format(self, filename: str, allowed_formats: list) -> bool:
        """Validate file format"""
        return any(filename.lower().endswith(fmt) for fmt in allowed_formats)