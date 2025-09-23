class Vehicle:
    def __init__(self):
        self.chassis_type = None
        self.engine_type = None
        self.body_style = None
        self.features = []
        self.color = None

    def __str__(self):
        return (f"Vehicle: Chassis={self.chassis_type}, Engine={self.engine_type}, "
                f"Body={self.body_style}, Color={self.color}, Features={self.features}")

class VehicleConfigurator:
    def __init__(self):
        self._vehicle = Vehicle()
        self._required_fields = {'chassis_type', 'engine_type', 'body_style'}

    def set_chassis(self, chassis_type):
        if chassis_type not in ['sedan', 'suv', 'truck']:
            raise ValueError("Invalid chassis type")
        self._vehicle.chassis_type = chassis_type
        return self

    def set_engine(self, engine_type):
        if engine_type not in ['v4', 'v6', 'v8']:
            raise ValueError("Invalid engine type")
        self._vehicle.engine_type = engine_type
        return self

    def set_body_style(self, body_style):
        self._vehicle.body_style = body_style
        return self

    def add_feature(self, feature):
        incompatible_features = {
            'manual_transmission': ['automatic_transmission'],
            'sunroof': ['convertible_top']
        }
        if feature in incompatible_features:
            for inc in incompatible_features[feature]:
                if inc in self._vehicle.features:
                    raise ValueError(f"Feature {feature} incompatible with {inc}")
        self._vehicle.features.append(feature)
        return self

    def set_color(self, color):
        self._vehicle.color = color
        return self

    def _validate_required(self):
        missing = self._required_fields - {
            attr for attr in self._required_fields
            if getattr(self._vehicle, attr) is not None
        }
        if missing:
            raise ValueError(f"Missing required fields: {missing}")

    def _validate_features(self):
        if len(self._vehicle.features) > 5:
            raise ValueError("Too many features: maximum 5 allowed")
        if 'offroad_package' in self._vehicle.features and self._vehicle.chassis_type != 'suv':
            raise ValueError("'offroad_package' requires SUV chassis")

    def assemble(self):
        self._validate_required()
        self._validate_features()
        result = self._vehicle
        self._reset()
        return result

    def _reset(self):
        self._vehicle = Vehicle()

class VehicleOrchestrator:
    def __init__(self, configurator):
        self._configurator = configurator

    def create_sedan(self):
        self._configurator.set_chassis('sedan').set_engine('v4').set_body_style('4-door')
        self._configurator.set_color('silver').add_feature('automatic_transmission')

    def create_suv(self):
        self._configurator.set_chassis('suv').set_engine('v6').set_body_style('5-door')
        self._configurator.set_color('black').add_feature('sunroof').add_feature('offroad_package')

    def create_custom(self, specs):
        self._configurator.set_chassis(specs['chassis']).set_engine(specs['engine'])
        self._configurator.set_body_style(specs['body']).set_color(specs['color'])
        for feat in specs.get('features', []):
            self._configurator.add_feature(feat)

if __name__ == "__main__":
    configurator = VehicleConfigurator()
    orchestrator = VehicleOrchestrator(configurator)

    try:
        orchestrator.create_sedan()
        sedan = configurator.assemble()
        print("Sedan:", sedan)
    except ValueError as e:
        print("Error creating sedan:", e)

    try:
        orchestrator.create_suv()
        suv = configurator.assemble()
        print("SUV:", suv)
    except ValueError as e:
        print("Error creating SUV:", e)

    try:
        configurator.set_chassis('sedan').set_body_style('2-door').set_color('red')
        custom = configurator.assemble()
        print("Custom:", custom)
    except ValueError as e:
        print("Error creating custom:", e)

    try:
        configurator.add_feature('offroad_package')
        invalid = configurator.assemble()
    except ValueError as e:
        print("Edge case error:", e)