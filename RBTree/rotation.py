def bst_left_rotate(bst, node):
    r = node.right
    p = node.parent
    r.parent = p
    if p:
        if node == p.left:
            p.left = r
        else:
            p.right = r
    node.parent = r
    node.right = r.left
    node.right.parent = node
    r.left = node
    if node == bst.root:
        bst.root = r


def bst_right_rotate(bst, node):
    l = node.left
    p = node.parent
    l.parent = p
    if p:
        if node == p.left:
            p.left = l
        else:
            p.right = l
    node.parent = l
    node.left = l.right
    node.left.parent = node
    l.right = node
    if node == bst.root:
        bst.root = l