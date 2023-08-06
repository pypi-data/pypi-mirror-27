# -*- coding: utf-8 -*-

"""
Created on 2017-12-14
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('kotti_util')


def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_util.kotti_configure

        to enable the ``kotti_util`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """

    settings['pyramid.includes'] += ' kotti_util'


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """

    config.add_translation_dirs('kotti_util:locale')
    config.add_renderer(name='csv',
                        factory='kotti_util.renderers.CSVRenderer')


    config.scan(__name__)
