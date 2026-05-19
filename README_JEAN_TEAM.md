# Jean Team - Multi-Model Collaboration System

A framework for coordinated work between multiple AI models, each with specific roles and responsibilities.

## The Team

### 👔 Jean-Claude (Claude/Anthropic) - Project Manager
**Current Model:** `anthropic/claude-sonnet-4-5`  
**Role:** Orchestration, coordination, boss communication, cost management

### 🏗️ Jean-Jacques (Gemini/Google) - Architect  
**Current Model:** `google/gemini-2.5-pro`  
**Role:** Technical design, research, planning, best practices

### 💻 Jean-Pierre (OpenAI/ChatGPT) - Developer
**Current Model:** `openai/gpt-5`  
**Role:** Implementation, testing, coding, execution

## Quick Start

### 1. Configuration
All roles and models are defined in `jean-team-config.yaml`. To change roles or responsibilities:

```bash
# Edit the config file
nano jean-team-config.yaml

# Or use the orchestrator to view current setup
python3 jean_orchestrator.py
```

### 2. Running a Task

#### Option A: Manual Workflow (for testing)
```bash
# Run the workflow demo
./jean_workflow.sh "Your task description here"

# Check the activity log
cat jean-team-activity.log
```

#### Option B: OpenClaw Session Spawning (production use)

In your OpenClaw chat, initiate the Jean Team workflow:

```
As Jean-Claude (Project Manager), I need to coordinate this task:
[your task description]

Please:
1. Assess the task and delegate to Jean-Jacques for planning
2. Have Jean-Jacques research and design the architecture
3. Have Jean-Pierre implement following the plan
4. All Jeans review the final code
5. Report back to me with results
```

The system will automatically:
- Spawn sub-agent sessions for each Jean with their specific model
- Follow the workflow phases
- Log all activities
- Notify you when attention is needed

## Workflow Phases

### Phase 1: Initiation (Jean-Claude)
- Receives request from boss (you)
- Assesses scope and complexity
- Delegates to appropriate team members
- Sets priorities

### Phase 2: Planning (Jean-Jacques)
- Researches best practices online
- Designs architecture
- Creates implementation plan
- Reports to Jean-Claude

### Phase 3: Implementation (Jean-Pierre)
- Follows Jean-Jacques' plan
- Writes clean, documented code
- Performs testing
- Prepares for review

### Phase 4: Review (All Jeans)
- Each model reviews from their perspective:
  - Jean-Claude: Project alignment, efficiency
  - Jean-Jacques: Architecture, standards
  - Jean-Pierre: Code quality, testing
- Issues flagged and addressed
- Boss notified if attention required

## Practical OpenClaw Integration

### Using sessions_spawn

The main agent (Jean-Claude) can spawn sub-agents for specific tasks:

```python
# Jean-Claude spawns Jean-Jacques for planning
sessions_spawn(
    task="Design authentication system architecture following best practices",
    model="google/gemini-2.5-pro",
    label="jean-jacques-planning",
    context="fork"
)

# Jean-Claude spawns Jean-Pierre for implementation  
sessions_spawn(
    task="Implement the authentication system following this plan: [plan]",
    model="openai/gpt-5",
    label="jean-pierre-implementation",
    context="isolated"
)
```

### Code Review Process

After Jean-Pierre commits code:

1. Jean-Claude checks for project alignment and cost efficiency
2. Jean-Jacques reviews architecture and adherence to plan
3. Jean-Pierre reviews his own work for code quality
4. Comments are added to the commit if issues found
5. Boss is notified if critical issues arise

### Cost Management

Jean-Claude tracks usage and prefers smaller models when appropriate:
- Simple tasks → `sonnet`, `flash`, `gpt-5-mini`
- Complex tasks → `opus`, `gemini-2.5-pro`, `gpt-5`

## Files in This System

- **JEAN_TEAM.md** - Team structure and responsibilities documentation
- **jean-team-config.yaml** - Role configuration (modify this to change roles)
- **jean_orchestrator.py** - Python orchestration library
- **jean_workflow.sh** - Bash workflow demonstration script
- **README_JEAN_TEAM.md** - This file
- **jean-team-activity.log** - Activity log (auto-generated)
- **jean-team-log.json** - Task delegation log (auto-generated)

## Modifying Roles

To change who does what:

1. Edit `jean-team-config.yaml`
2. Change the role assignments under `team:`
3. Modify responsibilities as needed
4. Save and the system picks up changes immediately

Example - swap roles:
```yaml
team:
  project_manager:
    name: "Jean-Jacques"  # Gemini is now PM
    model: "google/gemini-2.5-pro"
    # ... etc
```

## Boss Notifications

You will be notified when:
- Ambiguous requirements need clarification
- Technical blockers are encountered
- Significant cost implications arise
- Strategic decisions are needed
- Critical issues found in code review
- Security concerns identified

## Examples

### Example 1: Building a New Feature

**Boss request:** "Add user authentication to the Django app"

**Jean-Claude:** Assesses scope → delegates to Jean-Jacques  
**Jean-Jacques:** Researches Django auth best practices → creates plan  
**Jean-Pierre:** Implements authentication following plan → commits code  
**All:** Review code → Jean-Jacques flags a security issue → Boss notified  

### Example 2: Debugging

**Boss request:** "Fix the login bug"

**Jean-Claude:** Quick fix, uses smaller models to save cost  
**Jean-Pierre:** Debugs with `gpt-5-mini` → finds issue → fixes  
**Jean-Jacques:** Quick review with `flash` → approves  
**Jean-Claude:** Confirms and reports back to boss  

## Logs and Monitoring

All activities are logged:
```bash
# View recent activity
tail -f jean-team-activity.log

# View task delegation history
cat jean-team-log.json

# Check model usage
grep "Model:" jean-team-activity.log | sort | uniq -c
```

## Integration with Git

The Jean Team respects your Git workflow:
- Jean-Pierre commits implementation code
- All Jeans can add review comments via Git
- Jean-Claude handles communication with you about commits
- Automatic push when review passes

## Future Enhancements

- Automatic model selection based on task complexity
- Cost tracking and budget alerts
- Performance benchmarking between models
- Automated testing integration
- Multi-repo support

---

**Questions or issues?** Jean-Claude (the Project Manager) will escalate to you automatically.
