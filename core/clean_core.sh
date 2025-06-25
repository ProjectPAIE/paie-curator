#!/bin/bash

mkdir -p ../_archive/core

# Archive legacy modules
mv config_loaderv1.py \
   curator_router_backup.py \
   schema_selector_backup.py \
   schemas_OLD.py \
   ui_components.py \
   ingestion_engine_corebuild.py \
   ../_archive/core 2>/dev/null

# Archive macOS & metadata files
mv ._*.py .DS_Store ../_archive/core 2>/dev/null

echo "✅ core/ cleaned and archived successfully."
