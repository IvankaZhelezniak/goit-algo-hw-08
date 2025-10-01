# Алгоритм (функція), який знаходить найменше значення у двійковому дереві пошуку або в AVL-дереві.

# -----------------------------
# Варіант 1: Звичайне BST (бінарне дерево пошуку)
# -----------------------------
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def bst_insert(root: Node | None, key: int) -> Node:
    """Стандартна вставка в BST."""
    if root is None:
        return Node(key)
    if key < root.val:
        root.left = bst_insert(root.left, key)
    else:
        root.right = bst_insert(root.right, key)
    return root

def bst_min_value(root: Node | None) -> int | None:
    """
    Повертає мінімальне значення в BST.
    Алгоритм: ідемо максимально вліво (поки є left).
    Якщо дерево порожнє -> None.
    Складність: O(h), де h — висота дерева.
    """
    if root is None:
        return None
    current = root
    while current.left is not None:
        current = current.left
    return current.val


# -----------------------------
# Варіант 2: AVL-дерево
# (мінімум шукається тим самим принципом — ідемо вліво)
# -----------------------------
class AVLNode:
    def __init__(self, key: int):
        self.key = key
        self.height = 1
        self.left: "AVLNode | None" = None
        self.right: "AVLNode | None" = None

def avl_height(node: AVLNode | None) -> int:
    return 0 if node is None else node.height

def avl_balance(node: AVLNode | None) -> int:
    return 0 if node is None else avl_height(node.left) - avl_height(node.right)

def avl_right_rotate(y: AVLNode) -> AVLNode:
    x = y.left
    T3 = x.right if x else None

    x.right = y
    y.left = T3

    y.height = 1 + max(avl_height(y.left), avl_height(y.right))
    x.height = 1 + max(avl_height(x.left), avl_height(x.right))
    return x

def avl_left_rotate(z: AVLNode) -> AVLNode:
    y = z.right
    T2 = y.left if y else None

    y.left = z
    z.right = T2

    z.height = 1 + max(avl_height(z.left), avl_height(z.right))
    y.height = 1 + max(avl_height(y.left), avl_height(y.right))
    return y

def avl_insert(root: AVLNode | None, key: int) -> AVLNode:
    if root is None:
        return AVLNode(key)
    if key < root.key:
        root.left = avl_insert(root.left, key)
    elif key > root.key:
        root.right = avl_insert(root.right, key)
    else:
        return root  # дублікатів не вставляємо

    root.height = 1 + max(avl_height(root.left), avl_height(root.right))
    bal = avl_balance(root)

    # LL
    if bal > 1 and key < root.left.key:
        return avl_right_rotate(root)
    # RR
    if bal < -1 and key > root.right.key:
        return avl_left_rotate(root)
    # LR
    if bal > 1 and key > root.left.key:
        root.left = avl_left_rotate(root.left)
        return avl_right_rotate(root)
    # RL
    if bal < -1 and key < root.right.key:
        root.right = avl_right_rotate(root.right)
        return avl_left_rotate(root)

    return root

def avl_min_value(root: AVLNode | None) -> int | None:
    """
    Повертає мінімальний ключ в AVL-дереві.
    Ідемо максимально вліво. Якщо дерево порожнє -> None.
    Складність: O(h), h — висота дерева (в AVL h = O(log n)).
    """
    if root is None:
        return None
    current = root
    while current.left is not None:
        current = current.left
    return current.key


# -----------------------------
# Тести
# -----------------------------
if __name__ == "__main__":
    # BST приклад
    bst_root = None
    for x in [5, 3, 7, 2, 4, 6, 8]:
        bst_root = bst_insert(bst_root, x)
    print("Мінімум у BST:", bst_min_value(bst_root))  # очікуємо 2

    # Порожній BST
    print("Мінімум у порожньому BST:", bst_min_value(None))  # очікуємо None

    # AVL приклад
    avl_root = None
    for x in [10, 20, 30, 25, 28, 27, -1]:
        avl_root = avl_insert(avl_root, x)
    print("Мінімум в AVL:", avl_min_value(avl_root))  # очікуємо -1

    # Порожній AVL
    print("Мінімум у порожньому AVL:", avl_min_value(None))  # очікуємо None


    # Швидкі перевірки
assert bst_min_value(bst_root) == 2
assert bst_min_value(None) is None
assert avl_min_value(avl_root) == -1
assert avl_min_value(None) is None
print("Всі тести пройдені!")
