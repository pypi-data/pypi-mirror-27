import csv
import io
import re
from pathlib import Path

from docutils import nodes, utils
from docutils.parsers.rst import Directive, directives
from sphinx.locale import _

class CSVListDirective(Directive):

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'file': directives.path,
        'encoding': directives.encoding,
        'title-key': directives.unchanged,
        'id-key': directives.unchanged,
        'id-prefix': directives.unchanged,
    }
    has_content = True

    def run(self):
        attributes = {'format': ' '.join(self.arguments[0].lower().split())}
        encoding = self.options.get('encoding', self.state.document.settings.input_encoding)
        title_key = self.options.get('title-key', '')
        id_key = self.options.get('id-key', '')
        id_prefix = self.options.get('id-prefix', '')

        if self.content:
            if 'file' in self.options:
                raise self.error(
                    '"%s" directive may not both specify an external file '
                    'and have content.' % self.name)
            text = '\n'.join(self.content)

        elif 'file' in self.options:
            source_dir = str(Path(self.state.document.current_source).resolve().parent)
            path = (Path(source_dir) / self.options['file']).resolve()
            text = path.read_text(encoding=encoding)
            attributes['source'] = utils.relative_path(None, path)

        with io.StringIO(text) as f:
            rows = list(csv.reader(f))
        output = '<div class="csv-list">'
        header = rows[0]
        for row in rows[1:]:
            obj = dict(zip(header, row))
            if id_key in obj:
                output += f'<div class="csv-list-item" id="{id_prefix + obj[id_key]}">'
            else:
                output += '<div class="csv-list-item">'
            for key, value in zip(header, row):
                if key != title_key:
                    continue
                value = re.sub(r'[\r\n]+', '<br>', value)
                output += f'<p class="csv-list-title caption" data-csv-list-key="{key}">'
                output += f'<span class="csv-list-key">{key}</span>'
                output += f'<span class="csv-list-value">{value}</span>'
                if id_key in obj:
                    output += f'<a class="headerlink" href="#{id_prefix + obj[id_key]}" title="{_("Permalink to this headline")}">¶</a>'
                output += '</p>'
            for key, value in zip(header, row):
                if key == title_key:
                    continue
                value = re.sub(r'[\r\n]+', '<br>', value)
                output += f'<p class="csv-list-field" data-csv-list-key="{key}">'
                output += f'<span class="csv-list-key">{key}</span>'
                output += f'<span class="csv-list-value">{value}</span>'
                output += '</p>'
            output += '</div>'
        output += '</div>'

        raw_node = nodes.raw('', output, **attributes)
        (raw_node.source, raw_node.line) = self.state_machine.get_source_and_line(self.lineno)
        return [raw_node]



def setup(app):

    def builder_inited(app_):
        if app_.builder.name != 'html':
            return
        app_.builder.config.html_static_path.append(str(Path(__file__).resolve().parent / 'static'))
        app_.add_stylesheet('csv_list.css')

    app.connect('builder-inited', builder_inited)
    app.add_directive('csv-list', CSVListDirective)
