import nltk
import ssl
import os

# Fix SSL certificate issues on some systems
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

print("Downloading NLTK data...")

# Set download directory
nltk_data_dir = os.path.join(os.path.dirname(__file__), 'nltk_data')
os.makedirs(nltk_data_dir, exist_ok=True)

# Download required NLTK packages
packages = ['punkt', 'wordnet', 'stopwords', 'punkt_tab']
for package in packages:
    try:
        nltk.download(package, download_dir=nltk_data_dir, quiet=True)
        print(f"✅ Downloaded {package}")
    except Exception as e:
        print(f"⚠️ Error downloading {package}: {e}")

print("✅ NLTK setup complete!")