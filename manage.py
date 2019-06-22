import sys
import unittest
from flask.cli import FlaskGroup
import coverage
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
def test():
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
