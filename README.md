# YAML Deserialization Vulnerability Demo

This application demonstrates the potential security vulnerabilities in YAML deserialization using the PyYAML library. It provides both secure and insecure modes to highlight the differences and risks associated with improper YAML parsing.

## Overview

YAML (YAML Ain't Markup Language) is a human-readable data serialization format. However, when improperly used, it can lead to serious security vulnerabilities, including remote code execution.

This demo application allows users to upload YAML files and see how they are parsed in both secure and insecure modes.

## The Vulnerability

The vulnerability lies in the `yaml.load()` function when used with untrusted input. This function can construct arbitrary Python objects, which may allow an attacker to execute malicious code.

For example, consider this YAML content:

```yaml
!!python/object/apply:os.system
- 'echo Hello, vulnerability!'
```

When parsed insecurely, this YAML could execute the `echo` command on the system.

## Secure vs. Insecure Modes

1. **Secure Mode**: Uses `yaml.safe_load()`, which only parses basic YAML tags and does not construct arbitrary Python objects.

2. **Insecure Mode**: Uses `yaml.load()` with `yaml.Loader`, which can construct arbitrary Python objects and is vulnerable to attacks.

## Setup and Running

1. Clone this repository:
   ```
   git clone <repository-url>
   cd yaml-deserialization-python
   ```

2. Build the Docker image:
   ```
   docker build -t yaml-deserialization-demo .
   ```

3. Run the container:

   - In secure mode:
     ```
     docker run -p 8880:8880 -e SECURE_MODE=true yaml-deserialization-demo
     ```

   - In insecure mode:
     ```
     docker run -p 8880:8880 -e SECURE_MODE=false yaml-deserialization-demo
     ```

4. Access the application at `http://localhost:8880`

## Usage

1. Open your web browser and go to `http://localhost:8880`.
2. You'll see whether the application is running in secure or insecure mode.
3. Upload a YAML file using the provided form.
4. The application will attempt to parse the YAML and display the result or any errors.

## Testing the Vulnerability

To safely demonstrate the YAML deserialization vulnerability:

1. Locate the `test_payload.yml` file in the project directory. It contains:
   ```yaml
   !!python/object/apply:platform.platform
   []
   ```

2. Run the application in secure mode:
   ```
   docker run -p 8880:8880 -e SECURE_MODE=true yaml-deserialization-demo
   ```

3. Upload the `test_payload.yml` file through the web interface.
   - Expected result: The application should reject the payload and display an error message.

4. Now, run the application in insecure mode:
   ```
   docker run -p 8880:8880 -e SECURE_MODE=false yaml-deserialization-demo
   ```

5. Upload the `test_payload.yml` file again.
   - Expected result: The application will process the payload and display information about the server's operating system.

This demonstration shows how the insecure YAML parsing can lead to unauthorized code execution. In a real-world scenario, an attacker could potentially run arbitrary code on the server.

**Note**: This payload safely demonstrates the vulnerability by retrieving system information without modifying any files or executing harmful commands. Always use `yaml.safe_load()` when working with untrusted YAML input in production environments.

## Security Best Practices

1. Always use `yaml.safe_load()` instead of `yaml.load()` when parsing untrusted YAML input.
2. Keep your PyYAML library updated to the latest version.
3. Implement proper input validation and sanitization.
4. Run applications with the least privileges necessary.

## Dependencies

- Flask 2.0.1
- PyYAML 5.4.1

## Disclaimer

This application is for demonstration and educational purposes only. It should not be used in a production environment or to process untrusted input.

## License

[MIT License](https://opensource.org/licenses/MIT)

## Contributing

Contributions to improve the demo or documentation are welcome. Please submit a pull request or open an issue to discuss proposed changes.