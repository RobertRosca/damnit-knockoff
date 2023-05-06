FROM python:3.10
WORKDIR /app
COPY . .
RUN python3 -m pip install --upgrade pip wheel setuptools
RUN python3 -m pip install -e .
CMD ["uvicorn", "damnit_knockoff.api:app", "--reload"]
