#!/usr/bin/env python3
"""
Agent List Generator
Automatically extracts and generates agent list from /root/.claude/agents/ directory
"""

import re
import yaml
import sys
from datetime import datetime
from pathlib import Path

def extract_agent_info_from_md(file_path):
    """Extract agent information from a markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    agent_name = file_path.stem  # Get filename without extension
    
    # Try to extract YAML frontmatter if exists
    yaml_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    metadata = {}
    description = ""
    
    if yaml_match:
        try:
            # Try to parse YAML
            yaml_content = yaml_match.group(1)
            metadata = yaml.safe_load(yaml_content)
            
            # Get FULL description from YAML frontmatter
            if metadata and 'description' in metadata:
                description = metadata['description']
                # Keep the full description, don't truncate it
        except yaml.YAMLError:
            # If YAML parsing fails, try to extract description manually
            metadata = {}
            # Look for description: line in the frontmatter
            desc_match = re.search(r'^description:\s*(.+?)(?=\n[a-z]+:|$)', yaml_match.group(1), re.MULTILINE | re.DOTALL)
            if desc_match:
                description = desc_match.group(1).strip()
    
    # If no description from YAML, try to find in content
    if not description:
        # Try to find Role & Mission section
        role_pattern = r'# Role & Mission\n+(.*?)(?:\n\n|\n#)'
        match = re.search(role_pattern, content, re.MULTILINE | re.DOTALL)
        if match:
            description = match.group(1).strip()
    
    # Check if consolidated or optimized
    is_consolidated = 'consolidated-' in agent_name or '[CONSOLIDATED]' in content
    is_optimized = 'optimized-' in agent_name or '[OPTIMIZED]' in content
    
    return {
        'name': agent_name,
        'description': description,  # Full description, no truncation
        'consolidated': is_consolidated,
        'optimized': is_optimized,
        'file': file_path.name,
        'metadata': metadata
    }


def scan_agents_directory():
    """Scan the agents directory for all agent definitions"""
    agents_dir = Path("/root/.claude/agents")
    
    if not agents_dir.exists():
        print(f"Error: Agents directory not found at {agents_dir}")
        return []
    
    agents = []
    
    # Files to exclude (generated files, not actual agents)
    exclude_files = {'AGENT_DIRECTORY.md', 'agent-catalog.json', 'agent-list.txt'}
    
    # Scan for .md files
    for file_path in agents_dir.glob("*.md"):
        # Skip excluded files
        if file_path.name in exclude_files:
            continue
            
        try:
            agent_info = extract_agent_info_from_md(file_path)
            agents.append(agent_info)
            print(f"  ✓ Processed: {file_path.name}")
        except Exception as e:
            print(f"  ✗ Error processing {file_path.name}: {e}")
    
    return agents

def generate_markdown_summary(agents):
    """Generate markdown formatted agent summary with full descriptions"""
    content = []
    content.append("# Available Agents Directory")
    content.append(f"\n*Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    content.append(f"\n**Total Agents: {len(agents)}**")
    
    # Statistics
    consolidated_count = sum(1 for a in agents if a['consolidated'])
    optimized_count = sum(1 for a in agents if a['optimized'])
    content.append(f"\n- Consolidated: {consolidated_count}")
    content.append(f"- Optimized: {optimized_count}")
    content.append(f"- Standard: {len(agents) - consolidated_count - optimized_count}")
    
    content.append("\n## All Agents\n")
    
    # List all agents alphabetically
    for agent in sorted(agents, key=lambda x: x['name']):
        # Determine type badge
        badges = []
        if agent['consolidated']:
            badges.append("🔧 Consolidated")
        if agent['optimized']:
            badges.append("⚡ Optimized")
        badge_str = f" *({', '.join(badges)})*" if badges else ""
        
        content.append(f"### `{agent['name']}`{badge_str}")
        content.append("")
        
        # Add full description (already includes examples)
        content.append(agent['description'])
        content.append("")
        content.append("---")
        content.append("")
    
    return '\n'.join(content)


def generate_simple_list(agents):
    """Generate simple text list of agent names"""
    return '\n'.join(sorted([agent['name'] for agent in agents]))

def main():
    """Main function to generate agent lists"""
    print("🔍 Scanning /root/.claude/agents/ directory...")
    agents = scan_agents_directory()
    
    if not agents:
        print("❌ No agents found")
        return
    
    print(f"\n✅ Found {len(agents)} agents")
    
    # Determine output directory from command line argument or use default
    if len(sys.argv) > 1:
        output_dir = Path(sys.argv[1])
    else:
        output_dir = Path("/root/.claude/data")
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Output directory: {output_dir}")
    
    # Generate markdown summary with full descriptions
    markdown_content = generate_markdown_summary(agents)
    markdown_path = output_dir / "AGENT_DIRECTORY.md"
    with open(markdown_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    print(f"📄 Generated markdown directory: {markdown_path}")
    
    # Generate simple list
    list_content = generate_simple_list(agents)
    list_path = output_dir / "agent-list.txt"
    with open(list_path, 'w', encoding='utf-8') as f:
        f.write(list_content)
    print(f"📝 Generated simple list: {list_path}")
    
    # Print summary
    print("\n📈 Summary:")
    consolidated = sum(1 for a in agents if a['consolidated'])
    optimized = sum(1 for a in agents if a['optimized'])
    standard = len(agents) - consolidated - optimized
    
    print(f"  - Total: {len(agents)} agents")
    print(f"  - Consolidated: {consolidated} agents")
    print(f"  - Optimized: {optimized} agents")
    print(f"  - Standard: {standard} agents")

if __name__ == "__main__":
    main()