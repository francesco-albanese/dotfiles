#!/bin/bash
# Ralph Wiggum Bootstrap Script
# Creates scripts/ralph/ directory and copies the tracker-specific prompt template.
#
# Usage: bootstrap.sh [github|beads]
# Default: github

set -e

BACKEND="${1:-github}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$(cd "$SCRIPT_DIR/../assets/templates" && pwd)"
TARGET_DIR="scripts/ralph"

case "$BACKEND" in
    github|beads) ;;
    *)
        echo "Error: unknown backend '$BACKEND' (expected: github or beads)"
        exit 1
        ;;
esac

SOURCE_FILE="$TEMPLATE_DIR/prompt-$BACKEND.md"

if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: template not found: $SOURCE_FILE"
    exit 1
fi

mkdir -p "$TARGET_DIR"
cp "$SOURCE_FILE" "$TARGET_DIR/prompt.md"

NOTIFY_EXAMPLE="$TEMPLATE_DIR/notify.env.example"
if [ -f "$NOTIFY_EXAMPLE" ] && [ ! -f "$TARGET_DIR/notify.env.example" ]; then
    cp "$NOTIFY_EXAMPLE" "$TARGET_DIR/notify.env.example"
fi

echo "Ralph template ($BACKEND) copied to $TARGET_DIR/prompt.md"
echo ""
echo "Files created:"
echo "  - $TARGET_DIR/prompt.md (Claude instructions, tracker=$BACKEND)"
echo "  - $TARGET_DIR/notify.env.example (WhatsApp notify template; copy to notify.env to enable)"
echo ""
echo "Tip: copy notify.env.example -> notify.env and fill in CallMeBot creds to get WhatsApp pings when AFK runs finish."
echo ""
echo "Next steps:"
echo "  1. Run: ralph-once (single iteration)"
echo "  2. Or:  afk-ralph (10 iterations)"
