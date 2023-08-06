# -*- coding: utf-8 -*-

from trytond.pool import Pool
from .party import Party


def register():
    Pool.register(
        Party,
        module='party_fieldaddon', type_='model')
