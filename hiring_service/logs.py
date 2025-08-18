from enum import StrEnum


class LogLevel(StrEnum):
    Info = "info"
    Debug = "debug"

    @classmethod
    def from_str(cls, mode: str) -> "LogLevel":
        match mode:
            case "info":
                return cls.Info
            case "debug":
                return cls.Debug

        raise ValueError(f"No log level mode: {mode} is not supported")
