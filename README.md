# Here are your Instructions

# 🎬 CineAI – AI-Powered OTT Streaming Platform

CineX is a full-stack AI-powered OTT (Over-The-Top) streaming platform that allows users to browse, stream, and discover movies with personalized recommendations.

Built with a modern scalable architecture, CineX integrates machine learning, real-time APIs, and cloud storage to deliver a seamless streaming experience.

---

## 🚀 Features

### 🎥 Streaming Platform

- Video streaming with adaptive playback
- Resume watching functionality
- Watch history tracking
- Movie details and metadata

### 🤖 AI Recommendation System

- Personalized movie recommendations
- Trending and popular content
- User behavior tracking
- ML-based suggestion engine

### 🔐 Authentication & Security

- JWT-based authentication
- Secure login & registration
- Role-based access control (RBAC)

### 📊 Backend System

- RESTful API architecture
- Scalable microservice-ready design
- Redis caching for performance
- Kafka (optional) for event streaming

### ☁️ Cloud Storage (No AWS)

- Firebase Storage integration
- Secure video upload & access
- No billing / free-tier friendly setup

---

## 🏗️ Tech Stack

### Frontend

- Next.js
- React.js
- Tailwind CSS

### Backend

- Node.js
- Express.js

### Database

- MongoDB

### Caching & Messaging

- Redis
- Kafka (optional)

### AI / ML Service

- Python (FastAPI)

### Storage

- Firebase Storage

---

## 📂 Project Structure

```
├── frontend/        # Next.js frontend
├── backend/         # Node.js API server
├── ml-service/      # AI recommendation service
├── infra/           # Docker & deployment configs
├── scripts/         # Utility scripts (seeding, processing)
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory.

```env
# App
NODE_ENV=development
PORT=3001

# Auth
JWT_SECRET=your_secret
JWT_REFRESH_SECRET=your_refresh_secret

# Database
MONGODB_URI=mongodb://localhost:27017/cinex
REDIS_URL=redis://localhost:6379

# Services
ML_SERVICE_URL=http://localhost:8001
ENABLE_KAFKA=false

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:3001/api/v1

# Firebase Storage
STORAGE_BACKEND=firebase
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
FIREBASE_CLIENT_EMAIL=your-client-email
FIREBASE_PRIVATE_KEY_B64=your_base64_key
```

---

## 🛠️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/DevOP67/OTT-Platform.git
cd OTT-Platform
```

### 2️⃣ Install Dependencies

```bash
npm install
```

### 3️⃣ Setup Environment

```bash
cp .env.example .env
```

Fill in required values.

---

### 4️⃣ Run Backend

```bash
npm run dev
```

---

### 5️⃣ Run Frontend

```bash
cd frontend
npm run dev
```

---

### 6️⃣ Run ML Service

```bash
cd ml-service
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

---

## 📡 API Endpoints

### 🔐 Auth

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`

### 🎬 Movies

- `GET /api/v1/movies`
- `GET /api/v1/movies/:id`

### 🤖 Recommendations

- `GET /api/v1/recommendations`

### 🎥 Streaming

- `GET /api/v1/stream/:id`
- `POST /api/v1/stream/:id/progress`

---

## 🎥 Video Upload Flow

1. Upload video via API
2. Stored in Firebase Storage
3. URL returned to backend
4. Stream via frontend player

---

## 🧪 Testing

```bash
npm run test
```

---

## 🚀 Deployment

### Firebase Hosting (Frontend)

```bash
firebase deploy
```

### Backend

- Deploy on Render / Railway / VPS

---

## 📌 Future Improvements

- 🎞️ HLS adaptive streaming
- 💳 Subscription system
- 📱 Mobile app support
- 📊 Advanced analytics dashboard
- 🔒 DRM protection

---

## 👨‍💻 Author

**Subho Pattanayak**

- GitHub: https://github.com/DevOP67
- LinkedIn: https://linkedin.com/in/subha-pattanayak-8a8165254

---

## ⭐ Contributing

Contributions are welcome!
Feel free to fork the repo and submit a PR.

---

## 📜 License

This project is licensed under the MIT License.
