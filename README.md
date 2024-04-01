
# Campaign Organization Database Management Tool

This tool is a comprehensive Python script for managing a PostgreSQL database tailored for "Green-not-Greed" (GnG), an environmental-activist organization. It facilitates querying, managing campaigns and events, handling financial records, and engaging with member data.

## Table of Contents
- [Problem Statement](#problem-statement)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Usage](#usage)
- [Features](#features)

## Problem Statement

**Green-not-Greed** (GnG) is a local environmental-activist organization focused on raising awareness of environmental issues in regions similar in scale to Vancouver Island. With a growing need for computerized record-keeping and concerns about online data security, GnG seeks a private, in-house system to manage their campaigns, participant involvement, and financial transactions.

Their activities primarily involve public awareness campaigns in various localities, utilizing volunteers and a few salaried employees. These campaigns require efficient scheduling, participant tracking, and financial oversight. Additionally, the coordination of campaign information with their website is crucial. This tool aims to address these needs, offering a secure and efficient way to manage GnG's operations and campaign efforts.

## Installation

**Prerequisites:**
- Python 3.x
- PostgreSQL
- psycopg2 library

**Steps:**
1. Clone the repository:
   ```
   git clone https://github.com/your-repository/campaign-organization-tool.git
   ```
2. Install required Python packages:
   ```
   pip install psycopg2
   ```



## Database Setup

To set up the database with the necessary schema and some dummy data:

1. Ensure PostgreSQL is installed and running.
2. Use `pg_dump` to create the database schema and populate it with dummy data.
   - The provided `pg_dump` file contains the necessary commands to set up the database.
   - Run the following command in your PostgreSQL environment:
     ```
     psql -U [username] -d [database] -f path/to/pg_dump_file.sql
     ```
   - Replace `[username]`, `[database]`, and `path/to/pg_dump_file.sql` with your PostgreSQL username, database name, and the path to the `pg_dump` file.

```python
dbconn = psycopg2.connect("host=[hostname] user=[username] password='[password]'")
```

Replace `[hostname]`, `[username]`, and `[password]` with your actual PostgreSQL host, username, and password within `main.py`.

## Usage

Run the script from your terminal:

```bash
python campaign_management_tool.py
```

Follow the on-screen prompts to interact with the database.

## Features

### Database Connection
- Connect to PostgreSQL and handle connection errors.

### Query Execution
- Execute SQL queries with optional parameters.

### Phase 1: Preset Queries
- Execute predefined queries for campaign insights.

### Phase 2: Campaign Management
- Initialize campaigns, schedule events, enroll volunteers/members, and view campaign details.

### Phase 3: Financial Reporting
- Generate financial reports including balance, costs, and donations.

### Phase 4: Membership Management
- Browse membership history and manage campaign/member annotations.

### Phase 5: Member Engagement Dashboard
- Dashboard showing member participation in events and campaigns.

