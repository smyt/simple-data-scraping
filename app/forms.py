"""Project forms."""
from flask_wtf import FlaskForm
from wtforms import validators, SelectField, StringField, ValidationError
from wtforms.fields.html5 import EmailField


class DownloadForm(FlaskForm):
    """Form for input user's data."""

    CHOICES_TYPE_PARCING = (
        ('html', 'Html'),
        ('sitemap', 'Sitemap')
    )
    email = EmailField('E-mail address', [validators.DataRequired(), validators.Email()])
    url = StringField('Url', [validators.DataRequired()])
    type_parsing = SelectField('Parsing type', choices=CHOICES_TYPE_PARCING, default=CHOICES_TYPE_PARCING[1][0])

    def validate_url(self, field):
        """Validate url for require len."""
        from urllib.parse import urlparse
        url_ob = urlparse(field.data)
        url_parts = [part for part in url_ob.path.split('/') if part]
        if len(url_parts) != 3:
            raise ValidationError('Wrong url. Please, see example')
