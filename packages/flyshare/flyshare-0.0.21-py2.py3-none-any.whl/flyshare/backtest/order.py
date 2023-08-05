# coding=utf-8

class Order():
    def __init__(self, *args, **kwargs):
        self.order = QAMarket_bid()

    def load_order_strategy(self, strategy):
        self.strategy = strategy

    def apply_order_strategy(self):
        self.order.apply(self.strategy)

    def signal(towards=1):
        pass




if __name__=='__main__':
    order=Order()
