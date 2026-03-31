FROM python: 3.10-slim //
WORKDIR /app  //
copy ..  //
RUN pip install --no-cache-dir -r requirements.txt  //
EXPOSE 8000  //
CMD["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]  //


Building of DOCKER image:
-------------------------
docker build -t data-cleaning-env

Run container: (If using OpenAI baseline inside container)
--------------
docker run -p 8000:8000 -e OPENAI_API_KEY = your_key data-cleaning-env

Test:
-----
https://locolhost:8000/docs
