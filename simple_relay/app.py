from datetime import datetime, timedelta
from logging import basicConfig, INFO, getLogger
from threading import Thread
from time import sleep

from flask import Flask


basicConfig(level=INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = getLogger(__name__)

TRIGGER_DURATION = timedelta(seconds=20)
TRIGGERED = False
UN_TRIGGER_AT = datetime.now()
GPIO_CHANNEL = 17


def init_gpio():
    global GPIO_CHANNEL
    try:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_CHANNEL, GPIO.OUT)
    except Exception:
        logger.exception("Failed to init GPIO")


def try_trigger() -> bool:
    global GPIO_CHANNEL, TRIGGERED, UN_TRIGGER_AT
    if TRIGGERED:
        logger.info("Relay already triggered")
        return False

    logger.info("Triggering relay.")
    try:
        now = datetime.now()
        UN_TRIGGER_AT = now + TRIGGER_DURATION
        logger.info("Triggered relay at %s, will un-trigger at %s", now, UN_TRIGGER_AT)
        import RPi.GPIO as GPIO
        GPIO.output(GPIO_CHANNEL, GPIO.HIGH)
        TRIGGERED = True
    except Exception:
        logger.exception("Failed to trigger relay")


def try_un_trigger():
    global GPIO_CHANNEL, TRIGGERED, UN_TRIGGER_AT
    now = datetime.now()
    if not TRIGGERED or UN_TRIGGER_AT > now:
        return

    try:
        logger.info("Un-Triggering relay at %s", now)
        import RPi.GPIO as GPIO
        GPIO.output(GPIO_CHANNEL, GPIO.LOW)
        TRIGGERED = False
    except Exception:
        logger.exception("Failed to un-trigger relay")


def create_app() -> Flask:
    app = Flask(
        __name__,
        static_url_path="",
        static_folder="web/static",
    )

    @app.route("/")
    def catch_all():
        return app.send_static_file("index.html")

    @app.route("/trigger", methods=["POST"])
    def trigger_relay():
        try_trigger()
        return app.send_static_file("index.html")

    return app


def do_monitor():
    while True:
        sleep(.1)
        try_un_trigger()


def start():
    trigger_monitor_thread = Thread(name="Trigger Monitor", daemon=True, target=do_monitor)
    trigger_monitor_thread.start()

    init_gpio()

    app = create_app()
    app.run(
        host="0.0.0.0",
        port=8080,
    )
