from os import environ

SESSION_CONFIGS = [
    dict(
        name='sara_usa',
        display_name='SARA USA 2026',
        app_sequence=['sara'],
        num_demo_participants=1,
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc='',
)

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False
DEMO_PAGE_TITLE = 'SARA USA 2026'

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

SECRET_KEY = 'sara-usa-2026-dev-key'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD', 'admin')
