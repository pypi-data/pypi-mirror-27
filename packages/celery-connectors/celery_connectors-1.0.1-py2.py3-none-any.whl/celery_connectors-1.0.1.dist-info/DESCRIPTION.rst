For running headless celery subscribers and kombu publishers to process json or pickled messages using a celery-ready messaging backend. Headless means no task result backend (like mongo). I am planning to glue Django and Jupyter together with this connection framework, and allow workers to process messages from my windows laptop out of a shared broker.


