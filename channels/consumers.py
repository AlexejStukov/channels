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
        if call in valid_calls:
            call_method = getattr(self, call)
            call_method(message)

    def send(self, data):
        self.channel.send({"text": data})

    def echo(self, message):
        data = message.get("text", None)
        self.send(data)


class GroupConsumer(Consumer):
    group_name
    
    @property
    def channel(self):
        return Group(group_name)
    
    def connect(self, message):
        self.channel.add(message.reply_channel)
    
    def disconnect(self, message):
        self.channel.discard(message.reply_channel)
        
        
        
    
    
    
