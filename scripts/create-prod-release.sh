#!/bin/bash

# Production Release Script for Trunk-Based Development
# Usage: ./scripts/create-prod-release.sh <version>
# Example: ./scripts/create-prod-release.sh 1.0.0

set -e

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "❌ Error: Version is required"
    echo "Usage: $0 <version>"
    echo "Example: $0 1.0.0"
    exit 1
fi

# Validate version format (semantic versioning)
if ! [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "❌ Error: Version must follow semantic versioning (e.g., 1.0.0)"
    exit 1
fi

TAG_NAME="prod/v$VERSION"

echo "🚀 Creating production release: $TAG_NAME"
echo ""

# Check if we're on main/master branch
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" != "main" && "$CURRENT_BRANCH" != "master" ]]; then
    echo "❌ Error: You must be on main or master branch to create a production release"
    echo "Current branch: $CURRENT_BRANCH"
    exit 1
fi

# Check if working directory is clean
if ! git diff-index --quiet HEAD --; then
    echo "❌ Error: Working directory is not clean. Please commit or stash your changes."
    git status --short
    exit 1
fi

# Check if tag already exists
if git tag -l | grep -q "^$TAG_NAME$"; then
    echo "❌ Error: Tag $TAG_NAME already exists"
    exit 1
fi

echo "✅ Pre-checks passed:"
echo "   - On main/master branch: $CURRENT_BRANCH"
echo "   - Working directory is clean"
echo "   - Tag $TAG_NAME does not exist"
echo ""

# Run pre-deployment checks
echo "🔍 Running pre-deployment checks..."
if ! make pre-deploy; then
    echo "❌ Pre-deployment checks failed. Aborting release creation."
    exit 1
fi

echo ""
echo "✅ All checks passed! Creating production release..."

# Create and push the tag
git tag -a "$TAG_NAME" -m "Production release $VERSION"
git push origin "$TAG_NAME"

echo ""
echo "🎉 Production release $TAG_NAME created and pushed!"
echo ""
echo "📋 Next steps:"
echo "   1. GitHub Actions will automatically:"
echo "      - Run quality checks and tests"
echo "      - Build and deploy to production"
echo "      - Create a GitHub release"
echo ""
echo "   2. Monitor the deployment:"
echo "      - Check GitHub Actions: https://github.com/$GITHUB_REPOSITORY/actions"
echo "      - Check Cloud Run logs in Google Cloud Console"
echo ""
echo "   3. Verify the release:"
echo "      - Check GitHub releases: https://github.com/$GITHUB_REPOSITORY/releases"
echo "      - Test the production API endpoints"
echo ""
echo "🔗 Useful links:"
echo "   - GitHub Actions: https://github.com/$GITHUB_REPOSITORY/actions"
echo "   - Releases: https://github.com/$GITHUB_REPOSITORY/releases"
