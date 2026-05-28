# Downloading youtube videos

#installations
#pip install yt-dlp tqdm pandas openpyxl

import pandas as pd
import subprocess
import os
from tqdm import tqdm
import time
from datetime import datetime

SOBER_EXCEL = r"C:/Users/simrankhare/Desktop/dataset_links_sober.xlsx"
DRUNK_EXCEL = r"C:/Users/simrankhare/Desktop/dataset_links_drunk.xlsx"     

# Output directory on D drive because i have more space there
OUTPUT_BASE_DIR = r"D:\DIF_Videos"