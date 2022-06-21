from inventory.test.api.utils import get_connection_query

item_node_query_fragment = f"""
    id
    sku
    isService
    isActive
    barcode
    cost
    currentStock
    creationDate
    markup
    name
    price
    versionId
    {get_connection_query("id", "itemVersions")}
"""
