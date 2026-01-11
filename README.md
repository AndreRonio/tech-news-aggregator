# Tech News Aggregator

**Author:** Andreas Roniotis

## Description

Automated ETL pipeline that extracts top stories from the Hacker News API, transforms the data, and loads it into PostgreSQL.

## How to run (Docker)

This project runs using Docker Compose and includes two services:

* **postgres**: PostgreSQL database
* **hn\_etl**: ETL pipeline container (runs automatically via cron)

### Start the project

From the repository root (on the VM):

```bash
docker compose -f docker/docker-compose.yml up -d --build
```

### Stop the project

```bash
docker compose -f docker/docker-compose.yml down
```

### Scheduling note (Important)

For demonstration/testing purposes, the cron schedule is configured to run every minute:

```yaml
* * * * *
```

This makes it easier to verify that the pipeline is working (no need to wait 4 hours).

In a production-like scenario, the schedule can be changed to run every 4 hours, by editing docker/cron\_job.



