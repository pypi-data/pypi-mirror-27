from pyadf.group_node import GroupNode
from pyadf.group_node_children_mixin import GroupNodeChildrenMixin


class _ListNode(GroupNode):

    def add_item(self, item):
        "Simplified implementation to add a single list item"
        list_item = ListItem(self)
        list_item.content.append(item)
        self.content.append(list_item)


class BulletList(_ListNode):
    type = 'bulletList'


class OrderedList(_ListNode):
    type = 'orderedList'


class ListItem(GroupNode, GroupNodeChildrenMixin):
    type = 'listItem'
