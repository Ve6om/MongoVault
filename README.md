# MongoVault
A lightweight, configurable Python tool for automated MongoDB backups with scheduling, filtering, compression, and cleanup.

## Features
- Scheduled backups (via cron or manual execution)
- Exclude specific databases from backups
- .tar.gz compression for reduced storage usage
- Auto-pruning to limit the number of stored backups
- .env-based configuration for flexibility

## Requirements
- Python 3.7+
- MongoDB
- Python packages:
  `pip install python-dotenv`

## Installation
1. Clone this repository:
   `git clone https://github.com/yourname/mongo-vault.git`
   `cd mongo-vault`
2. Create and activate a virtual environment (optional but recommended):
   `python3 -m venv venv`
   `source venv/bin/activate`
3. Install required Python packages:
   `pip install python-dotenv`
4. Copy the .env-example file to .env and fill in your MongoDB details:
   `cp .env-example .env`
5. Configure your preferences in the .env file (MongoDB credentials, backup directory, etc.).

## Usage
You can run the backup manually with the following command: `python3 mongo_backup.py`

## Scheduling Backups
You can schedule the backup using cron, or any other scheduler. Steps for this won't be shown.
