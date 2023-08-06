FOO = {
    'Foo': {
        'extensibility-implied': False,
        'imports': {},
        'object-classes': {},
        'object-sets': {},
        'types': {
            'Answer': {
                'type': 'SEQUENCE',
                'members': [
                    {'name': 'id', 'optional': False, 'type': 'INTEGER'},
                    {'name': 'answer','optional': False,'type': 'BOOLEAN'}
                ]
            },
            'Question': {
                'type': 'SEQUENCE',
                'members': [
                    {'name': 'id', 'optional': False, 'type': 'INTEGER'},
                    {'name': 'question', 'optional': False, 'type': 'IA5String'}
                ]
            }
        },
        'values': {}
    }
}
