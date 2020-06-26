FROM python:3.8
WORKDIR /usr/app/
COPY . /usr/app/
ENV SECRET_KEY=secret_key
ENV FLASK_APP=app
ENV FLASK_ENV=development
ENV FLASK_RUN_PORT=5000
ENV FLASK_RUN_HOST=0.0.0.0
ENV URL_API=https://5ef253b225da2f0016227ebd.mockapi.io/api/v1/
ENV JWT_SECRET_KEY=secret_key
RUN python -m pip install -r requirements.txt
CMD flask run