FROM python:3.10.4-alpine3.15

ENV PYTHONUNBUFFERED=1

RUN  apk update \
	&& apk add --no-cache gcc musl-dev postgresql-dev python3-dev libffi-dev \
	&& pip install --upgrade pip

COPY requirements/ /tmp/requirements/
RUN pip install -r /tmp/requirements/base.txt

COPY  ./ ./
CMD ["python", "library_api/manage.py", "runserver", "0.0.0.0:8000"]
