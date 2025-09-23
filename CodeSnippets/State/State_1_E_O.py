class Locked:
    def handle(self, ctx, a):
        if a == 'coin':
            ctx.mode = Unlocked(); print('unlocked')
        elif a == 'push':
            print('push ignored')
        else:
            print('unknown')

class Unlocked:
    def handle(self, ctx, a):
        if a == 'push':
            ctx.mode = Locked(); print('locked')
        elif a == 'coin':
            print('already unlocked')
        else:
            print('unknown')

class Door:
    def __init__(self):
        self.mode = Locked()
    def request(self, a):
        self.mode.handle(self, a)

if __name__ == '__main__':
    d = Door()
    for a in ['push', 'coin', 'coin', 'push', 'push']:
        print('action', a)
        d.request(a)