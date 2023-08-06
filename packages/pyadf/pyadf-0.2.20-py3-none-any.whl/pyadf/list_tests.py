import unittest
from .lists import BulletList, OrderedList, ListItem
from pyadf.paragraph import Paragraph
from pyadf.document import Document

class ListTests(unittest.TestCase):

    def test_bullet_list_with_no_items(self):
        bullet_list = BulletList()
        doc = bullet_list.to_doc()
        
        self.assertEqual(doc, {
            'type': 'bulletList',
            'content': []
        })

    def test_ordered_list_with_no_items(self):
        ordered_list = OrderedList()
        doc = ordered_list.to_doc()
        
        self.assertEqual(doc, {
            'type': 'orderedList',
            'content': []
        })

    def test_list_item_with_text(self):
        list_item = ListItem()
        list_item.paragraph().text('hello there')
        doc = list_item.to_doc()

        self.assertEqual(doc, {
            'type': 'listItem',
            'content': [{
                'type': 'paragraph',
                'content': [
                    {
                        'type': 'text',
                        'text': 'hello there'
                    }
                ]
            }]
        })

    def test_bullet_list_with_two_items(self):
        bullet_list = BulletList()
        bullet_list.add_item(Paragraph().text('hello'))
        bullet_list.add_item(Paragraph().text('there'))
        
        doc = bullet_list.to_doc()

        self.assertEqual(doc, {
            'type': 'bulletList',
            'content': [
                {
                    'type': 'listItem',
                    'content': [{
                        'type': 'paragraph',
                        'content': [
                            {
                                'type': 'text',
                                'text': 'hello'
                            }
                        ]
                    }]
                },
                {
                    'type': 'listItem',
                    'content': [{
                        'type': 'paragraph',
                        'content': [
                            {
                                'type': 'text',
                                'text': 'there'
                            }
                        ]
                    }]
                }
            ]
        })

    def test_ordered_list_with_two_items(self):
        ordered_list = OrderedList()
        ordered_list.add_item(Paragraph().text('hello'))
        ordered_list.add_item(Paragraph().text('there'))
        
        doc = ordered_list.to_doc()

        self.assertEqual(doc, {
            'type': 'orderedList',
            'content': [
                {
                    'type': 'listItem',
                    'content': [{
                        'type': 'paragraph',
                        'content': [
                            {
                                'type': 'text',
                                'text': 'hello'
                            }
                        ]
                    }]
                },
                {
                    'type': 'listItem',
                    'content': [{
                        'type': 'paragraph',
                        'content': [
                            {
                                'type': 'text',
                                'text': 'there'
                            }
                        ]
                    }]
                }
            ]
        })
