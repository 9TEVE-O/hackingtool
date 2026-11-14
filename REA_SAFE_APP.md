# REA Safe App (bounded build)

This is a **restricted local entry point** for the existing Hackingtool repository.
It is not the full legacy menu, not a privileged installer, and not an authorization
to scan networks, access other hosts, or launch third-party tools.

## Requirements

Python 3.10+ standard library only. No sudo, pip installation, root access, or network
download is required.

## Run

```sh
python3 rea_safe_app.py list
python3 rea_safe_app.py host-to-ip localhost
python3 -m unittest discover -s tests -p 'test_rea_safe_app.py' -v
```

Example resolution output:

```json
{"address": "127.0.0.1", "hostname": "localhost", "scope": "loopback-only", "tool": "Host2IP"}
```

The app preserves the original repository's Host2IP *capability*, but implements a
new standard-library-only, fail-closed resolver. It does **not** import or execute
the original interactive method. Passing the local tests is not proof the full
legacy Hackingtool application starts successfully.

## Security boundaries

- Only the literal hostname `localhost` may reach the resolver.
- Even if a compromised resolver returns a non-loopback IP, the result is blocked.
- External hostnames and other commands are rejected.
- No installer, subprocess, scanning, credential access, or deployment.
- This entry point must not be automatically expanded into an unrestricted launcher.

## Verification and release

The local build was tested with Python 3.13.5. The six regression tests passed.
A full repository CI run and independent release assessment remain open.

This PR is a bounded additive change. It does not replace the original launcher,
merge to master, install system packages, or deploy software.
