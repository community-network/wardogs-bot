from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class RoleStats(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The level property
    level: Optional[int] = 0
    # The xp property
    xp: Optional[int] = 0
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> RoleStats:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: RoleStats
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return RoleStats()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "level": lambda n : setattr(self, 'level', n.get_int_value()),
            "xp": lambda n : setattr(self, 'xp', n.get_int_value()),
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
        writer.write_int_value("level", self.level)
        writer.write_int_value("xp", self.xp)
        writer.write_additional_data_value(self.additional_data)
    

