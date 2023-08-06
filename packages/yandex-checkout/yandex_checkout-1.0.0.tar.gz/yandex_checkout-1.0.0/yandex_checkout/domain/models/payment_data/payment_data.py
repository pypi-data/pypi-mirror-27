from yandex_checkout.domain.common.base_object import BaseObject


class PaymentData(BaseObject):
    """
    Base class for Payment data objects
    """
    __type = None

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        self.__type = str(value)
