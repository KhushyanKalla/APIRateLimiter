API Rate Limiter & Analytics SaaS

A production-grade backend service that lets developers protect their own APIs with rate limiting, API key management, and usage analytics. Built end-to-end as a hands-on backend portfolio project — covering async database access, JWT authentication, Redis-based rate limiting, background task processing, database migrations, and cloud deployment.

Live demo: https://apiratelimiter-bpes.onrender.com/

Note: hosted on Render's free tier, so the first request after inactivity may take 30–60 seconds while the service wakes up.

What it does

Any developer with their own API can use this platform to:

Register their API as a project
Generate secure API keys for it
Distribute those keys to their own consumers
Automatically enforce tier-based rate limits (e.g. 1,000 requests/month on the free tier)
View usage analytics — who's hitting their API, how often, and when

Think of it as a lightweight, self-hosted version of the rate-limiting layer that platforms like Stripe or OpenAI put in front of their own APIs — except here, you are the platform, and other developers are your users.

Tech Stack
Layer	Technology
Backend framework	FastAPI
ORM	SQLAlchemy 2.0 (async)
Database	PostgreSQL
Caching / Rate limiting	Redis
Auth	JWT (python-jose), bcrypt password hashing
Migrations	Alembic
Testing	Pytest
Containerization	Docker
Deployment	Render
Architecture Highlights
Async SQLAlchemy throughout — non-blocking DB access via asyncpg, so the app can handle concurrent requests efficiently.
Two-tier hashing strategy — bcrypt for user passwords (intentionally slow, resists brute-force), but SHA-256 for API keys. API keys are verified on every single request through the rate limiter, so a slow hash there would become a bottleneck; SHA-256 keeps verification fast while the key itself (a long random token) provides the actual security.
Redis-backed rate limiting — atomic INCR + EXPIRE per API key per billing window, avoiding race conditions under concurrent load without needing a cron job to reset counts.
Background analytics logging — each request is logged to Postgres asynchronously after the response is sent, so logging never adds latency to the client-facing request.
Raw-key-once pattern — like GitHub Personal Access Tokens, the raw API key is shown exactly once at generation time. Only its hash is ever persisted, so even a database leak doesn't expose usable keys.
Layered structure — models/ (DB tables) → schemas/ (request/response validation) → crud/ (DB operations) → routers/ (HTTP endpoints), keeping each concern isolated and testable.
Core Entities
Entity	Purpose
User	A platform account — the developer using this SaaS
Api	A registered API project belonging to a user
ApiKey	A generated key tied to an Api, used for rate-limited access
RequestLog	An immutable record of each request made with a given key

Relationships: User 1—N Api 1—N ApiKey 1—N RequestLog

API Overview
Endpoint	Method	Purpose
/auth/signup	POST	Create a new account
/auth/login	POST	Log in, receive a JWT
/apis/	POST	Register a new API
/apis/	GET	List your registered APIs
/apis/{api_id}/keys/	POST	Generate a new API key (raw key shown once)
/analytics/key/{api_key_id}/count	GET	Total request count for a given key

Full interactive docs available at /docs (Swagger UI) once running.

Getting Started (Local)
bash
# Clone and set up
git clone https://github.com/KhushyanKalla/APIRateLimiter.git
cd APIRateLimiter
python -m venv env
env\Scripts\activate      # Windows
pip install -r requirements.txt

# Configure environment — create a .env file:
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Run migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload

Visit http://127.0.0.1:8000 for the dashboard, or http://127.0.0.1:8000/docs for the API docs.

Running with Docker
bash
docker-compose up --build

Spins up the app, PostgreSQL, and Redis together. Update .env to point DATABASE_URL/REDIS_URL at the db/redis service names instead of localhost when running this way.

Running tests
bash
pytest tests/
How Rate Limiting Works
A request arrives with an X-API-Key header.
The middleware hashes the raw key (SHA-256) and looks up the matching ApiKey record.
If valid, Redis increments a counter for that key (INCR), with a TTL set on first use (EXPIRE) so the counter automatically resets at the end of the billing window — no scheduled job needed.
If the count exceeds the tier limit, the request is rejected with 429 Too Many Requests.
Otherwise, the request proceeds, and a background task logs it to Postgres for analytics — without blocking the response.
Project Status

Core auth, API/key management, Redis-backed rate limiting, and basic analytics are implemented and verified end-to-end, including live deployment.

Future Enhancements
Email verification — confirm real email ownership at signup before activating an account
Google OAuth sign-in — login without a password, using Google's OAuth2 flow
Automatic API key expiry — optional TTL on keys, in addition to manual revocation
Key listing & revocation UI — view all keys for an API and deactivate individual ones from the dashboard
Paid tier billing — Stripe integration for unlimited-tier subscriptions
Per-endpoint rate limits — finer-grained limits instead of per-key-only
Author

Built by Khushyan Kalla — a 2026 Computer Engineering graduate, as a hands-on backend portfolio project covering the full lifecycle: system design, implementation, testing, and deployment.
