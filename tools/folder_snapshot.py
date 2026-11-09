"""Read-only folder inventory and self-contained expandable HTML report."""
import argparse
from datetime import datetime, timezone
import html
import json
import os
from pathlib import Path
import stat
import uuid


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def capture(roots, include_system=False):
    selected = [Path(p).absolute() for p in roots]
    for root in selected:
        if root.is_symlink():
            raise ValueError('Select a real folder, not a symbolic link')
    resolved = [p.resolve() for p in selected]
    if len(set(resolved)) != len(resolved) or any(
        a != b and a.is_relative_to(b) for a in resolved for b in resolved
    ):
        raise ValueError('Selected roots must not overlap')
    result = dict(version=1, id=str(uuid.uuid4()), started=timestamp(),
                  parameters=dict(roots=[str(p) for p in selected],
                                  include_system=include_system,
                                  follow_links=False, hash_policy='none; metadata only'),
                  roots=[], complete=True)

    def walk(path):
        node = dict(name=path.name or str(path), path=str(path), kind='folder',
                    hidden=path.name.startswith('.'), children=[], files=0, bytes=0,
                    direct_files=0, folders=0, errors=[], excluded=False)
        try:
            metadata = path.lstat()
            if stat.S_ISLNK(metadata.st_mode) or getattr(metadata, 'st_file_attributes', 0) & 0x400:
                node.update(kind='boundary', reason='Link or reparse point; not followed')
                return node
            if not stat.S_ISDIR(metadata.st_mode):
                raise ValueError('Selected root is not a directory')
            if path.name in ('.git', '.obsidian') and not include_system:
                node.update(excluded=True, reason='System folder contents excluded')
                return node
            with os.scandir(path) as entries:
                ordered = sorted(entries, key=lambda e: e.name.casefold())
            for entry in ordered:
                child_path = path / entry.name
                try:
                    info = entry.stat(follow_symlinks=False)
                    if entry.is_symlink() or getattr(info, 'st_file_attributes', 0) & 0x400:
                        child = dict(name=entry.name, path=str(child_path), kind='boundary',
                                     reason='Link or reparse point; not followed')
                    elif entry.is_dir(follow_symlinks=False):
                        child = walk(child_path)
                        node['folders'] += 1 + child.get('folders', 0)
                        node['files'] += child.get('files', 0)
                        node['bytes'] += child.get('bytes', 0)
                    elif entry.is_file(follow_symlinks=False):
                        child = dict(name=entry.name, path=str(child_path), kind='file',
                                     bytes=info.st_size, modified_ns=info.st_mtime_ns)
                        node['direct_files'] += 1
                        node['files'] += 1
                        node['bytes'] += info.st_size
                    else:
                        child = dict(name=entry.name, path=str(child_path), kind='boundary', reason='Special file')
                    node['children'].append(child)
                except OSError as error:
                    node['errors'].append(dict(path=str(child_path), error=str(error)))
                    result['complete'] = False
            if path.stat().st_mtime_ns != metadata.st_mtime_ns:
                node['errors'].append(dict(path=str(path), error='Directory changed during scan; recapture recommended'))
                result['complete'] = False
        except (OSError, ValueError) as error:
            node['errors'].append(dict(path=str(path), error=str(error)))
            result['complete'] = False
        return node

    for root in selected:
        result['roots'].append(walk(root))
    result['finished'] = timestamp()
    return result


def render(snapshot):
    escape = lambda value: html.escape(str(value), quote=True)

    def branch(node):
        name = escape(node['name'])
        if node['kind'] == 'file':
            return f'<li title="{escape(node["path"])}">{name} <small>{node["bytes"]:,} bytes</small></li>'
        if node['kind'] == 'boundary':
            return f'<li>{name} <small>{escape(node["reason"])}</small></li>'
        badges = (' · dot-prefixed' if node['hidden'] else '') + (' · excluded contents' if node['excluded'] else '')
        errors = ''.join(f'<p class="error">{escape(e["path"])}: {escape(e["error"])}</p>' for e in node['errors'])
        contents = ''.join(branch(child) for child in node['children'])
        return (f'<details><summary><strong>{name}</strong> '
                f'<small>{node["files"]:,} files · {node["folders"]:,} folders · {node["bytes"]:,} bytes{badges}</small></summary>'
                f'<p class="path">{escape(node["path"])}</p>{errors}'
                f'<p>{escape(node.get("reason", ""))}</p><ul>{contents}</ul></details>')

    trees = ''.join('<section>' + branch(node) + '</section>' for node in snapshot['roots'])
    return ('''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Vault folder snapshot</title>
<style> :root{color-scheme:dark;font:16px/1.5 system-ui;background:#151920;color:#e7edf5}
body{max-width:1400px;margin:auto;padding:28px}h1{margin-bottom:4px}small,.path{color:#aebccc}
.path{overflow-wrap:anywhere}#roots{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:18px;align-items:start}
section,.parameters{background:#202733;border:1px solid #3c485a;border-radius:10px;padding:14px}
summary{cursor:pointer;padding:10px;overflow-wrap:anywhere}summary small{display:block;padding-left:18px}ul{padding-left:20px;list-style:none}li{padding:7px;overflow-wrap:anywhere}li small{margin-left:10px}details details{border-left:1px solid #465568;margin:7px 0}button{font:inherit;padding:8px 14px;margin:12px 8px 16px 0;background:#304059;color:inherit;border:1px solid #617899;border-radius:6px;cursor:pointer}.error{color:#ffbcac}pre{white-space:pre-wrap;overflow-wrap:anywhere}summary:focus-visible,button:focus-visible{outline:3px solid #b4ceff}</style>
<h1>Vault folder snapshot</h1><p>Read-only inventory · not a backup · counts cover included entries only.</p>
''' + f'<p>Captured {escape(snapshot["started"])} to {escape(snapshot["finished"])} · '
        + ('Completed with no scan errors' if snapshot['complete'] else '<span class="error">Incomplete — inspect errors below</span>') + '</p>' \
        + '<details class="parameters"><summary>Scan parameters</summary><pre>' + escape(json.dumps(snapshot['parameters'], indent=2)) + '</pre></details>' \
        + '<button id="expand">Expand all</button><button id="collapse">Collapse all</button><main id="roots">' + trees \
        + '''</main><script>document.getElementById('expand').onclick=()=>document.querySelectorAll('#roots details').forEach(d=>d.open=true);document.getElementById('collapse').onclick=()=>document.querySelectorAll('#roots details').forEach(d=>d.open=false);</script></html>''')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('roots', nargs='+', help='Vault or parent folders to inventory')
    parser.add_argument('--output', required=True, help='New report directory OUTSIDE all selected roots')
    parser.add_argument('--include-system', action='store_true', help='Inventory .git/.obsidian metadata, never file contents')
    parser.add_argument('--open', action='store_true', help='Open the saved report in the default browser')
    args = parser.parse_args()
    output = Path(args.output).resolve()
    if any(output.is_relative_to(Path(root).resolve()) for root in args.roots):
        parser.error('Report output must be outside every scanned root')
    if output.exists():
        parser.error('Choose a new output directory; existing reports are never overwritten')
    snapshot = capture(args.roots, args.include_system)
    output.mkdir(parents=True, exist_ok=False)
    (output / 'snapshot.json').write_text(json.dumps(snapshot, indent=2), encoding='utf-8')
    report = output / 'snapshot.html'
    report.write_text(render(snapshot), encoding='utf-8')
    print(f'Report: {report}\nJSON: {output / "snapshot.json"}')
    if args.open:
        import webbrowser
        webbrowser.open(report.as_uri())
    return 0 if snapshot['complete'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
