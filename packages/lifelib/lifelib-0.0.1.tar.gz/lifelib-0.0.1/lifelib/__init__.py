import os.path

VERSION = (0, 0, 1)
LIB_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(LIB_DIR, 'projects')
TEMPLATES = [f for f in os.listdir(TEMPLATE_DIR)
             if os.path.isdir(os.path.join(TEMPLATE_DIR, f))]

