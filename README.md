# Koma Zmanî Kurdî (KZK) - Kurdish Language Learning Platform

Koma Zmanî Kurdî is a comprehensive Django-based web application designed to help learners master the Kurdish language. The platform features interactive lessons, vocabulary builders, grammar guides, cultural insights, and a community forum.

## Features

- **Interactive Lessons**: Structured learning paths for different proficiency levels.
- **Vocabulary Builder**: Flashcards and spaced repetition system for vocabulary acquisition.
- **Grammar Guides**: Detailed explanations of Kurdish grammar rules with examples.
- **Cultural Insights**: Articles and information about Kurdish culture, traditions, and history.
- **Community Forum**: A place for learners to ask questions, share tips, and interact with each other.
- **User Profiles**: Track progress, save favorite lessons, and manage learning goals.
- **Responsive Design**: Beautiful, mobile-friendly interface using Tailwind CSS.

## Prerequisites

- Python 3.8+
- pip (Python package installer)
- Node.js and npm (for Tailwind CSS)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd KZK_V1
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Node.js dependencies**
   ```bash
   cd static
   npm install
   cd ..
   ```

5. **Configure environment variables**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3
   ```

6. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

## Running the Development Server

```bash
python manage.py runserver
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

## Project Structure

```
KZK_V1/
├── config/             # Django project configuration
├── kzk_app/            # Main application
│   ├── templates/      # HTML templates
│   ├── static/         # Static files (CSS, JS, images)
│   └── ...
├── lessons/            # Lesson content and data
├── media/              # User-uploaded media
├── static/             # Global static files
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

## Tailwind CSS Setup

The project uses Tailwind CSS for styling. To compile changes to `static/css/styles.css`:

```bash
cd static
npm run dev  # Development mode (watches for changes)
npm run build  # Production build
```

## License

MIT License
# kzk
