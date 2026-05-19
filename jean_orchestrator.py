#!/usr/bin/env python3
"""
Jean Team Orchestrator
Coordinates multi-model collaboration following defined roles and workflows.
"""

import yaml
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class JeanTeam:
    """Orchestrates collaboration between Jean-Claude, Jean-Jacques, and Jean-Pierre."""
    
    def __init__(self, config_path: str = "jean-team-config.yaml"):
        """Initialize the Jean Team with configuration."""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.team = self.config['team']
        self.workflow = self.config['workflow']
        self.task_log = []
        
    def get_role_info(self, role: str) -> Dict:
        """Get information about a specific role."""
        return self.team.get(role, {})
    
    def get_model_for_role(self, role: str, complexity: str = "default") -> str:
        """
        Get the appropriate model for a role based on complexity.
        
        Args:
            role: The role (project_manager, architect, developer)
            complexity: "default", "heavy", or "quick"
        
        Returns:
            Model identifier string
        """
        role_info = self.get_role_info(role)
        
        if complexity == "heavy" and "model_heavy" in role_info:
            return role_info["model_heavy"]
        elif complexity == "quick" and "model_quick" in role_info:
            return role_info["model_quick"]
        else:
            return role_info.get("model", "")
    
    def delegate_task(self, task: str, from_role: str, to_role: str) -> Dict:
        """Delegate a task from one role to another."""
        delegation = {
            "timestamp": datetime.utcnow().isoformat(),
            "task": task,
            "from": self.team[from_role]["name"],
            "to": self.team[to_role]["name"],
            "model": self.get_model_for_role(to_role)
        }
        
        self.task_log.append(delegation)
        return delegation
    
    def initiate_task(self, user_request: str) -> Dict:
        """
        Jean-Claude (Project Manager) initiates a task.
        
        Returns:
            Task breakdown and delegation plan
        """
        return {
            "phase": "initiation",
            "owner": self.team["project_manager"]["name"],
            "request": user_request,
            "status": "assessing",
            "next_step": "delegate_to_architect"
        }
    
    def plan_task(self, task_context: Dict) -> Dict:
        """
        Jean-Jacques (Architect) plans the implementation.
        
        Returns:
            Implementation plan
        """
        return {
            "phase": "planning",
            "owner": self.team["architect"]["name"],
            "model": self.get_model_for_role("architect"),
            "context": task_context,
            "status": "planning",
            "deliverables": [
                "Architecture design",
                "Best practices research",
                "Implementation plan",
                "Success criteria"
            ]
        }
    
    def implement_task(self, plan: Dict) -> Dict:
        """
        Jean-Pierre (Developer) implements the code.
        
        Returns:
            Implementation details
        """
        return {
            "phase": "implementation",
            "owner": self.team["developer"]["name"],
            "model": self.get_model_for_role("developer"),
            "plan": plan,
            "status": "coding",
            "deliverables": [
                "Implementation code",
                "Unit tests",
                "Documentation"
            ]
        }
    
    def code_review(self, code_path: str) -> Dict:
        """
        All Jean models review the code.
        
        Returns:
            Review results from all models
        """
        review_config = self.config['code_review']
        
        if not review_config['enabled']:
            return {"status": "skipped", "reason": "Code review disabled"}
        
        reviews = {}
        
        # Each role reviews from their perspective
        for role_key, role_data in self.team.items():
            reviews[role_data['name']] = {
                "model": role_data['model'],
                "perspective": role_key,
                "status": "pending"
            }
        
        return {
            "phase": "review",
            "code_path": code_path,
            "reviews": reviews,
            "all_models_participate": review_config['all_models_review']
        }
    
    def should_notify_boss(self, issue_type: str) -> bool:
        """Check if boss should be notified for this issue type."""
        pm_config = self.team['project_manager']
        notify_triggers = pm_config.get('escalate_to_boss', [])
        
        code_review_config = self.config['code_review']
        notify_on = code_review_config.get('notify_boss_on', [])
        
        return (issue_type in notify_triggers or 
                issue_type in notify_on)
    
    def get_task_log(self) -> List[Dict]:
        """Get the full task delegation log."""
        return self.task_log
    
    def export_log(self, filepath: str = "jean-team-log.json"):
        """Export task log to JSON file."""
        with open(filepath, 'w') as f:
            json.dump({
                "timestamp": datetime.utcnow().isoformat(),
                "tasks": self.task_log
            }, f, indent=2)


def main():
    """Example usage of Jean Team orchestrator."""
    team = JeanTeam()
    
    # Example: User request comes in
    print("=== Jean Team Orchestrator ===\n")
    
    print("Team Structure:")
    for role_key, role_data in team.team.items():
        print(f"  {role_data['name']} ({role_key}): {role_data['model']}")
    
    print("\nWorkflow Phases:")
    for phase in team.workflow['phases']:
        print(f"  {phase['name']}: owned by {phase['owner']}")
    
    # Simulate a task
    task = team.initiate_task("Build a user authentication system")
    print(f"\n1. Task Initiated by {task['owner']}")
    print(f"   Request: {task['request']}")
    
    # Delegate to architect
    delegation = team.delegate_task(
        "Design authentication system architecture",
        "project_manager",
        "architect"
    )
    print(f"\n2. Delegated to {delegation['to']}")
    print(f"   Model: {delegation['model']}")
    
    # Plan phase
    plan = team.plan_task(task)
    print(f"\n3. Planning by {plan['owner']}")
    print(f"   Deliverables: {', '.join(plan['deliverables'])}")
    
    # Implementation
    impl = team.implement_task(plan)
    print(f"\n4. Implementation by {impl['owner']}")
    print(f"   Model: {impl['model']}")
    
    # Code review
    review = team.code_review("example_code.py")
    print(f"\n5. Code Review:")
    for reviewer, details in review['reviews'].items():
        print(f"   {reviewer} ({details['perspective']}): {details['status']}")
    
    # Export log
    team.export_log()
    print(f"\nTask log exported to jean-team-log.json")


if __name__ == "__main__":
    main()
