FROM public.ecr.aws/lambda/python:3.8

# environment variables
ENV ACCESS_TOKEN=
ENV ACCESS_TOKEN_SECRET=
ENV CONSUMER_KEY=
ENV CONSUMER_SECRET=

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

CMD ["app.lambda_handler"]