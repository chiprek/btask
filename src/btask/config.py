import json
from pathlib import Path
from typing import Any, Dict, List

from platformdirs import user_config_dir, user_data_dir


class BTaskConfig:
    """Handle configuration and data storage for btask"""

    def __init__(self):
        # Platform-appropriate directories
        self.config_dir = Path(user_config_dir("btask"))
        self.data_dir = Path(user_data_dir("btask"))

        # Create directories if they don't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Define file paths
        self.config_file = self.config_dir / "config.json"
        self.projects_file = self.data_dir / "projects.json"

        # Initialize files with defaults if they don't exist
        self._initialize_files()

    def _initialize_files(self) -> None:
        """Create default files if they don't exist"""
        if not self.config_file.exists():
            default_config = {
                "theme": "crt_orange",
                "auto_save": True,
                "sidebar_visible": True,
                "last_project": None,
            }
            self.save_config(default_config)

        if not self.projects_file.exists():
            # Empty project list - will be populated from Excel or manually
            with open(self.projects_file, "w") as f:
                json.dump([], f, indent=2)

    # Config methods
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        with open(self.config_file, "r") as f:
            return json.load(f)

    def save_config(self, config_data: Dict[str, Any]) -> None:
        """Save configuration to file"""
        with open(self.config_file, "w") as f:
            json.dump(config_data, f, indent=2)

    def update_config(self, key: str, value: Any) -> None:
        """Update a single config value"""
        config = self.load_config()
        config[key] = value
        self.save_config(config)

    # Project methods
    def load_projects(self) -> List[Dict[str, Any]]:
        """Load all projects from file"""
        if self.projects_file.exists():
            with open(self.projects_file, "r") as f:
                return json.load(f)
        return []

    def save_projects(self, projects: List[Dict[str, Any]]) -> None:
        """Save all projects to file"""
        with open(self.projects_file, "w") as f:
            json.dump(projects, f, indent=2)

    def get_project_by_id(self, project_id: str) -> Dict[str, Any] | None:
        """Get a specific project by its ID"""
        projects = self.load_projects()
        for project in projects:
            if project.get("id") == project_id:
                return project
        return None

    def add_project(self, project: Dict[str, Any]) -> None:
        """Add a new project"""
        projects = self.load_projects()
        projects.append(project)
        self.save_projects(projects)

    def update_project(self, project_id: str, updated_project: Dict[str, Any]) -> bool:
        """Update an existing project. Returns True if successful."""
        projects = self.load_projects()
        for i, project in enumerate(projects):
            if project.get("id") == project_id:
                projects[i] = updated_project
                self.save_projects(projects)
                return True
        return False

    def delete_project(self, project_id: str) -> bool:
        """Delete a project. Returns True if successful."""
        projects = self.load_projects()
        filtered = [p for p in projects if p.get("id") != project_id]
        if len(filtered) < len(projects):
            self.save_projects(filtered)
            return True
        return False
