from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from swarm_agent import SwarmAgent
import uvicorn


app = FastAPI(title="Swarm AI Agent API")
agent = SwarmAgent()


class TextInput(BaseModel):
    text: str


class BatchInput(BaseModel):
    texts: List[str]


@app.post("/process")
async def process_text(input_data: TextInput):
    """
    Process a single text input.
    """
    try:
        response = agent.process_input(input_data.text)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/swarm-process")
async def swarm_process(input_data: BatchInput):
    """
    Process multiple texts in parallel.
    """
    try:
        responses = agent.swarm_process(input_data.texts)
        return {"responses": responses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/update-model")
async def update_model(model_name: str):
    """
    Update the model being used.
    """
    try:
        agent.update_model(model_name)
        return {"status": "Model updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 