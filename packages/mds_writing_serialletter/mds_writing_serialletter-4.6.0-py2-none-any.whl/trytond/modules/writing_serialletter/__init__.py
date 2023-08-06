# -*- coding: utf-8 -*-

from trytond.pool import Pool
from .serialletter import Serialletter, SerialletterRel
from .user import User
from .party import Party, Address
from .salutes import Salutes
from .greetings import Greetings
from .reportletter import SerialletterOdt

def register():
    Pool.register(
        User,
        Salutes,
        Greetings,
        Party,
        Address,
        Serialletter,
        SerialletterRel,
        module='writing_serialletter', type_='model')
    Pool.register(
        SerialletterOdt,
        module='writing_serialletter', type_='report')
