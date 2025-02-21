import logging
import ecs_logging

# Get the Logger
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

# Add an ECS formatter to the Handler
handler = logging.FileHandler('.logs.txt')
handler.setFormatter(ecs_logging.StdlibFormatter(exclude_fields=[
        "ecs", "function", "original", "process",
        "log.origin", "log.logger", "log.original"
    ]))
logger.addHandler(handler)

