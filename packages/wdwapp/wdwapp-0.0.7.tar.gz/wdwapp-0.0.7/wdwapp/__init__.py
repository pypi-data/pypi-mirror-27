__version__ = '0.0.7'
__year__ = 2017

def main(global_config, **settings):

    from pyramid.config import Configurator
    from sqlalchemy import engine_from_config
    from pyramid.session import SignedCookieSessionFactory
    from .models import DBSession, Base, Root

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    my_session_factory = SignedCookieSessionFactory(
        settings['session.secret'])

    config = Configurator(settings=settings,
                    session_factory=my_session_factory,
                    root_factory='wdwapp.models.Root')

    config.include('pyramid_chameleon')

    # Routes for web site
    config.add_route('overview', '/')
    config.add_route('detail', '/detail/{lid}')
    config.add_route('wikipage_add', '/add')
    config.add_route('wikipage_edit', '/{uid}/edit')
    config.add_route('home', '/howdy/{first}/{last}')

    # Static things
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('deform_static', 'deform:static/')

    # Let's go
    config.scan('.views')
    return config.make_wsgi_app()
