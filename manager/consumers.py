from channels.generic.websocket import JsonWebsocketConsumer


class AuctionConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        self.send_json({'type': 'auction.connect', 'message': 'Connected to auction channel'})

    def disconnect(self, close_code):
        pass

    def receive_json(self, content, **kwargs):
        self.send_json({'type': 'auction.echo', 'payload': content})


class MatchConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        self.send_json({'type': 'match.connect', 'message': 'Connected to match channel'})

    def disconnect(self, close_code):
        pass

    def receive_json(self, content, **kwargs):
        self.send_json({'type': 'match.echo', 'payload': content})
