import os
import subprocess
import shutil
import tarfile
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_AUTH = os.getenv("MONGO_AUTH")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
BACKUP_DIR = os.getenv("BACKUP_DIR", "/backups/mongo-vault")
BACKUP_MAX = int(os.getenv("BACKUP_MAX", "30"))
EXCLUDE_COLLECTIONS = set(os.getenv("EXCLUDE_COLLECTIONS", "").split(","))

TIMESTAMP = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
TEMP_DUMP_DIR = os.path.join(BACKUP_DIR, "database_dump")
TAR_GZ_PATH = os.path.join(BACKUP_DIR, f"mongo-backup-{TIMESTAMP}.tar.gz")

os.makedirs(BACKUP_DIR, exist_ok=True)

def run_mongodump():
    """ Run the mongodump command to get the current Mongo data. """
    dump_command = [
        "mongodump",
        f"--username={MONGO_USER}",
        f"--password={MONGO_PASS}",
        f"--authenticationDatabase={MONGO_AUTH}",
        f"--host={MONGO_HOST}",
        f"--port={MONGO_PORT}",
        "--gzip",
        f"--out={TEMP_DUMP_DIR}"
    ]
    print("Executing mongodump command...")
    result = subprocess.run(dump_command, capture_output=True)
    if result.returncode != 0:
        print("Backup failed:", result.stderr.decode())
        exit(1)

def filter_excluded_collections():
    """ Remove database folders that are in the exclude list. """
    if EXCLUDE_COLLECTIONS:
        print(f"Filtering out databases: {', '.join(EXCLUDE_COLLECTIONS)}")
        for db_name in os.listdir(TEMP_DUMP_DIR):
            db_path = os.path.join(TEMP_DUMP_DIR, db_name)
            if os.path.isdir(db_path) and db_name in EXCLUDE_COLLECTIONS:
                print(f"Ignoring excluded database: {db_name}")
                shutil.rmtree(db_path)

def compress_backup():
    """ Compress the remaining dump directory into a compressed file. """
    print(f"Compressing to {TAR_GZ_PATH}...")
    with tarfile.open(TAR_GZ_PATH, "w:gz") as tar:
        tar.add(TEMP_DUMP_DIR, arcname=os.path.basename(TEMP_DUMP_DIR))
    
def clean_up_temp_folder():
    """ Remove temporary dump directory """
    shutil.rmtree(TEMP_DUMP_DIR)

def prune_old_backups():
    """ Delete the oldest backup file, if the max backup amount is reached. """
    print("Pruning old backups...")
    backups = sorted(
        [f for f in os.listdir(BACKUP_DIR) if f.endswith(".tar.gz")],
        key=lambda f: os.path.getctime(os.path.join(BACKUP_DIR, f))
    )
    while len(backups) > BACKUP_MAX:
        oldest = backups.pop(0)
        os.remove(os.path.join(BACKUP_DIR, oldest))
        print(f"Deleted old backup: {oldest}")

def main():
    run_mongodump()
    filter_excluded_collections()
    compress_backup()
    clean_up_temp_folder()
    prune_old_backups()
    print("Backup operation has completed!")

if __name__ == "__main__":
    main()