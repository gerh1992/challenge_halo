FROM python:3.9.16

WORKDIR /challenge_halo/

# Copy && Install python packages first to leverage docker layering capabilities
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python3" ]

CMD ["-m", "flask", "run"]
