#!/usr/bin/env python
set -o nounset

pyserv() {
    python -m SimpleHTTPServer 8000
}
cd docs-copy/en/_build/dirhtml; pyserv; cd -
