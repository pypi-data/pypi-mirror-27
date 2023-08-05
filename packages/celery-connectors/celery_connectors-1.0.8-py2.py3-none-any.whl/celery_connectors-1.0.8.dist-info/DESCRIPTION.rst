Running headless Celery bootsteps to process json or pickled messages from Redis, RabbitMQ or AWS SQS. Includes Kombu message processors with relay publish-hook support for pub-sub or auto-caching functionality. Also has a Kombu Publisher with docker RabbitMQ and Redis containers too. For background, headless means no task result backend (like mongo). I am planning to glue Django and Jupyter together with this connection framework, and allow workers to process messages from my windows laptop out of a shared broker.


