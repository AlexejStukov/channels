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
        
    def echo(self, message):
        self.channel.send({"text": message.get("text", None)})
