from django.test import TestCase
from django.test.client import RequestFactory

from cms.api import add_plugin
from cms.models import Placeholder
from cms.plugin_rendering import ContentRenderer

from .cms_plugins import ContainerPlugin, ContainerCellPlugin
from .models import Container, ContainerCell


class GridTests(TestCase):

    def test_container_html(self):
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            ContainerPlugin,
            'en',
            background_class='background--light'
        )
        renderer = ContentRenderer(request=RequestFactory())
        html = renderer.render_plugin(model_instance, {})
        html = html.replace('\n', '')
        self.assertEqual(html, '<div class="background background--light" style=""><div class="container"><div class="row"></div></div></div>')

    def test_container_background_id(self):
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            ContainerPlugin,
            'en',
            background_id="my-id"
        )
        renderer = ContentRenderer(request=RequestFactory())
        html = renderer.render_plugin(model_instance, {})
        html = html.replace('\n', '')
        self.assertEqual(html, '<div class="background " style="" id="my-id"><div class="container"><div class="row"></div></div></div>')

    def test_container_padding(self):
        model = Container(
            padding_top='1rem',
            padding_right='2rem',
            padding_bottom='3rem',
            padding_left='4rem'
        )
        self.assertEqual(model.background_style, 'padding-top:1rem;padding-right:2rem;padding-bottom:3rem;padding-left:4rem')

    def test_container_str(self):
        model = Container(
            background_class='light',
            background_id='foo'
        )
        self.assertEqual(str(model), '#foo .light')

    def test_cell_html(self):
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            ContainerCellPlugin,
            'en',
            size_desktop=4,
            margin_top='1rem'
        )
        renderer = ContentRenderer(request=RequestFactory())
        html = renderer.render_plugin(model_instance, {})
        html = html.replace('\n', '')
        self.assertEqual(html, '<div class="col-sm-12 col-lg-4" style="margin-top:1rem"></div>')

    def test_cell_padding(self):
        model = ContainerCell(
            padding_top='1rem',
            padding_right='2rem',
            padding_bottom='3rem',
            padding_left='4rem'
        )
        self.assertEqual(model.style, 'padding-top:1rem;padding-right:2rem;padding-bottom:3rem;padding-left:4rem')

    def test_cell_margin(self):
        model = ContainerCell(
            margin_top='10%',
            margin_right='-5px',
            margin_bottom='0',
            margin_left='0'
        )
        self.assertEqual(model.style, 'margin-top:10%;margin-right:-5px;margin-bottom:0;margin-left:0')

    def test_cell_str(self):
        model = ContainerCell(
            size_desktop='6'
        )
        self.assertEqual(str(model), 'Mobile 12; Desktop 6')