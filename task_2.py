# Алгоритм (функція), який знаходить суму всіх значень у двійковому дереві пошуку або в AVL-дереві.
# ЗАВДАННЯ 2: сума всіх значень у BST (двійкове дерево пошуку) та AVL (збалансоване двійкове дерево пошуку).

# -----------------------------
# Частина 1. Звичайне BST
# -----------------------------
class Node:
    def __init__(self, key: int):
        # Кожен вузол зберігає значення (val) і посилання на лівого/правого нащадка
        self.left = None
        self.right = None
        self.val = key

def bst_insert(root: Node | None, key: int) -> Node:
    """Вставка в BST.
    Логіка BST: менше -> вліво, більше/дорівнює -> вправо.
    """
    if root is None:
        # База: якщо піддерево порожнє — створюємо вузол і повертаємо його як корінь піддерева
        return Node(key)
    if key < root.val:
        # Якщо ключ менший за поточний — рекурсивно вставляємо в ліве піддерево
        root.left = bst_insert(root.left, key)
    else:
        # Інакше — в праве (дублікати теж підуть вправо)
        root.right = bst_insert(root.right, key)
    return root  # повертається (можливо оновлений) корінь

def bst_sum(root: Node | None) -> int:
    """Рекурсивна сума значень у BST.
    Ідея: обійти ВСІ вузли (DFS) і скласти їх значення.
    Складність O(n), бо відвідується кожен вузол рівно один раз.
    """
    if root is None:
        # Порожнє піддерево додає 0 до суми — зручно для рекурсії
        return 0
    # Сума = сума лівого піддерева + значення поточного вузла + сума правого піддерева
    return bst_sum(root.left) + root.val + bst_sum(root.right)

# Ітеративна версія суми для BST через стек:
def bst_sum_iter(root: Node | None) -> int:
    """Ітеративний DFS (стек) без рекурсії."""
    total = 0
    stack: list[Node] = []
    cur = root
    # Симульований inorder: ідемо максимально вліво, піднімаємось, йдемо вправо
    while cur or stack:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        total += cur.val
        cur = cur.right
    return total


# -----------------------------
# Частина 2. AVL-дерево (самобалансоване BST)
# -----------------------------
class AVLNode:
    def __init__(self, key: int):
        # Крім ключа, кожен вузол зберігає свою висоту (для контролю балансу)
        self.key = key
        self.height = 1
        self.left: "AVLNode | None" = None
        self.right: "AVLNode | None" = None

def avl_height(n: AVLNode | None) -> int:
    # Висота порожнього піддерева вважається 0
    return 0 if n is None else n.height

def avl_balance(n: AVLNode | None) -> int:
    # Баланс = висота лівого - висота правого; має бути у [-1, 1]
    return 0 if n is None else avl_height(n.left) - avl_height(n.right)

def avl_right_rotate(y: AVLNode) -> AVLNode:
    """Права ротація навколо y.
    Використовується, коли ліве піддерево «занадто важке» (LL або LR випадки).
    """
    x = y.left          # новий корінь піддерева після ротації
    T3 = x.right        # тимчасово зберігаємо праве піддерево x

    # Виконуємо обертання ребер
    x.right = y
    y.left = T3

    # Переобчислюємо висоти після зміни структури
    y.height = 1 + max(avl_height(y.left), avl_height(y.right))
    x.height = 1 + max(avl_height(x.left), avl_height(x.right))
    return x            # повертаємо новий корінь піддерева

def avl_left_rotate(z: AVLNode) -> AVLNode:
    """Ліва ротація навколо z.
    Використовується, коли праве піддерево «занадто важке» (RR або RL випадки).
    """
    y = z.right         # новий корінь піддерева після ротації
    T2 = y.left         # тимчасово зберігаємо ліве піддерево y

    # Обертання
    y.left = z
    z.right = T2

    # Оновлюємо висоти
    z.height = 1 + max(avl_height(z.left), avl_height(z.right))
    y.height = 1 + max(avl_height(y.left), avl_height(y.right))
    return y

def avl_insert(root: AVLNode | None, key: int) -> AVLNode:
    """Вставка елемента в AVL-дерево.
    Крок 1: звичайна BST-вставка.
    Крок 2: оновити висоту вузла.
    Крок 3: перевірити баланс і виконати (за потреби) ротації.
    """
    # --- Крок 1. BST-вставка
    if root is None:
        return AVLNode(key)
    if key < root.key:
        root.left = avl_insert(root.left, key)
    elif key > root.key:
        root.right = avl_insert(root.right, key)
    else:
        # Дублікат не вставляємо — повертаємо корінь без змін
        return root

    # --- Крок 2. Оновлюємо висоту поточного вузла
    root.height = 1 + max(avl_height(root.left), avl_height(root.right))

    # --- Крок 3. Перевіряємо баланс і виправляємо дисбаланс ротаціями
    bal = avl_balance(root)

    # Випадки дисбалансу:
    # LL (ліве-ліве): новий ключ потрапив у ліве піддерево лівого нащадка
    if bal > 1 and key < root.left.key:
        return avl_right_rotate(root)

    # RR (праве-праве): новий ключ у правому піддереві правого нащадка
    if bal < -1 and key > root.right.key:
        return avl_left_rotate(root)

    # LR (ліве-праве): спочатку ліва ротація на лівому нащадку, потім права на корені
    if bal > 1 and key > root.left.key:
        root.left = avl_left_rotate(root.left)
        return avl_right_rotate(root)

    # RL (праве-ліве): спочатку права ротація на правому нащадку, потім ліва на корені
    if bal < -1 and key < root.right.key:
        root.right = avl_right_rotate(root.right)
        return avl_left_rotate(root)

    # Якщо баланс у нормі — повертаємо поточний корінь
    return root

def avl_sum(root: AVLNode | None) -> int:
    """Сума всіх значень у AVL-дереві (так само, як у BST).
    Рекурсивний DFS: sum(left) + key + sum(right).
    """
    if root is None:
        return 0
    return avl_sum(root.left) + root.key + avl_sum(root.right)


# -----------------------------
# Частина 3. Демонстрація/тести
# -----------------------------
if __name__ == "__main__":
    # Побудуємо приклад BST
    bst_root = None
    for x in [5, 3, 2, 4, 7, 6, 8]:
        # Послідовно вставляємо елементи — дерево виростає зверху вниз
        bst_root = bst_insert(bst_root, x)

    # Обчислюємо суму рекурсивно та ітеративно — мають збігатися
    print("Сума у BST (rec):", bst_sum(bst_root))     # очікуємо 35
    print("Сума у BST (iter):", bst_sum_iter(bst_root))  # очікуємо 35
    print("Сума у порожньому BST:", bst_sum(None))    # 0

    # Побудуємо приклад AVL
    avl_root = None
    for x in [10, 20, 30, 25, 28, 27, -1]:
        # Після кожної вставки AVL автоматично ребалансує піддерева
        avl_root = avl_insert(avl_root, x)

    print("Сума в AVL:", avl_sum(avl_root))           # очікуємо 139
    print("Сума у порожньому AVL:", avl_sum(None))    # 0

    # Швидкі перевірки: якщо щось піде не так — піднімуть AssertionError
    assert bst_sum(bst_root) == 35
    assert bst_sum_iter(bst_root) == 35
    assert bst_sum(None) == 0
    assert avl_sum(avl_root) == 139
    assert avl_sum(None) == 0
    print("Всі тести пройдені!")
