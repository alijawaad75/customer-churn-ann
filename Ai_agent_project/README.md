# Swarm AI Agent

A powerful AI agent that can process multiple inputs in parallel using transformer-based models.

## Features

- Single text processing
- Parallel (swarm) processing of multiple texts
- Easy model switching
- REST API interface
- GPU support (when available)

## Installation

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server

Run the following command to start the API server:
```bash
python app.py
```

The server will start on `http://localhost:8000`

### API Endpoints

1. Process Single Text
```bash
curl -X POST "http://localhost:8000/process" \
     -H "Content-Type: application/json" \
     -d '{"text": "Your input text here"}'
```

2. Process Multiple Texts (Swarm)
```bash
curl -X POST "http://localhost:8000/swarm-process" \
     -H "Content-Type: application/json" \
     -d '{"texts": ["Text 1", "Text 2", "Text 3"]}'
```

3. Update Model
```bash
curl -X POST "http://localhost:8000/update-model?model_name=gpt2"
```

## Configuration

The default model is GPT-2, but you can change it to any model from the Hugging Face model hub. To use a different model, simply call the update-model endpoint with your desired model name.

## Requirements

- Python 3.7+
- CUDA-compatible GPU (optional, but recommended for better performance)
- See requirements.txt for full list of dependencies

## License

MIT License 