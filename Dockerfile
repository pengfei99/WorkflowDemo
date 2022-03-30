#
FROM python:3.8-bullseye

# set api as the current work dir
WORKDIR /app

# copy the requirements lists
COPY ./requirements.txt /app/requirements.txt

# install all the requirements
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# set up python path for the added source
ENV PYTHONPATH "${PYTHONPATH}:/app"

# call the function
CMD ["python app.py"]
