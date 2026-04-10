# Regex bundles for `find_regex`

IDA MCP's `find_regex` accepts full ripgrep-style patterns. These
bundles are optimized for a single call that covers many IOC families
at once — in practice one call for each bundle saves 10-20 sequential
calls and gives the analyst a compact first-pass IOC list.

Each bundle is a single alternation; paste it whole.

---

## All-purpose IOC scan

```
https?://|\bftp://|[0-9]{1,3}(\.[0-9]{1,3}){3}(:\d+)?|[A-Za-z0-9-]{2,}\.(com|net|org|ru|cn|io|xyz|top|info|biz|dev|gg|su|sh)\b|User-Agent:|Host:\s|Cookie:
```

## Crypto and auth primitives

```
ChaCha20|Poly1305|AES-?(128|192|256)?|SHA-?(1|224|256|384|512)|HMAC|HKDF|PBKDF2|Argon2|scrypt|bcrypt|Ed25519|X25519|curve25519|secp256k1|RSA-?\d*|rustls|OpenSSL|BoringSSL|mbedTLS|-----BEGIN [A-Z ]+-----
```

## Shell, process, and execution

```
/bin/sh|/bin/bash|cmd\.exe|powershell|systemctl|sc\.exe|schtasks|curl\s|wget\s|chmod\s|chown\s|netsh|ipconfig|ifconfig|whoami|hostname|uname\s|nc\s|ncat\s|socat\s|/usr/bin/env
```

## Filesystem and persistence

```
/etc/(passwd|shadow|cron|rc|systemd)|/tmp/|/var/(run|tmp|lib)/|/proc/\d+/|~/\.(ssh|cache|config)|%APPDATA%|%TEMP%|%PROGRAMDATA%|C:\\Windows\\(System32|Temp)|HKLM\\|HKCU\\
```

## Rust-specific markers

```
panicked at\s|called `Option::unwrap|called `Result::unwrap|thread '.+' panicked|\.rs:\d+|registry/src/[^/]+/[a-zA-Z0-9_-]+-\d+\.\d+\.\d+|/home/[\w.-]+/|/Users/[\w.-]+/|rustc \d+\.\d+
```

## Go-specific markers

```
go1\.\d+(\.\d+)?|runtime\.(newproc|selectgo|chansend|chanrecv|newobject|makechan|morestack)|github\.com/[\w.-]+/[\w.-]+|gopkg\.in/[\w./-]+|main\.(main|init)\b|\.go:\d+
```

## Build / attribution fingerprints

```
GOROOT|GOPATH|CARGO_(HOME|TARGET)|RUSTC_|BUILD_ID|git rev-parse|[0-9a-f]{40}\b|/build/|/src/[\w./\-]+|filed\b|\bsucess|\brecive|\boccured\b
```

## Usage pattern

A typical Phase-1 survey will do **3** `find_regex` calls, one from the
"All-purpose IOC scan", one from the language-specific bundle (Rust or
Go), and one from "Build / attribution fingerprints". Three calls is
enough to drive the first analyst report; expand only as questions
sharpen.

Note: because the ripgrep backend is regex-anchored on whole strings,
escape backslashes appropriately when pasting into an MCP client that
JSON-encodes its arguments.
