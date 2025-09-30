import copy
from typing import Dict, Any

class Resume:
    def __init__(self) -> None:
        self.info: Dict[str, Any] = {}

    def set_info(self, key: str, value: Any) -> None:
        self.info[key] = value

    def get_info(self, key: str) -> Any:
        return self.info.get(key)

    def duplicate(self) -> 'Resume':
        try:
            return copy.deepcopy(self)
        except Exception as e:
            raise RuntimeError("Duplication failed") from e

    def __str__(self) -> str:
        return str(self.info)

if __name__ == "__main__":
    original = Resume()
    original.set_info("name", "Alice")
    original.set_info("skills", ["Python", "Design"])
    copy_resume = original.duplicate()
    copy_resume.set_info("name", "Alice-Smith")
    print(original)
    print(copy_resume)