# Sentiment Analysis Project

This project is a sentiment analysis web service built with Django, MySQL, and OpenAI GPT-4o. It allows users to input text and receive real-time sentiment analysis results.

## 🌟 Demo

Check out the live demo: [https://sa.hsingh.site/](https://sa.hsingh.site/)

## 📋 Prerequisites

- Docker
- Docker Compose

## 🚀 Installation

### 🐳 Docker
1. Clone the repository:

   ```bash
   git clone https://github.com/siinghd/sentiment-analysis.git
   cd sentiment-analysis
   ```
2. Configure `docker-compose.yml` with correct `ENV VARS`. Look [here](#configuration)
   
3. Build the Docker containers:

   ```bash
   docker-compose build # or docker compose build
   ```

4. Start the containers:

   ```bash
   docker-compose up # or docker compose up
   ```

   This will start the following services:
   - `db`: MySQL database container
   - `web`: Django web application container
   - `migrate`: Container to run database migrations (run and exit)

5. Access the web application:

   Open your web browser and visit `http://localhost:8000` to access the sentiment analysis web service.


### 🖥️ Non-Docker Setup

If you prefer to run the application without using Docker, follow these steps:

#### Prerequisites

- Python 3.8 or higher
- MySQL Server
- Pip (Python package installer)

#### Installation

1. **Set up the MySQL Database:**

   - Install MySQL on your machine.
   - Create a new database and user for the application.
   - Grant all privileges on your database to the new user.

2. **Clone the repository and enter the directory:**

   ```bash
   git clone https://github.com/siinghd/sentiment-analysis.git
   cd sentiment-analysis
   ```

3. **Install Python dependencies:**

   - Ensure `pip` is installed and then run:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the application:**

   - Copy the example environment configuration file and modify it with your settings:

   ```bash
   cp .env.example .env
   ```

   - Open the `.env` file and update it with your database credentials and other environment variables such as `OPENAI_API_KEY` and `DJANGO_SECRET_KEY`.

5. **Perform database migrations:**

   ```bash
   python manage.py migrate
   ```

6. **Run the Django development server:**

   ```bash
   python manage.py runserver # or pip install gunicorn and run :  gunicorn sentiment_analysis_project.wsgi:application --bind 127.0.0.1:8000
   ```

   This will start the server on `http://localhost:8000`.

7. **Access the web application:**

   - Open your web browser and visit `http://localhost:8000` to access the sentiment analysis web service.

#### ℹ️ Additional Notes:

- Ensure that your Python environment is correctly set up and that all dependencies listed in `requirements.txt` are installed without errors.
- Make sure your MySQL service is running and accessible by the Django application.
- Adjust the `.env` file as necessary to ensure all environment variables are correctly set for your development environment.

<h2 id="configuration">⚙️ Configuration</h2>

The project uses environment variables for configuration. You can modify the following variables in the `docker-compose.yml` file:

- `OPENAI_API_KEY`: Your OpenAI API key for sentiment analysis. Make sure to replace it with your own API key.
- `DJANGO_SECRET_KEY`: Secret key for Django. Change this to a secure value in production.
- `DB_NAME`: Name of the MySQL database.
- `DB_USER`: MySQL database user.
- `DB_PASSWORD`: MySQL database password.
- `DB_HOST`: MySQL database host (set to `db` for Docker Compose setup).
- `DB_PORT`: MySQL database port.
- `DEBUG`: Django DEBUG flag, default: `false`.

<h2 id="usage">📖 Usage</h2>

1. Open your web browser and visit `http://localhost:8000`.
2. Enter the text you want to analyze in the provided input field.
3. Click the "Analyze Sentiment" button.
4. The sentiment analysis result will be displayed on the page.

## 🏗️ Project Structure

The project has the following structure:

- `api/`: Django app containing the API views, models, serializers, and exceptions.
- `sentiment_analysis_project/`: Django project configuration files.
- `templates/`: HTML templates directory.
- `utils/`: Useful utilities
- `Dockerfile`: Dockerfile for building the web application container.
- `docker-compose.yml`: Docker Compose configuration file.
- `manage.py`: Django management script.
- `requirements.txt`: Python dependencies file.

## 📦 Dependencies

The project uses the following main dependencies:

- Django: Web framework for building the sentiment analysis web service.
- Django REST Framework: Toolkit for building RESTful APIs in Django.
- MySQL: Database for storing sentiment analysis results.
- OpenAI GPT-4o: API for performing sentiment analysis.
- Gunicorn: WSGI HTTP server for running the Django application.

For a complete list of dependencies, refer to the `requirements.txt` file.

## ☁️ AWS Deployment
For small projects, using other hosting services like Hetzner might be more cost-effective.
But if choosing AWS, here are some recommended services:

- `Amazon EKS`: Use EKS for managing Kubernetes containers. It's a scalable and secure environment.
- `Amazon ECR`: Store Docker images in a fully managed registry using ECR.
- `Amazon RDS`: Use RDS for databases. It makes setting up and scaling databases easier.
- `AWS Elastic Beanstalk`: Deploy apps quickly on Beanstalk without having to manage lots of hosting stuff manually.
- `Amazon EC2`: Run the app on EC2 virtual servers with customizable configurations.

### 🚀 Scaling & Load Balancing

`Elastic Load Balancing (ELB)`: Use ELB with Auto Scaling Groups to efficiently distribute traffic across multiple servers like EC2 instances. It can automatically scale resources based on demand.
