from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import ComposedTypeWrapper, Parsable, ParseNode, ParseNodeHelper, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .player_stats_created_at_member1 import PlayerStats_created_atMember1

@dataclass
class PlayerStats_created_at(ComposedTypeWrapper, Parsable):
    """
    Composed type wrapper for classes PlayerStats_created_atMember1, str
    """
    # Composed type representation for type PlayerStats_created_atMember1
    player_stats_created_at_member1: Optional[PlayerStats_created_atMember1] = None
    # Composed type representation for type str
    string: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> PlayerStats_created_at:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: PlayerStats_created_at
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        result = PlayerStats_created_at()
        if string_value := parse_node.get_str_value():
            result.string = string_value
        else:
            from .player_stats_created_at_member1 import PlayerStats_created_atMember1

            result.player_stats_created_at_member1 = PlayerStats_created_atMember1()
        return result
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .player_stats_created_at_member1 import PlayerStats_created_atMember1

        if self.player_stats_created_at_member1:
            return ParseNodeHelper.merge_deserializers_for_intersection_wrapper(self.player_stats_created_at_member1)
        return {}
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if writer is None:
            raise TypeError("writer cannot be null.")
        if self.string:
            writer.write_str_value(None, self.string)
        else:
            writer.write_object_value(None, self.player_stats_created_at_member1)
    

