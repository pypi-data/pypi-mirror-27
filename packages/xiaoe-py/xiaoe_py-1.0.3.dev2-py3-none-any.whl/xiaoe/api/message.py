from xiaoe.type import MessageCreateData, MessageQueryData


class Message(object):
    @classmethod
    def create(cls, data: MessageCreateData, poster):
        path = '/message.send/'
        return poster.post(path, data.data)

    @classmethod
    def query(cls, data: MessageQueryData, poster):
        path = '/message.list.get/'
        return poster.post(path, data.data)
