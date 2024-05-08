# Sentiment Analysis Project

This project is a sentiment analysis web service built with Django, MySQL, and OpenAI GPT-3.5. It allows users to input text and receive real-time sentiment analysis results.

## Demo

https://sa.hsingh.site/

## Prerequisites

- Docker
- Docker Compose

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/siinghd/sentiment-analysis.git
   cd sentiment-analysis
   ```
2. Configure `docker-compose.yml` with correct `ENV VARS`. Look [here](#configuration)
   
3. Build the Docker containers:

   ```bash
   docker-compose build
   ```

4. Start the containers:

   ```bash
   docker-compose up
   ```

   This will start the following services:
   - `db`: MySQL database container
   - `web`: Django web application container
   - `migrate`: Container to run database migrations (run and exist)

5. Access the web application:

   Open your web browser and visit `http://localhost:8000` to access the sentiment analysis web service.

<h2 id="configuration">Configuration</h2>

The project uses environment variables for configuration. You can modify the following variables in the `docker-compose.yml` file:

- `OPENAI_API_KEY`: Your OpenAI API key for sentiment analysis. Make sure to replace it with your own API key.
- `DJANGO_SECRET_KEY`: Secret key for Django. Change this to a secure value in production.
- `DB_NAME`: Name of the MySQL database.
- `DB_USER`: MySQL database user.
- `DB_PASSWORD`: MySQL database password.
- `DB_HOST`: MySQL database host (set to `db` for Docker Compose setup).
- `DB_PORT`: MySQL database port.
- `DUBUG`: Django DEBUG flag, default: `false`.

## Usage

1. Open your web browser and visit `http://localhost:8000`.
2. Enter the text you want to analyze in the provided input field.
3. Click the "Analyze Sentiment" button.
4. The sentiment analysis result will be displayed on the page.

## Project Structure

The project has the following structure:

- `api/`: Django app containing the API views, models, serializers, and exceptions.
- `sentiment_analysis_project/`: Django project configuration files.
- `templates/`: HTML templates directory.
- `Dockerfile`: Dockerfile for building the web application container.
- `docker-compose.yml`: Docker Compose configuration file.
- `manage.py`: Django management script.
- `requirements.txt`: Python dependencies file.

## Dependencies

The project uses the following main dependencies:

- Django: Web framework for building the sentiment analysis web service.
- Django REST Framework: Toolkit for building RESTful APIs in Django.
- MySQL: Database for storing sentiment analysis results.
- OpenAI GPT-3.5: API for performing sentiment analysis.
- Gunicorn: WSGI HTTP server for running the Django application.

For a complete list of dependencies, refer to the `requirements.txt` file.

## AWS Deployment
For small projects, I think using other hosting services like Hetzner might be more cost effective. 
But if I'm choosing AWS, here is what i would use:

- `Amazon EKS`: I'll use EKS for managing Kubernetes containers. It's a scalable and secure environment.
- `Amazon ECR`: I'll use ECR for storing my Docker images in a fully managed registry.
- `Amazon RDS`: I'll use RDS for databases. It makes setting up and scaling databases easier.
- `AWS Elastic Beanstalk`: I can deploy my apps quickly on Beanstalk without having to manage lots of hosting stuff myself.
- `Amazon EC2`: I'll run my app on EC2 virtual servers with configs I pick.

_*Scaling & Load Balancing*_:

`Elastic Load Balancing (ELB)`: I'll use ELB with Auto Scaling Groups to efficiently distribute traffic across multiple servers like EC2 instances. It can automatically scale resources based on demand.