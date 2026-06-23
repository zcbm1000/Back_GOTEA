from flask import Blueprint, render_template ,request, redirect, session
from utils.json_manager import load_dashboard, save_dashboard

dashboard_bp = Blueprint(
    'dashboard',
    __name__,
    url_prefix='/dashboard'
)

