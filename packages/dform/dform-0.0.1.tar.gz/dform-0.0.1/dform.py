import orms


def inject_all(df_class, *excludes):
    excludes = excludes or []
    for appname in filter(lambda name: not name.startswith('__'), dir(orms)):
        if appname in excludes:
            continue
        app = getattr(orms, appname)
        if callable(app):
            setattr(df_class, appname, app)

def inject_selective(df_class, *apps):
    for appname in filter(lambda name: not name.startswith('__'), dir(orms)):

        if appname in apps or appname.startswith('_'):
            app = getattr(orms, appname)
            if callable(app):
                setattr(df_class, appname, app)



