#!/bin/bash
# For Linux/Mac: use --reload for development
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
