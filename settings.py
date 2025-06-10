from os import environ


SESSION_CONFIGS = [
    dict(
        name="network_pd",
        display_name="Network Public Goods Game (old)",
        num_demo_participants=12,
        app_sequence=["network_pd"],
        # use_browser_bots=True,
    ),
]
# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ["is_dropped", "app_payoffs"]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = "ja"

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = "JPY"
USE_POINTS = True

ROOMS = [
    dict(
        name="econ101",
        display_name="Econ 101 class",
        participant_label_file="_rooms/econ101.txt",
    ),
    dict(name="live_demo", display_name="Room for live demo (no participant labels)"),
]

ADMIN_USERNAME = "admin"
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get("OTREE_ADMIN_PASSWORD")

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = "6741627010810"

INSTALLED_APPS = ["otree"]

# added codes
MIDDLEWARE = ["network_pd.middleware.RequestLogMiddleware"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        # oTree から出るログを全部拾う
        "otree": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        # Channels の低レイヤーも拾いたいなら
        "channels": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}
