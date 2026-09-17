from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .player_stats_player_data_version import PlayerStats_player_data_version
    from .role_stats import RoleStats
    from .unlock_info import UnlockInfo

@dataclass
class PlayerStats(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The cash property
    cash: Optional[int] = 0
    # The gold property
    gold: Optional[int] = 0
    # The driver property
    driver: Optional[RoleStats] = None
    # The infantry property
    infantry: Optional[RoleStats] = None
    # The medic property
    medic: Optional[RoleStats] = None
    # The pilot property
    pilot: Optional[RoleStats] = None
    # The player_data_version property
    player_data_version: Optional[PlayerStats_player_data_version] = None
    # The recon property
    recon: Optional[RoleStats] = None
    # The support property
    support: Optional[RoleStats] = None
    # The unlocks property
    unlocks: Optional[list[UnlockInfo]] = None
    # Current WARDOGS overall level.The live account we tested showed that the in-game Wardog levelmatched the sum of the six role levels.
    wardog_level: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> PlayerStats:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: PlayerStats
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return PlayerStats()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .player_stats_player_data_version import PlayerStats_player_data_version
        from .role_stats import RoleStats
        from .unlock_info import UnlockInfo

        from .player_stats_player_data_version import PlayerStats_player_data_version
        from .role_stats import RoleStats
        from .unlock_info import UnlockInfo

        fields: dict[str, Callable[[Any], None]] = {
            "cash": lambda n : setattr(self, 'cash', n.get_int_value()),
            "driver": lambda n : setattr(self, 'driver', n.get_object_value(RoleStats)),
            "gold": lambda n : setattr(self, 'gold', n.get_int_value()),
            "infantry": lambda n : setattr(self, 'infantry', n.get_object_value(RoleStats)),
            "medic": lambda n : setattr(self, 'medic', n.get_object_value(RoleStats)),
            "pilot": lambda n : setattr(self, 'pilot', n.get_object_value(RoleStats)),
            "player_data_version": lambda n : setattr(self, 'player_data_version', n.get_object_value(PlayerStats_player_data_version)),
            "recon": lambda n : setattr(self, 'recon', n.get_object_value(RoleStats)),
            "support": lambda n : setattr(self, 'support', n.get_object_value(RoleStats)),
            "unlocks": lambda n : setattr(self, 'unlocks', n.get_collection_of_object_values(UnlockInfo)),
            "wardog_level": lambda n : setattr(self, 'wardog_level', n.get_int_value()),
        }
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if writer is None:
            raise TypeError("writer cannot be null.")
        writer.write_int_value("cash", self.cash)
        writer.write_object_value("driver", self.driver)
        writer.write_int_value("gold", self.gold)
        writer.write_object_value("infantry", self.infantry)
        writer.write_object_value("medic", self.medic)
        writer.write_object_value("pilot", self.pilot)
        writer.write_object_value("player_data_version", self.player_data_version)
        writer.write_object_value("recon", self.recon)
        writer.write_object_value("support", self.support)
        writer.write_collection_of_object_values("unlocks", self.unlocks)
        writer.write_additional_data_value(self.additional_data)
    

