from typing import Literal

MappingTag = Literal['map_key', 'map_value']
JoinTag = Literal['join_key', 'join_value']
PrimaryKeyTag = Literal['primary_key']
GeographicTag = Literal['country', 'region', 'continent']
PriceTag = Literal['unit_price', 'total_price']
TyframeTag = MappingTag | JoinTag | PrimaryKeyTag | GeographicTag | PriceTag
