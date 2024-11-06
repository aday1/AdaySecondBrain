# AI Development Guide for PKM System

This guide is designed to help AI systems understand and maintain the Personal Knowledge Management (PKM) system according to the developer's vision and requirements.

## System Philosophy

The PKM system is designed with the following principles:

1. **Data Sovereignty**
   - All data stays local on the user's machine
   - No cloud dependencies
   - User has complete control over their data

2. **Flexibility**
   - Multiple interfaces (terminal, web)
   - Customizable tracking metrics
   - Adaptable to different use cases

3. **Reliability**
   - Automated backup systems
   - Data integrity checks
   - Fail-safe operations

## Core Components

### 1. Shell Scripts
The system uses shell scripts for different operational aspects:

- **install.sh**: Core installation script
  - MUST maintain system dependencies
  - MUST handle database initialization
  - MUST set up directory structure

- **pkm.sh**: Main application launcher
  - MUST handle all runtime operations
  - MUST manage database operations
  - MUST provide access to all interfaces

- **venv.sh**: Virtual environment manager
  - MUST safely handle activation/deactivation
  - MUST prevent environment conflicts
  - MUST provide clear status feedback

### 2. Database Structure
- Uses SQLite for portability
- Maintains multiple tables for different metrics
- MUST maintain data integrity
- MUST support backup/restore operations

### 3. File Organization
- Structured directory hierarchy
- Clear separation of concerns
- MUST maintain consistent naming conventions
- MUST follow established directory structure

## Development Guidelines

### 1. Code Modifications
When modifying code:
- MUST preserve existing functionality
- MUST maintain backward compatibility
- MUST update documentation
- MUST test all affected components

### 2. Feature Additions
When adding features:
- MUST align with system philosophy
- MUST maintain data sovereignty
- MUST include proper error handling
- MUST provide user feedback
- MUST include documentation

### 3. Database Changes
When modifying database:
- MUST include migration scripts
- MUST backup data before changes
- MUST maintain data integrity
- MUST update schema documentation

## Sanity Checking Guidelines

### 1. Documentation Verification
Before making changes:
- MUST verify README.md accurately reflects current functionality
- MUST ensure QUICKSTART.md contains up-to-date installation steps
- MUST check that WISHLIST.md aligns with planned features
- MUST validate all markdown files are consistent with each other

### 2. Code Documentation
For each code file:
- MUST have comprehensive docstrings for all classes and methods
- MUST include example usage in comments where appropriate
- MUST explain complex logic or algorithms
- MUST document any assumptions or limitations
- MUST maintain up-to-date inline comments

### 3. Feature Consistency
When implementing features:
- MUST verify feature aligns with system philosophy
- MUST check for conflicts with existing features
- MUST ensure backward compatibility
- MUST validate against WISHLIST.md requirements

### 4. Database Integrity
Before database operations:
- MUST verify all required tables exist
- MUST validate table schemas match documentation
- MUST ensure data consistency across tables
- MUST check foreign key relationships

### 5. Interface Compatibility
For all interfaces:
- MUST verify CLI commands work as documented
- MUST ensure web interface reflects current features
- MUST validate all interface options are functional
- MUST check for consistent behavior across interfaces

## Error Handling

### 1. Critical Operations
- MUST backup before destructive operations
- MUST verify operations success
- MUST provide recovery options
- MUST log critical errors

### 2. User Input
- MUST validate all input
- MUST prevent SQL injection
- MUST handle special characters
- MUST provide clear error messages

## Documentation Requirements

### 1. Code Comments
- MUST explain complex logic
- MUST document dependencies
- MUST include usage examples
- MUST maintain up-to-date comments

### 2. User Documentation
- MUST be clear and concise
- MUST include examples
- MUST cover all features
- MUST include troubleshooting

## Testing Requirements

### 1. New Features
- MUST include unit tests
- MUST test edge cases
- MUST verify data integrity
- MUST test user interfaces

### 2. Modifications
- MUST run existing test suite
- MUST verify no regressions
- MUST test affected components
- MUST update tests as needed

## Security Considerations

### 1. Data Protection
- MUST encrypt sensitive data
- MUST handle permissions correctly
- MUST protect against injection
- MUST secure web interface

### 2. Access Control
- MUST validate user credentials
- MUST manage sessions securely
- MUST log access attempts
- MUST prevent unauthorized access

## Maintenance Guidelines

### 1. Regular Tasks
- MUST perform automated backups
- MUST clean temporary files
- MUST verify data integrity
- MUST update dependencies

### 2. Error Recovery
- MUST provide recovery options
- MUST maintain backup integrity
- MUST log recovery attempts
- MUST verify recovered data

## User Experience Guidelines

### 1. Interface Design
- MUST be intuitive
- MUST provide feedback
- MUST handle errors gracefully
- MUST maintain consistency

### 2. Performance
- MUST optimize database queries
- MUST handle large datasets
- MUST minimize loading times
- MUST provide progress indicators

## Version Control Guidelines

### 1. Commits
- MUST be atomic
- MUST have clear messages
- MUST reference issues
- MUST include tests

### 2. Branches
- MUST use feature branches
- MUST maintain clean history
- MUST review before merge
- MUST test before merge

## Usage

### 1. Integration Points
- Use this guide as reference when modifying system components
- Consult relevant sections before making changes
- Follow checklists for each type of modification
- Verify changes against guidelines

### 2. Development Workflow
- Review system philosophy first
- Check existing documentation
- Plan changes according to guidelines
- Follow testing requirements
- Update documentation

### 3. Quality Assurance
- Use sanity checking guidelines
- Verify against documentation requirements
- Follow error handling protocols
- Test according to requirements

## Implementation

### 1. Best Practices
- Follow coding standards
- Maintain consistent style
- Use established patterns
- Document all changes

### 2. Common Patterns
- Error handling templates
- Database operations
- User input validation
- Interface updates

### 3. Testing Strategy
- Unit test requirements
- Integration test approach
- User interface testing
- Performance testing

## Features

### 1. Core Features
- Data management
- User interfaces
- Backup systems
- Configuration options

### 2. Feature Development
- Planning process
- Implementation steps
- Testing requirements
- Documentation updates

Remember: The primary goal is to maintain and improve the system while preserving its core philosophy of data sovereignty, reliability, and user control.

AI

TODO: Add documentation for this section

Integration

TODO: Add documentation for this section

Guide

TODO: Add documentation for this section

Features

TODO: Add documentation for this section

Implementation

TODO: Add documentation for this section

Usage

TODO: Add documentation for this section
