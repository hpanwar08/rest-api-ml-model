import sys
import unittest
from flask.cli import FlaskGroup
import coverage
from gevent import wsgi
from project import create_app

COV = coverage.coverage(
    branch=True,
    include="project/*",
    omit=["project/tests/*", "project/config.py"]
)
COV.start()


app = create_app()
cli = FlaskGroup(app)


@cli.command()
def start():
    """cli function to start server in gevent
    """
    try:
        http_server = wsgi.WSGIServer(('0.0.0.0', 5000), app)
        http_server.serve_forever()
    except KeyboardInterrupt:
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
        COV.erase()
        return 0
    sys.exit(result)


if __name__ == "__main__":
    cli()
