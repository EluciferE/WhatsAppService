class Base:
    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, json: dict):
        instance = cls()
        for key, value in json.items():
            instance.__dict__[key] = value
        return instance


class ProfileId(Base):
    user: str
    server: str
    _serialized: str


class Profile(Base):
    canReceiveMessage: bool
    id: dict
    isBusiness: bool
    numberExists: bool
    status: str
