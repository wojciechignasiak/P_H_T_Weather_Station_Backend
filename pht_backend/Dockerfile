
# 
FROM python:3

# 
WORKDIR /src

COPY requirements.txt /src/
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED 1

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
