# ELECTION BUDDY – AI-Powered Smart Election Assistant for India 🇮🇳

## 📝 Problem Statement
During elections in India, voters often face challenges such as misinformation, complex procedures, long waiting times at booths, and lack of awareness about their rights. This can lead to voter apathy or confusion on election day.

## 💡 Solution
**Election Buddy** is a real-time AI assistant designed to bridge the information gap. It provides a one-stop platform for guidance, civic awareness, and real-time booth status, ensuring every citizen can vote safely, confidently, and informed.

## 🚀 Key Features
- **AI Chat Assistant**: Powered by Gemini 3 Flash for step-by-step guidance.
- **Voter Toolkit**: Quick actions for Eligibility, Voter Rights, and Booth Process.
- **Interactive Timeline**: Stay updated with election phases and deadlines.
- **Smart Checklist**: Personal tracker for essential documents and actions.
- **Live Booth Status**: Real-time (simulated) crowd detection and wait-time estimates.
- **Election Day SOS**: One-click access to emergency help and official helplines.
- **Civic Awareness**: Clear explanations on NOTA, Voter Rights, and the importance of voting.

## 🛠 Tech Stack
- **AI Engine**: Gemini 3 Flash (via Google Cloud Vertex AI)
- **Backend**: FastAPI (Python)
- **Database**: Google Cloud Firestore (Logs & Crowd Data)
- **Deployment**: Google Cloud Run (Backend) & Firebase Hosting (Frontend)
- **Design**: Vanilla HTML/CSS/JS with Glassmorphism and India-centric aesthetics.

## 🧠 AI Prompt Engineering
The assistant uses a structured `master_prompt.txt` that enforces:
- **Safety-First** approach for crowd management.
- **Simple English** for maximum accessibility.
- **Actionable Steps** to ensure the user knows exactly what to do next.
- **Strict Neutrality** to maintain election integrity.

## 🔒 Security & Privacy
- **No PII**: No personal identification data is stored.
- **Input Sanitization**: Backend filters all user inputs.
- **API Security**: Keys are managed via Environment Variables in Cloud Run.

## 🚀 Deployment Steps

### 1. Google Cloud Setup
```bash
# Set your project ID
gcloud config set project project-c4cd6ab1-66ee-44df-88b

# Enable required APIs
gcloud services enable aiplatform.googleapis.com run.googleapis.com firestore.googleapis.com
```

### 2. Backend Deployment (Cloud Run)
```bash
cd backend
# Build and deploy to Cloud Run
gcloud run deploy election-buddy-api --source . --region us-central1 --allow-unauthenticated
```
*Note: Copy the service URL generated after deployment.*

### 3. Frontend Deployment (Firebase)
1. Update `API_URL` in `frontend/script.js` with your Cloud Run URL.
2. Deploy:
```bash
firebase deploy --only hosting
```

## 🇮🇳 Civic Contribution
This project is built to support the democratic process in India by making election information accessible to all. 

**Helpline: 1950** | **Email: eci@eci.gov.in**
