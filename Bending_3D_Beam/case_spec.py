import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CaseSpec:
    case_name: str
    analysis_type: str
    element_size_m: float
    load_value_n: float
    load_direction: str
    constraint: str
    stress_limit_pa: float

    @classmethod
    def from_file(cls, path: Path):
        with path.open("r", encoding="utf-8") as stream:
            data = json.load(stream)
        spec = cls(
            case_name=str(data["case_name"]),
            analysis_type=str(data["analysis_type"]),
            element_size_m=float(data["element_size_m"]),
            load_value_n=float(data["load_value_n"]),
            load_direction=str(data["load_direction"]),
            constraint=str(data["constraint"]),
            stress_limit_pa=float(data["stress_limit_pa"]),
        )
        return spec.validate()

    def validate(self):
        if not self.case_name.strip():
            raise ValueError("case_name must not be empty")
        if self.analysis_type != "static_structural":
            raise ValueError("analysis_type must be static_structural")
        if self.element_size_m <= 0:
            raise ValueError("element_size_m must be greater than zero")
        if self.load_value_n <= 0:
            raise ValueError("load_value_n must be greater than zero")
        if self.load_direction not in {"negative_x", "negative_y", "negative_z"}:
            raise ValueError("load_direction must be negative_x, negative_y, or negative_z")
        if self.constraint != "fixed_left_end":
            raise ValueError("constraint must be fixed_left_end")
        if self.stress_limit_pa <= 0:
            raise ValueError("stress_limit_pa must be greater than zero")
        return self
