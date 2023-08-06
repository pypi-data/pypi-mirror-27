# lambda-local-python
Run/debug AWS python lambda locally

## Installation

```bash
pip install lambda-local-python
```

## Usage

### Locally execute lambda function

```bash
ENV=my_env lambda-local-python -f path.to.module.function_name
```

### Debug in vscode

Refer to [examples/vscode-lambda-debug](examples/vscode-lambda-debug).

## Examples

Refer to examples.

- [simple-lambda](examples/simple-lambda)
- [vscode-lambda-debug](examples/vscode-lambda-debug)
