# The Daily Thomas Edison

A Django blog application deployed as a multi-tier architecture on AWS: EC2 Auto Scaling Group behind an Application Load Balancer, RDS for MySQL (Multi-AZ), and static assets served from S3 via CloudFront.

## Architecture

- **App tier** — Django app running in Docker (Gunicorn) on EC2 instances in a private subnet, managed by an Auto Scaling Group behind an Application Load Balancer.
- **Database** — Amazon RDS for MySQL, Multi-AZ, in a private subnet, encrypted with a customer-managed KMS key. Credentials are stored in Secrets Manager and resolved at container startup.
- **Static assets** — Collected via `collectstatic`, synced to S3, and served through a CloudFront distribution at `/static/*`, which also fronts the ALB for the rest of the site.
- **Networking** — VPC with public/private subnets across two AZs, NAT instance for private-subnet egress, and a jump server for bastion SSH access.

See [cloudformation.yaml](cloudformation.yaml) for the full resource definitions.

## Project layout

```
infra/
├── src/                    # Django project (settings, urls, wsgi/asgi)
│   └── blog/                # Blog app: Topic/Comment models, views, templates
├── Dockerfile               # App container image
├── entrypoint.sh            # Resolves DB secrets, then execs the container CMD
├── resolve_secrets.py       # Pulls DB credentials from Secrets Manager
├── cloudformation.yaml      # Full AWS infrastructure (VPC, ALB, ASG, RDS, CloudFront, etc.)
├── deploy.sh                # Build/push image, deploy stack, migrate, sync static assets
├── iam-app-instance-policy.json
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Local dev dependencies (SQLite, no mysqlclient)
├── .env.example              # Environment variable reference
└── manage.py
```

## Local development

1. Create a virtualenv and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements-dev.txt
   ```

2. Copy `.env.example` to `.env` and adjust as needed. Omit `DB_ENGINE` (or leave it unset) to fall back to the local SQLite database — no MySQL setup required.

3. Run migrations and start the dev server:

   ```bash
   python manage.py migrate
   python manage.py seed_data   # optional: seed sample topics/comments
   python manage.py runserver
   ```

4. Visit `http://localhost:8000/`.

### Routes

| Path                     | Description                          |
|---------------------------|---------------------------------------|
| `/`                        | List all blog topics                  |
| `/topic/<id>/`             | View a topic and its comments         |
| `/search/?q=...`           | Search topics by name or description  |
| `/health/`                 | Health check (used by the ALB target group) |
| `/admin/`                  | Django admin                          |

## Configuration

Environment variables (see [.env.example](.env.example)):

| Variable | Purpose |
|---|---|
| `DJANGO_SECRET_KEY` | Django secret key |
| `DJANGO_DEBUG` | `True`/`False` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed hosts |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Comma-separated trusted origins for CSRF |
| `DJANGO_STATIC_URL` | Base URL for static assets (CloudFront in production) |
| `DB_ENGINE` | Set to `mysql` to use RDS; unset/omitted falls back to SQLite |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | MySQL connection settings |
| `DB_SECRET_ARN` | Secrets Manager ARN; when set, `entrypoint.sh` resolves `DB_USER`/`DB_PASSWORD` at container startup, overriding the static env values |

## Deployment

`deploy.sh` runs the full deployment sequence against AWS:

1. Builds the Docker image and pushes it to ECR, tagged with the current git short SHA.
2. Deploys/updates the CloudFormation stack (`edison-blog`) with the new image URI.
3. Runs `manage.py migrate` on an app instance via SSM.
4. Syncs `staticfiles/` to the S3 static assets bucket, matching CloudFront's `/static/*` behavior.

Requires AWS credentials with permissions for ECR, CloudFormation, SSM, and S3, plus an existing EC2 key pair (`KeyPairName`) and Route53 hosted zone for the CloudFront/ACM setup.

`test.sh` prints the SSM command to run migrations and seed data manually against the currently running app instance.

## Docker

Build and run the container locally:

```bash
docker build -t edison-blog .
docker run -p 8000:8000 --env-file .env edison-blog
```
