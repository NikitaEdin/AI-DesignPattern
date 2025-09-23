class StatePatternDemo:
    def __init__(self):
        self.state = 'start'
    
    def request(self, req):
        if req == 'turn_on':
            self.state = 'on'
        elif req == 'turn_off':
            self.state = 'off'
        else:
            print('Unknown request')
    
    def get_state(self):
        return self.state

class Light:
    def __init__(self):
        self.state = StatePatternDemo()
    
    def turn_on(self):
        self.state.request('turn_on')
    
    def turn_off(self):
        self.state.request('turn_off')
    
    def get_state(self):
        return self.state.get_state()

if __name__ == '__main__':
    light = Light()
    light.turn_on()
    print(light.get_state()) # prints 'on'
    light.turn_off()
    print(light.get_state()) # prints 'off'