# documentation-scriptshifter

Documentation for [ScriptShifter](https://bibframe.org/scriptshifter/), the Library of Congress transliteration tool. Source code: https://github.com/lcnetdev/scriptshifter

Start at [index.md](index.md).

## Regenerating the supported scripts table

`supported-scripts.md` is generated from a local clone of the ScriptShifter repository:

```
uv run --with pyyaml python meta/gen_supported_scripts.py /path/to/scriptshifter
```

## License

Released into the public domain under [CC0 1.0](LICENSE).
