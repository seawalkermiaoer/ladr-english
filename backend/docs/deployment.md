# Deployment Guide

## Overview

This document provides instructions for deploying the LADR English backend application.

## Prerequisites

- Docker and Docker Compose installed
- Environment variables configured

## Deployment Options

### Docker Deployment

1. Build the Docker images:
   ```bash
   docker-compose build
   ```

2. Start the services:
   ```bash
   docker-compose up -d
   ```

### Manual Deployment

1. Install dependencies:
   ```bash
   pip install -r requirements/prod.txt
   ```

2. Set environment variables:
   ```bash
   export WORD_DB_URL=your-database-url
   export SUPABASE_URL=your-supabase-url
   export SUPABASE_ANON_KEY=your-supabase-anon-key
   export WORD_TOKEN_SECRET=your-token-secret
   ```

3. Run the application:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## Environment Variables

The following environment variables are required:

- `WORD_DB_URL`: Database connection URL
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_ANON_KEY`: Supabase anonymous key
- `WORD_TOKEN_SECRET`: Authentication token secret

## Health Check

The application provides a health check endpoint at `/health` which returns:
```json
{
  "status": "ok"
}
```