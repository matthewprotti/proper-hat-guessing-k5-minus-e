# Development record

The first independent-checker invocation failed at Python parsing because an
arithmetic key-encoding expression had an unmatched parenthesis. No mathematical
check ran and no acceptance was inferred. It was replaced by an explicit
four-digit accumulation loop. The corrected checker then passed the family,
all 136 pilot matchings, and the rejecting controls.

Some environment startup hooks printed an unrelated spreadsheet-runtime warning
on stderr while running ordinary Python. Final data-only checks use isolated
`-I -S -B` Python, which needs no site-package startup hooks. Exit status and
actual certificate checks, not the presence of a log word, determine success.

Builders and checkers are separately structured but were created in one
assistant context. No blinded independence or external human review is claimed.
