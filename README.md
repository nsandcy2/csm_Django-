# Django CMS Tool

## 📌 Overview
This is a Django-based CMS tool with a modern **Tailwind CSS frontend**.  
It is production-ready and can be deployed to AWS with RDS (PostgreSQL/MySQL) and static files served via S3 + CloudFront.

---

## 🛠️ Installation

### 1. Clone repository
```bash
git clone https://github.com/nsandcy2/csm_Django-.git
cd Project_csm
```

### 2. Create & activate virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate    # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## ⚙️ Database Setup

Update **`settings.py`** with your database config. Example (PostgreSQL):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'yourdbname',
        'USER': 'yourdbuser',
        'PASSWORD': 'yourpassword',
        'HOST': 'your-db-host.amazonaws.com',
        'PORT': '5432',
    }
}
```

Run migrations:
```bash
python manage.py migrate
```

Create superuser:
```bash
python manage.py createsuperuser
```

---

## 🎨 Tailwind CSS Setup

For development, Tailwind is included via CDN in `base.html`.  
For **production**, build Tailwind locally:

```bash
npm init -y
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init
```

Configure `tailwind.config.js`:
```js
module.exports = {
  content: [
    "./**/templates/**/*.html",
    "./**/*.py",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Add `src/input.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Build CSS:
```bash
npx tailwindcss -i ./src/input.css -o ./static/css/tailwind.css --minify
```

Update `base.html` to load this file instead of the CDN.

---

## ▶️ Run the app

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## 🚀 Deployment (AWS)

1. Use **AWS RDS** for database.
2. Store static/media files in **S3** and serve via **CloudFront**.
3. Set environment variables securely (DB password, secret key).
4. Use **Gunicorn + Nginx** on EC2 / Elastic Beanstalk.

Collect static files before deployment:
```bash
python manage.py collectstatic
```

---

## ✅ Features
- Django backend (CMS tool)
- Tailwind CSS modern frontend
- Responsive tables & forms
- Ready for AWS deployment