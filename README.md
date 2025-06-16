# Mail2Status 📬m️⚒️

**Mail2Status** is a Django-based automated order tracking system that leverages Google Generative AI to monitor email replies from warehouses and update order statuses accordingly.

## 🔧 Features

- Create and track orders via Django admin or APIs
- Automatically send emails to the warehouse when an order is placed
- Periodically check a Gmail inbox for messages
- Use Google GenAI to parse order updates from email content
- Update order statuses automatically
- Maintain logs for each email processed

---

## ⚙️ Tech Stack

- Python 3.10+
- Django 5.x
- PostgreSQL
- Celery + Redis ([Celery Intro](https://docs.celeryq.dev/en/main/getting-started/introduction.html))
- [Google Generative AI](https://ai.google.dev/gemini-api/docs)
- Gmail API ([SimpleGmail](https://github.com/jeremyephron/simplegmail))

---

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/vaisakhpv033/Mail2Status
cd mail2status
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. PostgreSQL Setup

Update your `.env` file with your PostgreSQL credentials:

```
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
```

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Setup Redis for Celery

Install Redis and run it locally or use a cloud provider. Update your `.env`:

```
CELERY_BROKER_URL=redis://localhost:6379
```

Start the Celery worker:

```bash
celery -A mail2status worker --loglevel=info
```

### 6.1 Setup Celery Beat for Periodic Email Checks

To enable automatic periodic checking of new emails:

- Install Django Celery Beat (already included in requirements.txt)
- Apply migrations:

```bash
python manage.py migrate django_celery_beat
```

- Start the beat scheduler:

```bash
celery -A mail2status beat --loglevel=info
```

- Make sure the periodic task for checking emails is registered in your code or via Django admin.

Read more about periodic tasks in the [Celery Beat Documentation](https://docs.celeryq.dev/en/main/userguide/periodic-tasks.html)

### 7. Configure Email

Set your SMTP config in `.env`:

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

### 8. Setup Google GenAI

- Go to [Google AI Console](https://ai.google.dev/gemini-api/docs)
- Get your API key
- Add it to your `.env`:

```
GOOGLE_GENERATIVE_AI_API_KEY=your_api_key
```

### 9. Setup Gmail API Access

- Visit [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project
- Enable **Gmail API**
- Configure **OAuth consent screen**
- Create **OAuth client credentials**
- Download `credentials.json`

Refer to [SimpleGmail](https://github.com/jeremyephron/simplegmail) for detailed setup.

Place `credentials.json` in your project root and authenticate:

```bash
python
>>> from simplegmail import Gmail
>>> gmail = Gmail()
>>> gmail.connect()  # Will prompt OAuth flow
```

### 10. Run the Server

```bash
python manage.py runserver
```

---

## ✍️ Example Flow

- A new order is created in Django
- Email sent to warehouse with a `mailto:` confirmation link
- Warehouse sends a reply to the connected mailbox
- Your script reads new emails using Gmail API
- GenAI parses the email content
- Order status is updated, and the log is saved

---

## 📃 License

MIT License.

---


