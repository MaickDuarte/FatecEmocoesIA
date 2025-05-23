#!/bin/bash
exec uvicorn apiEmocoes:app --host 0.0.0.0 --port $PORT
