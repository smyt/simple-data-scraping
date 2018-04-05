"""Views of site web pages."""
from flask import render_template, flash
from flask_rq import RQ
from flask_rq import get_queue

from app import app
from app.forms import DownloadForm
from app.messages import SUCCESSFUL_SEND_MESSAGE
from app.utils import start_task

RQ(app)


@app.route('/', methods=['GET', 'POST'])
def index_page():
    """Site main page."""
    form = DownloadForm()
    if form.validate_on_submit():
        url = form.url.data
        email = form.email.data
        type_parsing = form.type_parsing.data
        flash(SUCCESSFUL_SEND_MESSAGE)
        get_queue().enqueue(start_task, url, type_parsing, email)
    return render_template('index.html', form=form)
