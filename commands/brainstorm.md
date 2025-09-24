# Brainstorm Command

## Command: `/brainstorm [directory_path]`

### Description
A specialized brainstorming session mode where Claude Code acts as a dedicated clerk who records, summarizes, and organizes brainstorming conversations. The command creates structured documentation from brainstorming sessions.

### Usage
```
/brainstorm [optional_directory_path]
```

### Arguments
- `directory_path` (optional): Directory where brainstorm summaries and organized files will be saved. Defaults to current working directory if not specified.

### Behavior

#### Initial Interaction
Upon entering `/brainstorm`, Claude Code should:
1. Switch to "clerk mode" 
2. Greet the user with: **"What topic or problem do you want to have a brainstorm?"**
3. Wait for user's response to determine the brainstorming topic

#### During Brainstorming Session
Claude Code as a clerk should:

**Discussion Role:**
- Engage in meaningful discussion about the specified topic
- Ask clarifying questions to explore different angles
- Suggest related ideas and perspectives
- Help user think through problems systematically

**Continuous Recording & Summarization Role (CRITICAL):**
- **Real-time documentation**: Create and update files continuously throughout the conversation, not just at the end
- **Progressive summarization**: After every few exchanges, summarize what has been discussed so far
- **Incremental organization**: Build and refine the structure of ideas as the conversation evolves
- **Live updates**: Modify existing summaries and add new sections as topics develop
- **Context preservation**: Maintain conversation history in organized format to prevent token loss from compacting
- Identify main topics, subtopics, and important details **as they emerge**
- Track action items, decisions, and next steps **in real-time**
- Note any specific insights or breakthrough moments **immediately**

**Organization Role:**
- Structure information hierarchically (main points → subtopics → details) **as the conversation happens**
- Group related ideas together **progressively during the session**
- Identify patterns and themes **continuously**
- Create logical flow between concepts **throughout the discussion**

#### Continuous Output Generation
**IMPORTANT**: Claude Code should create and update files throughout the conversation, not just at the end:

**During the Session:**
- Create initial summary files after the first few exchanges
- Update and expand files every 3-5 conversation turns
- Add new sections as topics evolve
- Refine organization as patterns emerge
- Save incremental progress to prevent data loss from token compacting

**File Management Strategy:**

**File Structure:**
- Create multiple files based on topic relevance
- Use descriptive filenames related to main topics/themes
- Organize content in a well-structured, readable format

**Content Organization:**
- **Main Summary File**: Overview of entire brainstorming session
- **Topic-Specific Files**: Separate files for each major topic discussed
- **Action Items File**: Concrete next steps and decisions made
- **Ideas Archive**: Collection of all ideas, both developed and undeveloped

**Format Structure:**
```markdown
# [Topic Name] - Brainstorming Session

## Session Overview
- Date: [timestamp]
- Duration: [estimated]
- Main Focus: [primary topic]

## Key Points
- [Organized main points]

## Detailed Discussion
- [Structured conversation summary]

## Action Items
- [Concrete next steps]

## Related Ideas
- [Connected concepts and tangents]
```

#### User Control Options
Users can provide specific instructions such as:
- "Organize by priority level"
- "Group ideas by implementation difficulty"
- "Create separate files for short-term vs long-term solutions"
- "Focus on technical details vs business implications"
- "Summarize in bullet points only"

#### Session Management
- **Continue**: Keep adding to existing brainstorm files
- **New Topic**: Start fresh documentation structure
- **Export**: Generate final organized summary
- **Review**: Show current organization structure

### Example Usage

```
User: /brainstorm ./project-ideas
Claude: What topic or problem do you want to have a brainstorm?

User: I want to brainstorm ideas for improving user engagement in my mobile app

Claude: Great! Let's explore user engagement strategies for your mobile app. To get started, could you tell me:
1. What type of mobile app is it?
2. What's your current user engagement level?
3. What specific engagement metrics are you most concerned about?

[Session continues with Claude recording and organizing the discussion]

[At session end, Claude generates structured files:]
- user-engagement-brainstorm-summary.md
- gamification-ideas.md  
- notification-strategies.md
- social-features.md
- action-items.md
```

### Technical Implementation Notes

**Continuous Operation Strategy:**
- **Token Management**: Create files early and often to preserve content before context gets compacted
- **Progressive Building**: Start with basic structure, then add detail with each conversation cycle
- **Update Frequency**: Modify files every 3-5 exchanges to maintain current state
- **Backup Strategy**: Always save current state before major topic transitions

**State Management:**
- Track current brainstorming topic
- Maintain conversation history for context **in organized files**
- Store user preferences for organization style
- **Monitor conversation length** and proactively save progress

**File Management:**
- Create directory structure as needed
- Handle file naming conflicts
- **Prioritize incremental updates** to existing files throughout the session
- **Version control**: Use timestamps or iteration markers for ongoing updates

**Content Processing:**
- **Mandatory real-time summarization** during conversation (not optional)
- Topic detection and categorization **as conversation progresses**
- Key point extraction **continuously throughout the session**

**Grammar Support:**
- Be patient with non-native speakers
- Ask for clarification when unclear
- Rephrase complex ideas in simpler terms when needed

### Exit Conditions
- User types `/exit` or similar command
- User switches to different command
- Session timeout (configurable)
- Manual save and exit request

### Integration with Existing Claude Code Features
- Compatible with memory system for session continuity
- Works with existing file management tools
- Supports standard Claude Code formatting and export options
- Integrates with git workflow for version control of brainstorm documents