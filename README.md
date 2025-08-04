# Don't Panic Just Breathe

A documentation website built with MkDocs containing UPSC preparation resources, strategies, and study materials.

## Features

- Material Design theme with light/dark mode toggle
- Search functionality across all content
- MathJax support for mathematical equations
- Mermaid diagrams support
- Responsive design for mobile and desktop
- Google Analytics integration

## Content

This site contains:

- **UPSC Strategy**: Study strategies for different subjects
- **UPSC Resources**: 
  - Ethics and Essay materials
  - General Studies topicwise previous year questions
  - Mathematics notes and previous year questions
  - Prelims Android application information

## Development

### Prerequisites

Install Python dependencies:
```bash
pip install mkdocs mkdocs-material mkdocs-roamlinks-plugin mkdocs-video
```

### Local Development

1. **Start development server:**
   ```bash
   mkdocs serve
   ```
   Visit `http://127.0.0.1:8000` to view the site locally.

2. **Build for production:**
   ```bash
   mkdocs build
   ```
   Generated files will be in the `site/` directory.

### Deployment

**GitHub Pages:**
```bash
mkdocs gh-deploy
```

**Manual deployment:**
Upload the contents of the `site/` folder to your web server after running `mkdocs build`.

## Configuration

### Site Structure

Content is organized in the `docs/` folder:
- Navigation is configured in `mkdocs.yml`
- Pages follow the folder structure or custom navigation
- First-level markdown headings become page titles

### Customization

- **Theme**: Edit `mkdocs.yml` to modify colors, features, and layout
- **Navigation**: Update the `nav` section in `mkdocs.yml`
- **Analytics**: Google Analytics is pre-configured
- **Custom CSS/JS**: Add files to `overrides/` directory

## Contributing

1. Fork the repository
2. Make your changes in the `docs/` folder
3. Test locally with `mkdocs serve`
4. Submit a pull request

## License

See [LICENSE](LICENSE) file for details.

