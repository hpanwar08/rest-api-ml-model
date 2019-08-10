import logging
import sys
import unittest
from flask.cli import FlaskGroup
import click
import coverage
from gevent.pywsgi import WSGIServer
from gevent import monkey

from project import create_app
from constants import Constants
from configuration import initialize_logger
from configuration import initialize_config


monkey.patch_all()

COV = coverage.coverage(
    branch=True,
    include="project/*",
    omit=["project/tests/*", "project/config.py"]
)
COV.start()


app = create_app()
cli = FlaskGroup(app)


@cli.command()
@click.option('--env', default='prod', help='Setup environment for dev/test/prod')
@click.argument('server_config', type=str, default='server_config.yaml')
def start(env, server_config):
    """cli function to start server in gevent
    """
    config = initialize_config(env, server_config)
    app.config.from_object(config['flask_settings'])
    initialize_logger()
    logger = logging.getLogger(Constants.MICROSERVICE_NAME)
    logger.info('Starting web server')
    try:
        http_server = WSGIServer((config['host'], config['port']), app, log=app.logger)
        click.echo('Starting web server...')
        http_server.serve_forever()
    except KeyboardInterrupt:
        click.echo('Stopping web server...')
        logger.info('Stopping web server')
        http_server.stop()


@cli.command()
def test():
    """Run the tests
    """
    tests = unittest.TestLoader().discover("project/tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)


@cli.command()
def cov():
    """Run the test with code coverage
    """
    tests = unittest.TestLoader().discover("project/tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print("Coverage Summary:")
        COV.report()
        COV.html_report()
        COV.xml_report()
        COV.erase()
        return 0
    sys.exit(result)


if __name__ == "__main__":
    cli()
