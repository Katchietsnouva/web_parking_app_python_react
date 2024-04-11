# app/pages/base_page.py
from flask import render_template

class BasePage:
    def __init__(self, page_controller):
        self.page_controller = page_controller

    def render_template(self, template_name, **kwargs):
        return render_template(template_name, **kwargs)
    