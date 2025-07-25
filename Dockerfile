FROM python
LABEL maintainer="rvilla"
LABEL description="Discord bot using Ollama for AI responses"
WORKDIR /app
RUN pip install discord.py==2.5.2 ollama==0.5.1
COPY main.py .
ENTRYPOINT ["python", "main.py"]