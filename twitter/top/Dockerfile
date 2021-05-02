# set base image (host OS)
FROM public.ecr.aws/lambda/python:3.8

# environment variables
ENV ACCESS_TOKEN=
ENV ACCESS_TOKEN_SECRET=
ENV CONSUMER_KEY=
ENV CONSUMER_SECRET=

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .

# command to run on container start
CMD ["app.lambda_handler"]