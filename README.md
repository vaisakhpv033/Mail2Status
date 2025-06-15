# Mail2Status 📬🛠️

**Mail2Status** is a Django-based automated order tracking system that leverages LLMs to monitor email replies from warehouses and update order statuses accordingly.

## 🔧 Features

- Submit orders via a web form
- Automatically save orders to the database with initial status as `PLACED`
- Send confirmation emails to the warehouse
- Periodically monitor a connected mailbox using Celery or schedulers
- Use an LLM to parse incoming emails and extract relevant status info
- Update order statuses (e.g., `READY TO DISPATCH`, `IN TRANSIT`) based on parsed content
- Maintain a log of status updates with email metadata and LLM output

---

## ⚙️ Tech Stack

- Python 3.x
- Django 5.x
- PostgreSQL
- Celery + Redis (for task scheduling)
- Gmail API or IMAP (for reading emails)
- OpenAI / Gemini / Any LLM of choice (for parsing status from emails)

---

## 🛠️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/vaisakhpv033/Mail2Status
   cd mail2status
