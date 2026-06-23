import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEMBERSFILE = os.path.join(BASE_DIR, 'db', 'members.json')
DASHBOARDFILE = os.path.join(BASE_DIR, 'db', 'dashboard.json')

def load_members():
    try:
        with open(MEMBERSFILE, encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}
    
def save_members(members):
    with open(MEMBERSFILE, 'w', encoding='utf-8') as f:
        json.dump(
            members,
            f,
            ensure_ascii= False,
            indent=4
        )

def load_dashboard():
    try:
        with open(DASHBOARDFILE, encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}
    
def save_dashboard(dashboard):
    with open(DASHBOARDFILE, 'w', encoding='utf-8') as f:
        json.dump(
            dashboard,
            f,
            ensure_ascii= False,
            indent=4
        )