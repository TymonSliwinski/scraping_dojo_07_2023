import os
from dotenv import load_dotenv
from logging import getLogger

logger = getLogger(__name__)

if os.path.exists('./.env'):
    load_dotenv()
    try:
        PROXY = os.getenv('PROXY') or ''
        INPUT_URL = os.getenv('INPUT_URL')
        OUTPUT_FILE = os.getenv('OUTPUT_FILE')
    except Exception as e:
        print('Necessary environmental variables do not exist: err: %s', e)
else:
    try:
        PROXY = os.environ['PROXY'] or ''
        INPUT_URL = os.environ['INPUT_URL']
        OUTPUT_FILE = os.environ['OUTPUT_FILE']
    except KeyError as e:
        print('Necessary environmental variables do not exist: err: %s', e)
