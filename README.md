# pixian-ai

Python SDK for [pixian.ai](https://pixian.ai/).

## What is it?

Remove image backgrounds.

## Install

```bash
$ pip install pixian-ai
```

## Usage

### Basic

```python
from pixian_ai import PixianAI

client = PixianAI(
    api_id="PIXIAN-AI-API-ID",
    api_secret="PIXIAN-AI-API-SECRET",
)
img = client.remove_background("/path/to/input.jpeg")

img.save("/path/to/output.jpeg")
```

You can also use:

```python
client.remove_background(image_base64="base64encodedimage==")

# or

client.remove_background(image_url="https://imageurl.com/test.jpeg")
```

### Advanced

```python
client.remove_background(
    image_path="/path/to/image.jpeg",
    max_pixels=100,
    background_color="#0055FF"
    ...
)
```

Reference: [https://pixian.ai/api](https://pixian.ai/api#:~:text=uploading%20binary%20files.-,Parameters,-The%20input%20image)

All parameters described in the API spec above replace period (`.`) with underscore (`_`). For example, if the parameter is `background.color`, the SDK will use `background_color`.

## Contributing

Feel free to open a PR for any changes!

## Testing

```bash
$ python -m unittest discover -s tests -p 'test_*.py'
```

Made with ❤️ by [@mitchbregs](https://twitter.com/mitchbregs)
