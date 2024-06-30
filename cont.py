import os
from random import randint, choice
from datetime import datetime, timedelta

# Hardcoded start and end dates (format: YYYY-MM-DD)
START_DATE = "2024-07-01"
END_DATE = "2024-08-20"

# Convert string dates to datetime objects
start_date = datetime.strptime(START_DATE, "%Y-%m-%d")
end_date = datetime.strptime(END_DATE, "%Y-%m-%d")

# Calculate the number of days between start and end dates
num_days = (end_date - start_date).days + 1

current_date = start_date
while current_date <= end_date:
    # Choose a batch size (7 or 10 days)
    batch_size = choice([7, 10])
    
    # Randomly decide to skip 1 or 2 days in this batch
    days_to_skip = randint(1, 2)
    skip_days = set(randint(0, batch_size-1) for _ in range(days_to_skip))
    
    for i in range(batch_size):
        if i not in skip_days and current_date <= end_date:
            for j in range(randint(1, 10)):
                commit_date = current_date.strftime("%Y-%m-%d %H:%M:%S")
                with open('file.txt', 'a') as file:
                    file.write(f"Commit on {commit_date}\n")
                os.system('git add .')
                os.system(f'git commit --date="{commit_date}" -m "commit"')
        
        current_date += timedelta(days=1)

# Push to the main branch of the origin remote
os.system('git push -u origin main')