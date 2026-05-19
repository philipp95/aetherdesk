#!/bin/bash
# Jean Team Workflow Script
# Demonstrates practical usage of the multi-model collaboration system

set -e

WORKSPACE="/home/philipp/.openclaw/workspace"
CONFIG="$WORKSPACE/jean-team-config.yaml"
LOG_FILE="$WORKSPACE/jean-team-activity.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_jean() {
    local jean_name=$1
    local message=$2
    echo -e "${BLUE}[$jean_name]${NC} $message" | tee -a "$LOG_FILE"
}

# Extract model info from config
get_model() {
    local role=$1
    python3 -c "
import yaml
with open('$CONFIG') as f:
    config = yaml.safe_load(f)
print(config['team']['$role']['model'])
"
}

# Jean-Claude (Project Manager) - Orchestration
jean_claude_orchestrate() {
    local task="$1"
    log_jean "Jean-Claude (PM)" "Received task: $task"
    log_jean "Jean-Claude (PM)" "Assessing scope and delegating to architect..."
    
    # Log to activity file
    echo "---" >> "$LOG_FILE"
    echo "TASK INITIATED: $task" >> "$LOG_FILE"
    echo "PM: Jean-Claude | Model: $(get_model project_manager)" >> "$LOG_FILE"
    echo "---" >> "$LOG_FILE"
}

# Jean-Jacques (Architect) - Planning
jean_jacques_plan() {
    local task="$1"
    log_jean "Jean-Jacques (Architect)" "Planning architecture for: $task"
    log_jean "Jean-Jacques (Architect)" "Researching best practices..."
    
    echo "PLANNING PHASE" >> "$LOG_FILE"
    echo "Architect: Jean-Jacques | Model: $(get_model architect)" >> "$LOG_FILE"
}

# Jean-Pierre (Developer) - Implementation
jean_pierre_implement() {
    local plan="$1"
    log_jean "Jean-Pierre (Developer)" "Implementing based on plan..."
    log_jean "Jean-Pierre (Developer)" "Following coding best practices..."
    
    echo "IMPLEMENTATION PHASE" >> "$LOG_FILE"
    echo "Developer: Jean-Pierre | Model: $(get_model developer)" >> "$LOG_FILE"
}

# Code Review - All Jeans participate
code_review_all() {
    local code_file="$1"
    log "=== CODE REVIEW PHASE ==="
    
    log_jean "Jean-Claude (PM)" "Reviewing for project alignment and efficiency..."
    log_jean "Jean-Jacques (Architect)" "Reviewing for architecture and standards..."
    log_jean "Jean-Pierre (Developer)" "Reviewing for code quality and testing..."
    
    echo "CODE REVIEW COMPLETE" >> "$LOG_FILE"
    echo "All models participated in review of: $code_file" >> "$LOG_FILE"
}

# Usage tracking
usage_summary() {
    log "=== USAGE SUMMARY ==="
    log "Jean-Claude calls: tracked in logs"
    log "Jean-Jacques calls: tracked in logs"
    log "Jean-Pierre calls: tracked in logs"
    log "See jean-team-activity.log for details"
}

# Main workflow demonstration
main() {
    echo -e "${GREEN}=== Jean Team Workflow ===${NC}"
    echo ""
    
    local task="${1:-Test task: Create a simple feature}"
    
    # Phase 1: Initiation
    jean_claude_orchestrate "$task"
    sleep 1
    
    # Phase 2: Planning
    jean_jacques_plan "$task"
    sleep 1
    
    # Phase 3: Implementation
    jean_pierre_implement "Architecture plan from Jean-Jacques"
    sleep 1
    
    # Phase 4: Review
    code_review_all "example_feature.py"
    sleep 1
    
    # Summary
    usage_summary
    
    echo ""
    echo -e "${GREEN}Workflow complete! Check jean-team-activity.log for details.${NC}"
}

# Run if called directly
if [ "${BASH_SOURCE[0]}" -ef "$0" ]; then
    main "$@"
fi
