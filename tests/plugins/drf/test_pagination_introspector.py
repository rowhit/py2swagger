from unittest import SkipTest

from django.test import TestCase

from py2swagger.utils import OrderedDict
from py2swagger.plugins.drf.introspectors.pagination import LimitOffsetPaginationIntrospector, \
    PageNumberPaginationIntrospector, CursorPaginationIntrospector, PaginationBySerializerIntrospector, \
    get_pagination_introspector
from py2swagger.plugins.drf.introspectors.serializer import SerializerIntrospector

from . import REST_FRAMEWORK_V3
from testapp.serializers import TestSimpleSerializer

if REST_FRAMEWORK_V3:
    from testapp.pagination import TestLimitOffsetPaginationViewSet, \
        TestPageNumberPaginationViewSet, TestCursorPaginationViewSet
else:
    from testapp.pagination import TestPaginationSerializerViewSet


class LimitOffsetPaginationIntrospectorTestCase(TestCase):
    def setUp(self):
        if not REST_FRAMEWORK_V3:
            raise SkipTest('Introspector only for DjangoRestFramework => 3.0.0 version')

        serializer_introspector = SerializerIntrospector(TestSimpleSerializer)
        self.introspector = LimitOffsetPaginationIntrospector(view=TestLimitOffsetPaginationViewSet,
                                                              instance=TestLimitOffsetPaginationViewSet.pagination_class,
                                                              si=serializer_introspector)

    def test_responses(self):
        expected_responses = OrderedDict([
            (200, OrderedDict([
                ('description', 'Pagination response'),
                ('schema', OrderedDict([
                    ('type', 'object'),
                    ('id', 'TestSimpleSerializerPaginator'),
                    ('required', ['count', 'next', 'previous', 'results']),
                    ('properties', OrderedDict([
                        ('count', OrderedDict([('type', 'integer')])),
                        ('next', OrderedDict([('type', 'string')])),
                        ('previous', OrderedDict([('type', 'string')])),
                        ('results', OrderedDict([
                            ('type', 'array'), ('items', OrderedDict([
                                ('schema', OrderedDict([
                                    ('id', 'TestSimpleSerializer'),
                                    ('type', 'object'),
                                    ('required', []),
                                    ('properties', OrderedDict([
                                        ('test_field', OrderedDict([
                                            ('type', 'integer'),
                                            ('minimum', 0),
                                            ('maximum', 10),
                                            ('default', 5)
                                        ]))
                                    ]))
                                ]))
                            ]))
                        ]))
                    ]))
                ]))
            ]))
        ])

        responses = self.introspector.responses
        self.assertEqual(expected_responses, responses)

    def test_parameters(self):
        expected_parameters = [
            OrderedDict([('in', 'query'),
                         ('name', u'limit'),
                         ('type', 'string'),
                         ('description', 'Limit parameter (default=None)'),
                         ('required', False)]),
            OrderedDict([('in', 'query'),
                         ('name', u'offset'),
                         ('type', 'integer'),
                         ('description', 'Offset parameter'),
                         ('required', False)])]
        parameters = self.introspector.parameters
        self.assertEqual(parameters, expected_parameters)


class PageNumberPaginationIntrospectorTestCase(TestCase):
    def setUp(self):
        if not REST_FRAMEWORK_V3:
            raise SkipTest('Introspector only for DjangoRestFramework => 3.0.0 version')

        serializer_introspector = SerializerIntrospector(TestSimpleSerializer)
        self.introspector = PageNumberPaginationIntrospector(view=TestPageNumberPaginationViewSet,
                                                             instance=TestPageNumberPaginationViewSet.pagination_class,
                                                             si=serializer_introspector)

    def test_parameters(self):
        expected_parameters = [
            OrderedDict([('in', 'query'),
                         ('name', u'page'),
                         ('type', 'string'),
                         ('description', 'Page parameter'),
                         ('required', False)])
        ]
        parameters = self.introspector.parameters
        self.assertEqual(parameters, expected_parameters)


class CursorPaginationIntrospectorTestCase(TestCase):
    def setUp(self):
        if not REST_FRAMEWORK_V3:
            raise SkipTest('Introspector only for DjangoRestFramework => 3.0.0 version')

        serializer_introspector = SerializerIntrospector(TestSimpleSerializer)
        self.introspector = CursorPaginationIntrospector(view=TestCursorPaginationViewSet,
                                                         instance=TestCursorPaginationViewSet.pagination_class,
                                                         si=serializer_introspector)

    def test_parameters(self):
        expected_parameters = [OrderedDict([('in', 'query'),
                                            ('name', u'cursor'),
                                            ('type', 'string'),
                                            ('description', 'Cursor parameter'),
                                            ('required', False)])]
        parameters = self.introspector.parameters
        self.assertEqual(parameters, expected_parameters)


class PaginationSerializerIntrospectorTestCase(TestCase):
    def setUp(self):
        if REST_FRAMEWORK_V3:
            raise SkipTest('Introspector only for DjangoRestFramework < 3.0.0 version')

        serializer_introspector = SerializerIntrospector(TestPaginationSerializerViewSet.serializer_class)
        self.introspector = PaginationBySerializerIntrospector(view=TestPaginationSerializerViewSet,
                                                               instance=None,
                                                               si=serializer_introspector)

    def test_parameters(self):
        expected_parameters = [OrderedDict([
            ('in', 'query'),
            ('name', 'page'),
            ('type', 'integer'),
            ('description', 'Page parameter'),
            ('required', False)])]
        parameters = self.introspector.parameters
        self.assertEqual(parameters, expected_parameters)


class PaginationIntrospectorMethodsTestCase(TestCase):

    def test_get_introspectos(self):
        if REST_FRAMEWORK_V3:
            introspector = get_pagination_introspector(TestPageNumberPaginationViewSet)
            self.assertTrue(isinstance(introspector, PageNumberPaginationIntrospector))

            introspector = get_pagination_introspector(TestCursorPaginationViewSet)
            self.assertTrue(isinstance(introspector, CursorPaginationIntrospector))

            introspector = get_pagination_introspector(TestLimitOffsetPaginationViewSet)
            self.assertTrue(isinstance(introspector, LimitOffsetPaginationIntrospector))
        else:
            introspector = get_pagination_introspector(TestPaginationSerializerViewSet)
            self.assertTrue(isinstance(introspector, PaginationBySerializerIntrospector))
