# FIXtodict

FIXtodict is a FIX Dictionary generator tool.

> Copyright (c) 2020, Filippo Costa. Released under Apache License 2
> <https://www.apache.org/licenses/LICENSE-2.0.t
> Find me on Github: <https://github.com/neysofu>

FIXtodict program performs data enhancing and data sanitazion on raw FIX Repository files. The resulting data will feature:

- High-quality Markdown documentation obtained from several sources, plus
  minor improvements, e.g.
  * links to ISO standards,
  * RFC 2119 terms highlight,
  * links for internal navigation,
  * markup, bold text, etc.
- Embedded documentation strings (instead of separate files, like the
  original FIX Repository).
- Full breakdown into fields and components.
- Information about included Extension Packs.
- General cleanup and improved data consistency across all FIX protocol
  versions.

Developers working with the FIX Protocol can really benefit from higher-quality JSON (rather than clunky XML) sources to use for code generation, data explorations, and so on.

In short, FIXtodict makes it much easier to work with the FIX protocol.