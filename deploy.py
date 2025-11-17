import subprocess
import os

# Create and activate virtual environment
subprocess.run(['mkvirtualenv', '--python=/usr/bin/python3.10', 'nexussphere'], check=True)
subprocess.run(['workon', 'nexussphere'], check=True)

# Clone the repository
subprocess.run(['git', 'clone', 'https://github.com/ShedrackAmodu/NexusSphere.git'], check=True)

# Change to the project directory
os.chdir('NexusSphere')

# Install requirements
subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)

# Run migrations
subprocess.run(['python', 'manage.py', 'migrate'], check=True)

# Collect static files
subprocess.run(['python', 'manage.py', 'collectstatic', '--noinput'], check=True)

print("Deployment setup complete.")
