## Setup

pip install user-agent-middleware

add the following to your settings file:

MIDDLEWARE_CLASSES = [
    /// ... Your middleware

    # ECOMMERCE MIDDLEWARE
    'useragent.middleware.get_user_agent_info.VisitorSiteMiddlewareClass',
]

INSTALLED_APPS = [
    ...
    'useragent',
]

run python manage.py migrate useragent