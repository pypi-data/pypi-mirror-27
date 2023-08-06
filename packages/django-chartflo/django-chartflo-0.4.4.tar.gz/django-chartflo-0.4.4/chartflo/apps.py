from __future__ import unicode_literals
import importlib
from goerr import err
from django.apps import AppConfig
from chartflo.engine import ChartFlo


GENERATORS = {}
cf = ChartFlo()


def load_generator(modname, subgenerator=None):
    try:
        path = modname + ".chartflo"
        if subgenerator is not None:
            path = path + "." + subgenerator
        mod = importlib.import_module(path)
        generator = getattr(mod, "run")
        return generator
    except ImportError as e:
        if "No module named" not in str(e):
            err.new(e)
        return None
    except Exception as e:
        err.new(e, load_generator, "Error loading module")


class ChartfloConfig(AppConfig):
    name = 'chartflo'
    verbose_name = "Chartflo"

    def ready(self):
        """
        Load generators and initialize class instance
        """
        global GENERATORS, cf
        from django.conf import settings
        apps = settings.INSTALLED_APPS
        generators = {}
        for app in apps:
            try:
                res = load_generator(app)
                if res is not None:
                    generators[app] = res
            except Exception as e:
                err.new(e, self.ready,
                        "Can not initialize Chartflo generators")
        GENERATORS = generators
        if err.exists:
            err.trace()
