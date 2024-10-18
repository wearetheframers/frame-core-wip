---
title: Config
publish: true
---

# Config

::: frame.src.framer.config.FramerConfig
    permissions: Optional[List[str]] = Field(default_factory=lambda: ["with_memory", "with_mem0_search_extract_summarize_plugin", "with_shared_context"])
