# Ayu-watch

A modern file watcher and development tool featuring the beautiful Ayu color scheme, designed to monitor file changes and provide an elegant developer experience.

## Overview

Ayu-watch combines the aesthetic beauty of the Ayu color palette with powerful file watching capabilities. Whether you're developing web applications, writing scripts, or managing configuration files, Ayu-watch provides real-time feedback with a visually pleasing interface inspired by the popular Ayu theme.

## Features

- **Real-time File Monitoring**: Watch files and directories for changes with instant notifications
- **Ayu Theme Integration**: Three beautiful color schemes (Dark, Mirage, and Light) for comfortable viewing in any lighting condition
- **Cross-platform Support**: Works seamlessly on Windows, macOS, and Linux
- **Customizable Watch Patterns**: Define specific file types, directories, or glob patterns to monitor
- **Event Filtering**: Choose which file system events to track (create, modify, delete, rename)
- **Low Resource Usage**: Efficient monitoring that doesn't slow down your system
- **Terminal UI**: Beautiful terminal interface with color-coded output
- **Plugin System**: Extend functionality with custom plugins and integrations

## Installation

### Using npm

```bash
npm install -g ayu-watch
```

### Using yarn

```bash
yarn global add ayu-watch
```

### From Source

```bash
git clone https://github.com/WIZARD3022/Ayu-watch.git
cd Ayu-watch
npm install
npm link
```

## Quick Start

Watch the current directory for changes:

```bash
ayu-watch
```

Watch a specific directory:

```bash
ayu-watch ./src
```

Watch with a specific theme:

```bash
ayu-watch --theme mirage
```

## Usage

### Basic Commands

```bash
# Watch current directory
ayu-watch

# Watch specific directory
ayu-watch <path>

# Watch multiple directories
ayu-watch ./src ./config ./public

# Watch with specific file extensions
ayu-watch --ext js,jsx,ts,tsx

# Ignore specific patterns
ayu-watch --ignore "node_modules/**,*.log"
```

### Command Line Options

| Option | Alias | Description | Default |
|--------|-------|-------------|---------|
| `--theme` | `-t` | Color theme (dark, mirage, light) | `dark` |
| `--ext` | `-e` | File extensions to watch | `*` |
| `--ignore` | `-i` | Patterns to ignore | `node_modules` |
| `--events` | `-v` | Events to watch (add, change, unlink) | `all` |
| `--recursive` | `-r` | Watch directories recursively | `true` |
| `--depth` | `-d` | Maximum recursion depth | `infinite` |
| `--quiet` | `-q` | Minimal output | `false` |
| `--verbose` | `-V` | Detailed logging | `false` |
| `--config` | `-c` | Path to config file | `.ayuwatch.json` |

### Configuration File

Create a `.ayuwatch.json` file in your project root:

```json
{
  "theme": "mirage",
  "watch": ["./src", "./config"],
  "ignore": ["**/*.log", "node_modules/**", ".git/**"],
  "extensions": [".js", ".jsx", ".ts", ".tsx", ".json"],
  "events": ["add", "change", "unlink"],
  "recursive": true,
  "depth": 10,
  "actions": [
    {
      "pattern": "**/*.js",
      "command": "npm run lint"
    },
    {
      "pattern": "**/*.test.js",
      "command": "npm test"
    }
  ]
}
```

## Advanced Features

### Custom Actions

Define actions that trigger automatically when specific files change:

```json
{
  "actions": [
    {
      "pattern": "src/**/*.scss",
      "command": "npm run build:css",
      "debounce": 300
    },
    {
      "pattern": "src/**/*.js",
      "command": "npm run build:js",
      "debounce": 500
    }
  ]
}
```

### Programmatic Usage

Use Ayu-watch in your Node.js applications:

```javascript
const AyuWatch = require('ayu-watch');

const watcher = new AyuWatch({
  paths: ['./src'],
  theme: 'mirage',
  ignore: ['node_modules'],
  events: ['change', 'add']
});

watcher.on('change', (path) => {
  console.log(`File changed: ${path}`);
});

watcher.on('add', (path) => {
  console.log(`File added: ${path}`);
});

watcher.start();
```

### Plugin Development

Extend Ayu-watch with custom plugins:

```javascript
// plugins/custom-notifier.js
module.exports = {
  name: 'custom-notifier',
  
  init(watcher, options) {
    watcher.on('change', (path) => {
      // Send desktop notification
      this.notify(`File changed: ${path}`);
    });
  },
  
  notify(message) {
    // Your notification logic here
  }
};
```

Load plugins in your configuration:

```json
{
  "plugins": [
    "./plugins/custom-notifier.js"
  ]
}
```

## Color Themes

### Ayu Dark
Perfect for low-light environments with high contrast and vibrant colors.

### Ayu Mirage
A balanced middle ground with softer colors, ideal for extended coding sessions.

### Ayu Light
Clean and crisp for bright environments, easy on the eyes during daytime work.

## Examples

### Watch and Build on Change

```bash
ayu-watch ./src --ext js,jsx --command "npm run build"
```

### Monitor Configuration Files

```bash
ayu-watch ./config --events change --verbose
```

### Development Workflow

```bash
ayu-watch ./src --theme mirage --ext ts,tsx --command "npm run dev"
```

## Troubleshooting

### High CPU Usage

If you experience high CPU usage, try reducing the watch scope:

```bash
ayu-watch ./src --depth 5 --ignore "**/*.log,**/dist/**"
```

### Events Not Triggering

Ensure your file system supports file watching and check permissions:

```bash
ayu-watch --verbose
```

### Theme Not Displaying Correctly

Make sure your terminal supports 256 colors:

```bash
echo $TERM
```

If not, try setting it:

```bash
export TERM=xterm-256color
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
git clone https://github.com/WIZARD3022/Ayu-watch.git
cd Ayu-watch
npm install
npm run dev
```

### Running Tests

```bash
npm test
```

### Code Style

This project follows the Airbnb JavaScript Style Guide. Run the linter before committing:

```bash
npm run lint
```

## Dependencies

- [chokidar](https://github.com/paulmillr/chokidar) - Efficient file watching
- [chalk](https://github.com/chalk/chalk) - Terminal styling
- [commander](https://github.com/tj/commander.js) - Command-line interface
- [glob](https://github.com/isaacs/node-glob) - Pattern matching

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the beautiful [Ayu color scheme](https://github.com/dempfi/ayu) by @dempfi
- Built with love for developers who appreciate aesthetics and functionality
- Thanks to all contributors who help improve this project

## Support

- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/WIZARD3022/Ayu-watch/issues)
- **Discussions**: Join conversations in [GitHub Discussions](https://github.com/WIZARD3022/Ayu-watch/discussions)
- **Email**: For private inquiries, contact the maintainer

## Roadmap

- [ ] GUI application with system tray integration
- [ ] Cloud sync for configuration across devices
- [ ] Integration with popular IDEs (VS Code, WebStorm)
- [ ] Docker container monitoring support
- [ ] Custom theme creation tool
- [ ] Performance analytics and statistics
- [ ] Remote file watching over SSH

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

---

**Made with ❤️ by WIZARD3022**

If you find this project helpful, please consider giving it a ⭐️ on GitHub!
