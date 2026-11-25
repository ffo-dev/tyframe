from typing import Literal

MappingTag = Literal['map_key', 'map_value']
JoinTag = Literal['join_key', 'join_value']
PrimaryKeyTag = Literal['primary_key']
TyframeTag = MappingTag | JoinTag | PrimaryKeyTag
