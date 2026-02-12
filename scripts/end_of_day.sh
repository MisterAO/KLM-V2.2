#!/bin/bash
#
# End-of-Day Refactoring and Documentation Script
# Run this at the end of each development day to ensure code quality
#

echo "🌅 KLM V2 End-of-Day Refactoring and Documentation"
echo "=================================================="
echo "📅 Date: $(date '+%Y-%m-%d')"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found"
    exit 1
fi

# Check if the end-of-day script exists
if [ ! -f "scripts/end_of_day.py" ]; then
    echo "❌ End-of-day script not found"
    exit 1
fi

# Run the end-of-day script
echo "🔄 Running end-of-day processing..."
python3 scripts/end_of_day.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ End-of-day processing completed successfully"
else
    echo ""
    echo "⚠️  End-of-day processing completed with issues"
fi

echo ""
echo "💡 Next steps:"
echo "  1. Review any changes made"
echo "  2. Run 'git status' to see what needs to be committed"
echo "  3. Commit any documentation or code quality improvements"
echo ""
echo "✨ Have a great evening!"