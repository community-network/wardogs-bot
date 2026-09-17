from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import ComposedTypeWrapper, Parsable, ParseNode, ParseNodeHelper, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .player_stats_player_data_version_member1 import PlayerStats_player_data_versionMember1

@dataclass
class PlayerStats_player_data_version(ComposedTypeWrapper, Parsable):
    """
    Composed type wrapper for classes int, PlayerStats_player_data_versionMember1
    """
    # Composed type representation for type int
    integer: Optional[int] = None
    # Composed type representation for type PlayerStats_player_data_versionMember1
    player_stats_player_data_version_member1: Optional[PlayerStats_player_data_versionMember1] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> PlayerStats_player_data_version:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: PlayerStats_player_data_version
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        result = PlayerStats_player_data_version()
        if integer_value := parse_node.get_int_value():
            result.integer = integer_value
        else:
            from .player_stats_player_data_version_member1 import PlayerStats_player_data_versionMember1

            result.player_stats_player_data_version_member1 = PlayerStats_player_data_versionMember1()
        return result
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .player_stats_player_data_version_member1 import PlayerStats_player_data_versionMember1

        if self.player_stats_player_data_version_member1:
            return ParseNodeHelper.merge_deserializers_for_intersection_wrapper(self.player_stats_player_data_version_member1)
        return {}
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if writer is None:
            raise TypeError("writer cannot be null.")
        if self.integer:
            writer.write_int_value(None, self.integer)
        else:
            writer.write_object_value(None, self.player_stats_player_data_version_member1)
    

