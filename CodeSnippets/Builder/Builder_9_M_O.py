import abc
import copy


class House:
    def __init__(self, foundation=None, structure=None, roof=None, features=None):
        self.foundation = foundation
        self.structure = structure
        self.roof = roof
        self.features = features or []

    def __str__(self):
        parts = [
            f"Foundation: {self.foundation}",
            f"Structure: {self.structure}",
            f"Roof: {self.roof}",
            f"Features: {', '.join(self.features) if self.features else 'None'}",
        ]
        return "House:\n  " + "\n  ".join(parts)


class Assembler(abc.ABC):
    @abc.abstractmethod
    def reset(self):
        pass

    @abc.abstractmethod
    def set_foundation(self, kind: str):
        pass

    @abc.abstractmethod
    def set_structure(self, kind: str):
        pass

    @abc.abstractmethod
    def set_roof(self, kind: str):
        pass

    @abc.abstractmethod
    def add_feature(self, feature: str):
        pass

    @abc.abstractmethod
    def get_result(self) -> House:
        pass


class BasicAssembler(Assembler):
    def __init__(self):
        self.reset()

    def reset(self):
        self._product = House()
        self._completed = False

    def set_foundation(self, kind: str):
        if not kind:
            raise ValueError("Foundation type required")
        self._product.foundation = kind

    def set_structure(self, kind: str):
        if not kind:
            raise ValueError("Structure type required")
        self._product.structure = kind

    def set_roof(self, kind: str):
        if not kind:
            raise ValueError("Roof type required")
        self._product.roof = kind

    def add_feature(self, feature: str):
        if feature:
            self._product.features.append(feature)

    def get_result(self) -> House:
        if not (self._product.foundation and self._product.structure and self._product.roof):
            raise RuntimeError("Incomplete assembly: foundation, structure, and roof are required")
        result = copy.deepcopy(self._product)
        self.reset()
        return result


class LuxuryAssembler(BasicAssembler):
    def add_feature(self, feature: str):
        super().add_feature(feature)
        if feature and feature.lower() == "pool":
            self._product.features.append("heated pool")
            self._product.features.append("pool lighting")


class Orchestrator:
    def assemble_minimal(self, assembler: Assembler) -> House:
        assembler.set_foundation("Concrete")
        assembler.set_structure("Wood Frame")
        assembler.set_roof("Asphalt Shingles")
        return assembler.get_result()

    def assemble_luxury(self, assembler: Assembler) -> House:
        assembler.set_foundation("Reinforced Concrete")
        assembler.set_structure("Steel Frame")
        assembler.set_roof("Slate Tiles")
        assembler.add_feature("Smart Home System")
        assembler.add_feature("Pool")
        assembler.add_feature("Solar Panels")
        return assembler.get_result()


if __name__ == "__main__":
    orchestrator = Orchestrator()

    basic = BasicAssembler()
    minimal_house = orchestrator.assemble_minimal(basic)
    print(minimal_house)

    luxury = LuxuryAssembler()
    luxury_house = orchestrator.assemble_luxury(luxury)
    print()
    print(luxury_house)

    incomplete = BasicAssembler()
    try:
        incomplete.set_foundation("Stone")
        incomplete.get_result()
    except RuntimeError as e:
        print()
        print("Error during assembly:", e)