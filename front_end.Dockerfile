FROM python:latest

WORKDIR /src
RUN pip install flask pandas validators requests dill keras numpy tensorflow
COPY *.py .
COPY templates/ templates
COPY best_model/ best_model
EXPOSE 5555
ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]

