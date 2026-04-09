# Practical Commands For Go Symbol Recovery

Use this reference when you want a concrete, analyst-style command sequence instead of only high-level workflow guidance.

## Fast local triage

```bash
file sample.bin
sha256sum sample.bin
binwalk -Me sample.bin
```

**binwalk notes:**

- `-Me` extracts known file system signatures recursively; review `*_extract/` output for nested loaders.
- Add `-W` for deeper entropy / signature passes when the first pass is empty but the file looks packed.
- Use `-y '!<sig>'` to exclude noisy signature types when extraction explodes in size.

**UPX (only if `file` or binwalk indicates UPX):**

```bash
upx -d -o sample.unpacked sample.bin
```

Keep the original file; hash both originals and unpacked artifacts.

```bash
go version -m sample.bin
go tool buildid sample.bin
python3 scripts/extract_buildinfo.py sample.bin
```

## Strings: host tools vs disassembler

Go binaries often expose many plaintext strings. If IDA or Ghidra shows suspiciously few strings, trust **`strings(1)` on the file** and investigate segment alignment or analysis settings.

```bash
strings -a -n 6 sample.bin | wc -l
strings -a -n 6 sample.bin | rg -i 'go1\.|main\.|runtime\.|github\.com/|gitlab\.com/|/src/|/pkg/mod/|golang\.org/'
```

ELF targets (Linux):

```bash
strings -el sample.bin | head -200
```

**Quick IOC-oriented grep (adjust patterns to case):**

```bash
strings -a -n 8 sample.bin | rg -i 'https?://|grpc|\.onion|powershell|/bin/(ba)?sh|/etc/|/tmp/|BEGIN (RSA|OPENSSH) PRIVATE'
```

## Object-level inspection (locate pclntab / sections)

```bash
readelf -S sample.bin 2>/dev/null | rg -i 'gopclntab|noptrdata|rodata'
objdump -h sample.bin 2>/dev/null | rg -i 'text|data|rodata'
```

Use these when automations fail—manual section boundaries sometimes need repair in the disassembler.

## Metadata parsers

```bash
GoReSym -t -d -p sample.bin > goresym.json
python3 scripts/go_inventory.py goresym.json
redress info sample.bin
redress packages sample.bin --std --vendor --filepath
redress source sample.bin
```

## IDA Pro MCP sequence

If `mrexodia/ida-pro-mcp` is connected, prefer these concrete tools:

1. `list_funcs` for `main` and any recovered package prefixes.
2. `lookup_funcs` to resolve `main.main`, `main.init`, and large user handlers.
3. `decompile` for `main.main`, `main.init`, and functions reached from runtime pivots.
4. `xrefs_to`:
   - `runtime.newobject`
   - `runtime.newproc`
   - `runtime.makechan`
   - `runtime.selectgo`
5. `find_regex` for:
   - `go1\\.` or module paths
   - `/src/`, `/pkg/mod/`, `github.com/`, `gitlab.com/`
   - config paths, URLs, shell strings, service names
6. `export_funcs` for the top user packages and suspicious handler functions.
7. `rename` and `set_comments` only after the user-code shortlist is stable.

Suggested wording:
- Run `list_funcs` for `main` and show the largest recovered user functions.
- Run `xrefs_to` on `runtime.newproc` and keep only non-runtime callers.
- Run `find_regex` for `github.com/|gitlab.com/|/src/|/pkg/mod/` and return xref-bearing hits.
- Run `export_funcs` for the top five user handlers in JSON.

Do not claim the MCP ran unless it actually ran.

## Further reading

See [external-resources.md](external-resources.md) for Mandiant/Google posts, GoReSym, Redress, AlphaGolang, and practitioner articles.
