#!/usr/bin/env python3
"""Render the public benchmark's Mermaid files through Kroki (requires curl).

Renders the gold-standard domain models (class diagrams) and the gold-standard
sequence diagrams to SVG, validates the result, and regenerates the sequence
diagram gallery (3_visualizations/sequence_diagrams/README.md).
"""

import argparse
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / '2_gold_standard_domain_models'
SEQUENCES = ROOT / '4_gold_standard_sequence_diagrams'
STORIES = ROOT / '1_user_stories'
VISUALS = ROOT / '3_visualizations'
SEQ_VISUALS = VISUALS / 'sequence_diagrams'
SVG = '{http://www.w3.org/2000/svg}'

PROJECT_NAMES = {'fish_chips': 'Fish & Chips'}
ARROW = re.compile(r'^\s*(\w+)\s*-{1,2}[>x)]{1,2}\s*(\w+)\s*:', re.M)
LIFELINE = re.compile(r'^\s*(actor|participant) (\w+) as (.+?)\s*$', re.M)


def project_name(stem):
    return PROJECT_NAMES.get(stem, stem.capitalize())


def render(source, endpoint):
    response = subprocess.run(
        ['curl', '-L', '--fail', '--silent', '--show-error', '--retry', '2', '--max-time', '60',
         '-H', 'Content-Type: text/plain', '--data-binary', '@' + str(source),
         endpoint.rstrip('/') + '/mermaid/svg'],
        capture_output=True,
    )
    if response.returncode:
        raise SystemExit(response.stderr.decode('utf-8', errors='replace'))
    # Keep dark lines and labels readable in viewers using dark backgrounds.
    return response.stdout.replace(b'<svg ', b'<svg style="background-color: white;" ', 1)


def parse_svg(name, data):
    svg = ET.fromstring(data)
    if svg.tag != SVG + 'svg':
        raise ValueError(f'{name}: response is not an SVG')
    return svg


def classes_of(svg):
    for e in svg.iter():
        yield e, e.attrib.get('class', '').split()


def check_domain_model(source, data):
    """Confirm that Mermaid rendered every declared class and association."""
    svg = parse_svg(source.name, data)
    text = source.read_text(encoding='utf-8')
    expected = (len(re.findall(r'^\s+class C\d+\[', text, re.M)),
                len(re.findall(r'^\s+C\d+ -- C\d+\s*$', text, re.M)))
    actual = (sum('node' in c and e.tag.endswith('}g') for e, c in classes_of(svg)),
              sum('relation' in c and e.tag.endswith('}path') for e, c in classes_of(svg)))
    if actual != expected:
        raise ValueError(f'{source.name}: rendered node/edge count differs: '
                         f'{actual[0]}/{actual[1]} vs {expected[0]}/{expected[1]}')
    return f'{actual[0]} nodes, {actual[1]} associations'


def check_sequence_svg(source, data):
    """Confirm that Mermaid rendered every declared lifeline and message."""
    svg = parse_svg(source.name, data)
    text = source.read_text(encoding='utf-8')
    expected = (len(LIFELINE.findall(text)), len(ARROW.findall(text)))
    actual = (sum('actor-top' in c for _, c in classes_of(svg)),
              sum('messageText' in c for _, c in classes_of(svg)))
    if actual != expected:
        raise ValueError(f'{source.name}: rendered lifeline/message count differs: '
                         f'{actual[0]}/{actual[1]} vs {expected[0]}/{expected[1]}')
    return f'{actual[0]} lifelines, {actual[1]} messages'


def norm(term):
    term = re.sub(r'[^a-z]', '', term.lower())
    return term[:-1] if term.endswith('s') else term


def gold_model(project):
    text = (MODELS / f'{project}.mmd').read_text(encoding='utf-8')
    ids = dict(re.findall(r'class (C\d+)\["([^"]+)"\]', text))
    associations = {frozenset((ids[a], ids[b]))
                    for a, b in re.findall(r'^\s*(C\d+) -- (C\d+)\s*$', text, re.M)}
    return {norm(c): c for c in ids.values()}, associations


def read_sequence(source, classes, associations):
    """Parse the header comments and check the diagram against the gold domain model."""
    text = source.read_text(encoding='utf-8')
    head = re.search(r'^\s*%% (SD\d+) - (.+?)\s*$', text, re.M)
    stories = re.search(r'^\s*%% Stories:(.+)$', text, re.M)
    description = re.search(r'^\s*%% Description:\s*(.+?)\s*$', text, re.M)
    if not (head and stories and description):
        raise ValueError(f'{source}: needs %% SDn - title, %% Stories: and %% Description: comments')
    lifelines = {}
    for kind, alias, label in LIFELINE.findall(text):
        if kind == 'participant':
            if norm(label) not in classes:
                raise ValueError(f'{source}: participant "{label}" is not a gold class')
            lifelines[alias] = classes[norm(label)]
        else:
            lifelines[alias] = None
    for sender, receiver in ARROW.findall(text):
        a, b = lifelines.get(sender), lifelines.get(receiver)
        if a and b and a != b and frozenset((a, b)) not in associations:
            raise ValueError(f'{source}: message {sender} -> {receiver} has no gold association {a} -- {b}')
    listed = [int(n) for n in re.findall(r'\d+', stories[1])]
    tagged = {int(n) for group in re.findall(r'\[([\d, ]+)\]', text) for n in group.split(',')}
    if set(listed) != tagged:
        raise ValueError(f'{source}: stories in the header {sorted(listed)} differ from the [n] tags {sorted(tagged)}')
    return {'id': head[1], 'title': head[2], 'stories': listed, 'description': description[1],
            'source': source, 'messages': len(ARROW.findall(text))}


def story_texts(project):
    lines = (STORIES / f'{project}.txt').read_text(encoding='utf-8').splitlines()
    return {i: line.strip() for i, line in enumerate(lines, 1) if line.strip()}


def ranges(numbers):
    numbers, out, start = sorted(numbers), [], None
    for i, n in enumerate(numbers):
        start = n if start is None else start
        if i + 1 == len(numbers) or numbers[i + 1] != n + 1:
            out.append(str(start) if start == n else f'{start}–{n}')
            start = None
    return ', '.join(out)


def gallery(projects):
    out = ['# Sequence-diagram gallery', '',
           '[Back to dataset README](../../README.md) · '
           '[Conventions and coverage](../../4_gold_standard_sequence_diagrams/README.md)', '',
           'Gold-standard sequence diagrams, rendered from the Mermaid sources in '
           '`4_gold_standard_sequence_diagrams/`. They are an addition to the original dataset, written for a '
           'master thesis on validating LLM-generated domain models, and are not part of the work of '
           'Bragilovski et al. Click an image to open its SVG and zoom in. `[n]` in a diagram is the line '
           'number of the user story it covers.', '']
    for project, diagrams in projects.items():
        stories = story_texts(project)
        covered = {n for d in diagrams for n in d['stories']}
        name = project_name(project)
        out += [f'## {name}', '',
                f'{len(diagrams)} diagrams, {sum(d["messages"] for d in diagrams)} messages, '
                f'{len(covered)} of {len(stories)} user stories covered '
                f'(not covered: {ranges(set(stories) - covered)}). '
                f'[User stories](../../1_user_stories/{project}.txt) · '
                f'[Domain model](../{project}.svg)', '']
        for d in diagrams:
            stem = d['source'].stem
            out += [f'### {d["id"]} · {d["title"]}', '', d['description'], '',
                    f'[Mermaid source](../../4_gold_standard_sequence_diagrams/{project}/{stem}.mmd) · '
                    f'[SVG image]({project}/{stem}.svg)', '',
                    f'[![{name} {d["id"]}: {d["title"]}]({project}/{stem}.svg)]({project}/{stem}.svg)', '',
                    '<details><summary>User stories covered</summary>', '',
                    '| # | User story |', '|---|---|']
            out += [f'| {n} | {stories[n].replace("|", "&#124;")} |' for n in d['stories']]
            out += ['', '</details>', '']
    return '\n'.join(out)


def write(destination, data):
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + '.tmp')
    temporary.write_bytes(data)
    temporary.replace(destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--endpoint', default='https://kroki.io',
                        help='Kroki base URL; receives each Mermaid source file')
    parser.add_argument('--check', action='store_true',
                        help='Validate existing SVG files and the gallery without network access')
    args = parser.parse_args()

    models = sorted(MODELS.glob('*.mmd'))
    if not models:
        parser.error('No Mermaid files found')
    rendered = []
    for source in models:
        destination = VISUALS / f'{source.stem}.svg'
        data = destination.read_bytes() if args.check else render(source, args.endpoint)
        print(f'{source.name}: {check_domain_model(source, data)}', flush=True)
        rendered.append((destination, data))

    projects = {}
    for folder in sorted(p for p in SEQUENCES.glob('*') if p.is_dir()):
        classes, associations = gold_model(folder.name)
        diagrams = [read_sequence(s, classes, associations) for s in sorted(folder.glob('*.mmd'))]
        projects[folder.name] = diagrams
        for d in diagrams:
            source = d['source']
            destination = SEQ_VISUALS / folder.name / f'{source.stem}.svg'
            data = destination.read_bytes() if args.check else render(source, args.endpoint)
            print(f'{folder.name}/{source.name}: {check_sequence_svg(source, data)}', flush=True)
            rendered.append((destination, data))
    page = gallery(projects).encode('utf-8')
    gallery_path = SEQ_VISUALS / 'README.md'

    if args.check:
        if not gallery_path.exists() or gallery_path.read_bytes().replace(b'\r\n', b'\n') != page:
            raise SystemExit(f'{gallery_path.relative_to(ROOT)} is out of date; run scripts/render_models.py')
        print(f'Validated {len(rendered)} SVG diagrams and the sequence-diagram gallery')
        return
    for destination, data in rendered:
        write(destination, data)
    write(gallery_path, page)
    print(f'Saved {len(rendered)} SVG diagrams and the sequence-diagram gallery in {VISUALS}')


if __name__ == '__main__':
    main()
