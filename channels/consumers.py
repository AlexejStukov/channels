from channels import Channel, Group


class Consumer:
    valid_calls = ["echo"]
    channel = None

    def connect(self, message):
        self.channel = message.reply_channel

    def disconnect(self, message):
        self.channel = None

    def receive(self, message):
        call = message.get("call", None)
        if call in self.valid_calls:
            call_method = getattr(self, call)
            call_method(message)

    def send(self, data):
        self.channel.send({"text": data})

    def echo(self, message):
        text = self.get_text(message)
        self.send(text)

    @staticmethod
    def get_text(message):
        return message.get("text", None)


class GroupConsumer(Consumer):
    group_name = None

    @property
    def channel(self):
        return Group(self.group_name)
    
    def connect(self, message):
        self.channel.add(message.reply_channel)
    
    def disconnect(self, message):
        self.channel.discard(message.reply_channel)
        

class ModelConsumer(GroupConsumer):
    model = None
    serializer = None
    publish_to = None

    @property
    def channel(self):
        return Group(self.model.__name__)


class ModelInstanceConsumer(ModelConsumer):
    instance_pk = None

    @property
    def channel(self):
        return Group(self.model.__name__ + str(self.instance_pk))

    def connect(self, message):
        text = self.get_text(message)
        self.instance_pk = text.get("pk", None)



    
    
