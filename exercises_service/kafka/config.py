from dataclasses import dataclass
from typing import Self

from environment import Config, EnvVar


@dataclass(frozen=True)
class KafkaProducerConfig(Config):
    bootstrap: str
    acks: str = "all"
    linger_ms: int = 5

    @classmethod
    def from_env(cls) -> Self:
        return cls(
            bootstrap=EnvVar.get_or_default("KAFKA_BOOTSTRAP", "localhost:9092"),
            acks=EnvVar.get_or_default("KAFKA_ACKS", "all"),
            linger_ms=EnvVar.get_or_default("KAFKA_LINGER_MS", 5, int),
        )


@dataclass(frozen=True)
class KafkaConsumerConfig(Config):
    bootstrap: str
    group_id: str
    auto_offset_reset: str

    @classmethod
    def from_env(cls) -> Self:
        return cls(
            bootstrap=EnvVar.get_or_default("KAFKA_BOOTSTRAP", "localhost:9092"),
            group_id=EnvVar.get_or_default("KAFKA_GROUP_ID", "exercises-service"),
            auto_offset_reset=EnvVar.get_or_default(
                "KAFKA_AUTO_OFFSET_RESET", "earliest"
            ),
        )
