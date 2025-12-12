# Deprecated: scripts/

**This directory has been deprecated and consolidated into `35-scripts/`.**

## Migration Guide

All script files from this directory have been moved to:
- **New Location**: `governance/35-scripts/`
- **Purpose**: Centralized script management within the numbered governance dimension structure

## Why This Change?

To resolve duplicate directory issues and align with the governance restructuring:
- Eliminates confusion between root-level `scripts/` and `35-scripts/`
- Provides single source of truth for all governance scripts
- Aligns with the numbered dimension structure

## What to Do

1. Update all references from `governance/scripts/` to `governance/35-scripts/`
2. Update import paths in Python code
3. Update file paths in YAML configurations
4. Update documentation links
5. Update shell script paths

## Backward Compatibility

The original files remain available in:
- `governance/35-scripts/` - **Use this location going forward**

---
**Deprecated**: 2025-12-12
**Migration Deadline**: 2026-03-31
