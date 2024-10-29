# MoodSync: An Emotionally Intelligent Chatbot with Music Recommendations

## Demo Video
- URL : https://drive.google.com/file/d/1rwoXDIw-GRuiA1JCfjIpRR6w13BqHhgI/view?usp=drive_link

## Setup Instructions

### Front-end
- **Technology**: React.js
- **Steps**:
  ```bash
  # Ensure Node.js is installed on your system.
  cd frontend/
  npm install
  npm start # Starts the React application on the default port.
  ```

### Middle-end
- **Technology**: Flask
- **Steps**:
  ```bash
  cd frontend/api/
  pip install -r requirements.txt
  python app.py # Runs the Flask application.
  ```

### Back-end
- **Technologies**: Keras, TensorFlow
- **Steps**:
  ```bash
  # Use Python 3.5.2 in a virtual environment for compatibility.
  cd backend/
  pip install -r requirements.txt -r requirements-local.txt
  python tools/fetch.py # Fetch the pre-trained model.
  python tools/train.py # Optionally train the model.
  python bin/cakechat_server.py # Start the chatbot server.
  ```

### Docker Implementation (Alternative for Back-end Execution)
- **Steps**:
  Consider using Docker to containerize and manage the application components seamlessly.

## Note
- It's recommended to run each part of the project on different ports to avoid conflicts. Ensure all parts are correctly configured and running on specified ports for full functionality.
```
