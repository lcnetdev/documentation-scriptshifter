#!/usr/bin/env python
"""
Generate ../supported-scripts.md from a local clone of the ScriptShifter
source repository (https://github.com/lcnetdev/scriptshifter).

Usage:

    uv run --with pyyaml python meta/gen_supported_scripts.py /path/to/scriptshifter

This mirrors the logic of `doc/gen_script_table_doc.py` in the ScriptShifter
repository, but does not need the application installed or its database
initialized. It reads `scriptshifter/tables/index.yml` for the list of
exposed languages, and each table's YAML file for version, date and
supported directions. Mapping-file links point at the GitHub repository.
"""

import sys
from datetime import date
from os import path

import yaml

DOCROOT = path.dirname(path.dirname(path.abspath(__file__)))
OUT = path.join(DOCROOT, "supported-scripts.md")
GH_BLOB = "https://github.com/lcnetdev/scriptshifter/blob/main/scriptshifter/tables/data"

HEADER = """# Supported scripts

Below are the scripts and languages supported by ScriptShifter, and the
supported directionality of each. The same list is available live from the
[`/languages`](https://bibframe.org/scriptshifter/languages) endpoint of the
REST API and in the language drop-down of the
[web interface](https://bibframe.org/scriptshifter/).

- **Mapping file**: the key used in the API and in the `?lang=` URL parameter
  of the web interface. Links go to the transliteration table on GitHub.
- **Alias of**: the entry uses the same transliteration table as the one
  indicated, under a different name.
- **Script-to-Roman** / **Roman-to-script**: whether the table supports
  romanization and/or the reverse direction.
- **Version** and **Last updated**: version and date recorded in the
  transliteration table itself.

*This table was generated on {today} from the
[ScriptShifter repository](https://github.com/lcnetdev/scriptshifter).*

| Mapping file | Script name | Alias of | Script-to-Roman | Roman-to-script | Version | Last updated |
| --- | --- | --- | :-: | :-: | --- | --- |
"""

FOOTER = """
---

[Back to Table of Contents](index.md)
"""


def main(src_root):
    tables_dir = path.join(src_root, "scriptshifter", "tables")
    data_dir = path.join(tables_dir, "data")

    with open(path.join(tables_dir, "index.yml")) as fh:
        index = yaml.safe_load(fh)

    rows = []
    for name, entry in index.items():
        label = entry.get("name", name)
        if "alias_of" in entry:
            target = entry["alias_of"]
            rows.append(
                f"| `{name}` | {label} | [`{target}`]({GH_BLOB}/{target}.yml)"
                " | - | - | - | - |"
            )
            continue

        with open(path.join(data_dir, name + ".yml")) as fh:
            table = yaml.safe_load(fh)
        general = table.get("general", {}) or {}
        version = general.get("version", "-")
        updated = general.get("date", "-")
        rows.append(
            f"| [`{name}`]({GH_BLOB}/{name}.yml) | {label} | - | "
            f"{'Y' if 'script_to_roman' in table else 'N'} | "
            f"{'Y' if 'roman_to_script' in table else 'N'} | "
            f"{version} | {updated} |"
        )

    with open(OUT, "w") as fh:
        fh.write(HEADER.format(today=date.today().isoformat()))
        fh.write("\n".join(rows) + "\n")
        fh.write(FOOTER)

    n_alias = sum(1 for e in index.values() if "alias_of" in e)
    print(f"Wrote {OUT}: {len(rows)} entries ({n_alias} aliases).")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
