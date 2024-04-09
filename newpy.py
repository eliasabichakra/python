from flask import Flask, request, jsonify
from nudenet import NudeDetector
import tempfile

app = Flask(__name__)

# Initialize NudeDetector object
nude_detector = NudeDetector()

# Route to handle POST requests for nudity detection
@app.route('/detector', methods=['POST'])
def detect_nudity():
    # Check if the request contains an image file
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    # Get the image file from the request
    image_file = request.files['image']
    
    # Check if the file is empty
    if image_file.filename == '':
        return jsonify({'error': 'Empty image file provided'}), 400
    
    # Create a temporary file to save the uploaded image
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        image_file.save(temp_file.name)
        
        # Perform nudity detection
        try:
            detections = nude_detector.detect(temp_file.name)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Format the results
    results = []
    for i, detection in enumerate(detections):
        if 'class' in detection and 'score' in detection and 'box' in detection:
            result = {
                'detection_number': i + 1,
                'label': detection['class'],
                'confidence': detection['score'],
                'bounding_box': detection['box']
            }
            results.append(result)
        else:
            return jsonify({'error': 'Invalid format of detection result'}), 500
    
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)
