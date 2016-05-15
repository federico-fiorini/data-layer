# Create virtual env
virtualenv --no-site-packages --distribute .env

# Activate env
source .env/bin/activate

# Install requirements
pip install -r requirements.txt