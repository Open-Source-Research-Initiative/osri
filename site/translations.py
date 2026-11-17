#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Export current English messages or audit editable translation catalogs."""
import argparse
import json
from pathlib import Path
import sys

import i18n


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('build', type=Path, help='A freshly built site directory')
    parser.add_argument('--export', type=Path, help='Write a source inventory for translation')
    parser.add_argument('--page', help='Limit export to an English route, for example /start/')
    parser.add_argument('--language', choices=[tag for tag in i18n.LANGUAGES if tag != 'en'])
    parser.add_argument('--import-file', type=Path, help='Merge translated messages from a page export')
    parser.add_argument('--check', action='store_true', help='Fail if a language has untranslated source messages')
    args = parser.parse_args()
    inventory = json.loads((args.build / 'translation-source.json').read_text())
    hub = Path(__file__).resolve().parents[1]
    if args.page and args.page not in inventory['pages']:
        parser.error('Unknown page route')
    keys = set(inventory['messages'])
    if args.page:
        keys &= set(inventory['pages'][args.page])
    if args.import_file:
        if not args.language:
            parser.error('--import-file requires --language')
        incoming = json.loads(args.import_file.read_text())
        if incoming.get('language') != args.language:
            parser.error('Export language differs from --language')
        if incoming.get('source_digest') != inventory['source_digest']:
            parser.error('Export source changed. Export the current page and compare before importing.')
        changes = incoming['messages']
        if not isinstance(changes, dict) or any(key not in keys or not isinstance(value, str) or not value.strip() for key, value in changes.items()):
            parser.error('Import requires current English keys and nonempty translated strings')
        import re
        if any(set(re.findall(r'\{\w+\}', key)) != set(re.findall(r'\{\w+\}', value)) for key, value in changes.items()):
            parser.error('Preserve all named placeholders such as {count}')
        record = i18n.catalog(hub, args.language)
        record['messages'].update(changes)
        record['source_commit'] = inventory['source_commit']
        record['source_digest'] = inventory['source_digest']
        (hub / 'translations/catalogs' / (args.language + '.json')).write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    if args.export:
        current = i18n.catalog(hub, args.language)['messages'] if args.language else {}
        exported = {key: inventory[key] for key in ['source_commit', 'source_digest']}
        exported.update(language=args.language, page=args.page, messages={key: current.get(key, '') for key in sorted(keys)})
        args.export.write_text(json.dumps(exported, ensure_ascii=False, indent=2) + '\n')
    failed = False
    for language in i18n.LANGUAGES:
        if language == 'en':
            continue
        record = i18n.catalog(hub, language)
        missing = [key for key in inventory['messages'] if not record['messages'].get(key, '').strip()]
        obsolete = set(record['messages']) - set(inventory['messages'])
        print(f'{language}: {len(inventory["pages"])} pages; {len(missing)} missing; {len(obsolete)} obsolete; {record["status"]}; reviewer {record["reviewer"]}')
        failed |= bool(missing)
    if args.check and failed:
        sys.exit('Translation catalog is missing current English messages. Export, translate and rebuild.')


if __name__ == '__main__':
    main()
