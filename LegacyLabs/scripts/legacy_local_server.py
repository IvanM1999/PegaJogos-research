import argparse
import json
import logging
import socketserver
import urllib.parse
from http.server import SimpleHTTPRequestHandler
from pathlib import Path


class LegacyPegaJogoHandler(SimpleHTTPRequestHandler):
    LEGACY_REPORT_PATH = Path(__file__).resolve().parent.parent / 'reports' / 'legacy_strings_report.json'

    def __init__(self, *args, static_root: Path | None = None, **kwargs):
        self.static_root = static_root or Path('.')
        self.legacy_report = self.load_legacy_report()
        super().__init__(*args, directory=str(self.static_root), **kwargs)

    def load_legacy_report(self) -> dict:
        if not self.LEGACY_REPORT_PATH.exists():
            logging.warning('Legacy report file not found: %s', self.LEGACY_REPORT_PATH)
            return {}
        try:
            with self.LEGACY_REPORT_PATH.open('r', encoding='utf-8') as report_file:
                return json.load(report_file)
        except Exception as exc:
            logging.warning('Failed to load legacy report: %s', exc)
            return {}

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.lower()
        query = urllib.parse.parse_qs(parsed.query)
        raw_query = parsed.query
        logging.info('GET %s', self.path)

        if path == '/jogar':
            return self.serve_jogar(query)
        if path == '/_embed/swf.asp':
            return self.serve_embed_swf(query)
        if path.endswith(('.php', '.asp')) or path.startswith('/_embed'):
            return self.serve_legacy_stub(parsed.path, query, raw_query)
        return super().do_GET()

    def serve_jogar(self, query):
        jogo = query.get('jogo', [''])[0]
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        html = [
            '<!doctype html>',
            '<html><head><meta charset="utf-8"><title>PegaJogo Legacy Local Server</title></head><body>',
            '<h1>PegaJogo Local Server</h1>',
            '<p>This is a local stub for <code>/jogar</code>.</p>',
        ]
        if jogo:
            html.append(f'<p>Requested jogo: <strong>{jogo}</strong></p>')
        html.append('<p>If this page is used by the legacy client, it is now running locally.</p>')
        html.append('</body></html>')
        self.wfile.write('\n'.join(html).encode('utf-8'))

    def serve_embed_swf(self, query):
        swf_id = query.get('id', [''])[0]
        swf_file = self.find_swf_by_id(swf_id)
        if isinstance(swf_file, Path):
            swf_url = urllib.parse.quote(str(swf_file.relative_to(self.static_root)).replace('\\', '/'))
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            html = [
                '<!doctype html>',
                '<html><head><meta charset="utf-8"><title>Legacy SWF Embed</title></head><body>',
                f'<h1>Loading SWF id={swf_id}</h1>',
                f'<object data="/{swf_url}" type="application/x-shockwave-flash" width="800" height="600">',
                f'  <param name="movie" value="/{swf_url}">',
                '  <p>Flash content not available.</p>',
                '</object>',
                '</body></html>',
            ]
            self.wfile.write('\n'.join(html).encode('utf-8'))
            return

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        html = [
            '<!doctype html>',
            '<html><head><meta charset="utf-8"><title>Legacy SWF Embed</title></head><body>',
            f'<h1>SWF embed request id={swf_id}</h1>',
            '<p>No local SWF file was found for this id.</p>',
            '<p>Check the LegacyLabs string report for an exact URL and add the matching file to the `Games` folder.</p>',
            '</body></html>',
        ]
        self.wfile.write('\n'.join(html).encode('utf-8'))

    def serve_legacy_stub(self, path, query, raw_query):
        if path == '/_embed/swf.asp':
            return self.serve_embed_swf(query)

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        html = [
            '<!doctype html>',
            '<html><head><meta charset="utf-8"><title>Legacy Server Stub</title></head><body>',
            '<h1>Legacy Server Stub</h1>',
            f'<p>Requested path: <code>{path}</code></p>',
            '<p>This request is handled by the LegacyLabs local mock server.</p>',
            '<h2>Query</h2>',
            '<pre>' + urllib.parse.unquote_plus(raw_query) + '</pre>',
        ]

        urls = self.legacy_report.get('URLs', [])
        hosts = self.legacy_report.get('Hosts', [])
        scripts = self.legacy_report.get('Scripts', [])

        if urls:
            html.append('<h2>Known legacy URLs</h2>')
            html.append('<ul>')
            for url in urls:
                html.append(f'<li>{url}</li>')
            html.append('</ul>')

        if hosts:
            html.append('<h2>Known legacy hosts</h2>')
            html.append('<ul>')
            for host in hosts:
                html.append(f'<li>{host}</li>')
            html.append('</ul>')

        if scripts:
            html.append('<h2>Known legacy script URLs</h2>')
            html.append('<ul>')
            for script in scripts:
                html.append(f'<li>{script}</li>')
            html.append('</ul>')

        html.extend([
            '<h2>Available SWF files matching id</h2>',
            '<ul>',
        ])
        swf_matches = self.find_swf_by_id(query.get('id', [''])[0], list_only=True)
        if not isinstance(swf_matches, list):
            swf_matches = []
        for found in swf_matches:
            html.append(f'<li>{found}</li>')
        html.extend(['</ul>', '</body></html>'])
        self.wfile.write('\n'.join(html).encode('utf-8'))

    def find_swf_by_id(self, swf_id: str, list_only: bool = False) -> Path | list[str] | None:
        if not swf_id:
            return [] if list_only else None

        matches: list[str] = []
        for path in self.static_root.rglob('*.swf'):
            if swf_id in path.name:
                if list_only:
                    matches.append(str(path.relative_to(self.static_root)).replace('\\', '/'))
                else:
                    return path
        return matches if list_only else None

    def log_message(self, format, *args):
        logging.info(format % args)


def serve(port: int, root: Path):
    handler = lambda *args, **kwargs: LegacyPegaJogoHandler(*args, static_root=root, **kwargs)
    with socketserver.ThreadingTCPServer(('0.0.0.0', port), handler) as httpd:
        logging.info('Starting LegacyLabs local server on port %s, root=%s', port, root)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logging.info('Server stopped')


def parse_args():
    parser = argparse.ArgumentParser(description='Run a local mock server for legacy PegaJogo network requests.')
    parser.add_argument('--port', type=int, default=80, help='Port to listen on. Use 80 for legacy host binding.')
    parser.add_argument('--root', default='../DataOriginal/executavel', help='Static file root directory to serve existing legacy assets.')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging.')
    return parser.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format='[%(levelname)s] %(message)s')
    root = Path(args.root).resolve()
    if not root.exists():
        raise FileNotFoundError(f'Root path does not exist: {root}')
    serve(args.port, root)


if __name__ == '__main__':
    main()
