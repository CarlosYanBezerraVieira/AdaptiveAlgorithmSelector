def busca_hash(arr, target):
    """Cria uma tabela hash a partir do array e busca em tempo O(1) médio."""
    hash_table = {val: i for i, val in enumerate(arr)}
    return hash_table.get(target, -1)