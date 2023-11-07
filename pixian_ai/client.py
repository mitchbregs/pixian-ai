from typing import Union

import requests

from pixian_ai.utils import (
    enforce_types,
    param_exists,
    validate_css,
    validate_hex,
    validate_param,
    validate_wh,
)


class PixianAIException(Exception):
    """
    A class to represent an exception from the Pixian.ai API.

    Attributes:
        message (str): The message of the exception.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class PixianAIResponse(bytes):
    """
    A class to represent a response from the Pixian.ai API.

    Attributes:
        content (bytes): The content of the response.
    """

    def __init__(self, content):
        """
        Initializes a new instance of the PixianAIResponse class.

        Args:
            content (bytes): The content of the response.
        """
        super().__init__()
        self.content = content

    def __repr__(self):
        """
        String representation of the response.

        Returns:
            A string representation of the response.
        """
        return f"bytes:`PixianAIResponse`"

    def __str__(self):
        """
        String representation of the response.

        Returns:
            A string representation of the response.
        """
        return self.content.decode("utf-8")

    def save(self, fp: str):
        """
        Save the response to a file.

        Args:
            fp (str): The file path to save the response to.
        """
        with open(fp, "wb") as file:
            file.write(self.content)


class PixianAI:
    """
    A class to interact with the Pixian.ai API for vectorizing images.

    Attributes:
        api_id (str):
            The API ID to authenticate with the Pixian.ai API.
        api_secret (str):
            The API secret to authenticate with the Pixian.ai API.

    Methods:
        remove_background:
            Remove background of the given image with specified parameters.
    """

    def __init__(self, api_id: str, api_secret: str):
        """
        Initializes a new instance of the PixianAI class.

        Args:
            api_id (str):
                The API ID to authenticate with the Pixian.ai API.
            api_secret (str):
                The API secret to authenticate with the Pixian.ai API.
        """
        self.api_id = api_id
        self.api_secret = api_secret

    @enforce_types
    def remove_background(
        self,
        image_path: str = "",
        image_base64: str = "",
        image_url: str = "",
        max_pixels: int = 25000000,
        background_color: Union[str, None] = None,
        result_crop_to_foreground: bool = False,
        result_margin: str = "0px",
        result_target_size: Union[str, None] = None,
        result_vertical_alignment: str = "middle",
        output_format: str = "auto",
        output_jpeg_quality: int = 75,
    ):
        """
        Remove the background of an image with the specified parameters.

        Args:
            image_path (str, optional):
                The path to the image file to be vectorized.
                Defaults to an empty string.
            image_base64 (str, optional):
                The base64 encoded string of the image to be vectorized.
                Defaults to an empty string.
            image_url (str, optional): The URL of the image to be vectorized.
                Defaults to an empty string.
            max_pixels (int, optional):
                The maximum number of pixels in the input image.
                Defaults to 2097252.
            background_color (str, optional):
                The background color of the output image in hexadecimal format.
                Be sure to include the "#" symbol.
                Defaults to None.
            result_crop_to_foreground (bool, optional):
                Whether to crop the output image to the foreground.
                Defaults to False.
            result_margin (str, optional):
                The margin of the output image.
                Defaults to "0px".
            result_target_size (str, optional):
                The target size of the output image.
                Defaults to None.
            result_vertical_alignment (str, optional):
                The vertical alignment of the output image.
                Defaults to "middle".
            output_format (str, optional):
                The format of the output image.
                Defaults to "auto".
            output_jpeg_quality (int, optional):
                The quality to use when encoding JPEG results.
                Defaults to 75.

        Raises:
            TypeError: If the type of any of the parameters is invalid.
            ValueError: If any of the parameters are invalid.
            PixianAIException: If the request to the Pixian.ai API fails.

        Returns:
            PixianAIResponse: An object containing the background removed result.
        """
        param_exists(
            ["image_path", "image_base64", "image_url"],
            [image_path, image_base64, image_url],
        )

        validate_param("max_pixels", max_pixels, (100, 25000000))
        if background_color:
            validate_hex("background_color", background_color)
        validate_param(
            "result_crop_to_foreground", result_crop_to_foreground, [True, False]
        )
        validate_css("result_margin", result_margin)
        if result_target_size:
            validate_wh("result_target_size", result_target_size)
        validate_param(
            "result_vertical_alignment",
            result_vertical_alignment,
            ["top", "middle", "bottom"],
        )
        validate_param(
            "output_format", output_format, ["auto", "png", "jpeg", "delta_png"]
        )
        validate_param("output_jpeg_quality", output_jpeg_quality, (1, 100))

        url = "https://api.pixian.ai/api/v2/remove-background"
        files = {}
        data = {
            "max_pixels": max_pixels,
            "background.color": background_color,
            "result.crop_to_foreground": result_crop_to_foreground,
            "result.margin": result_margin,
            "result.target_size": result_target_size,
            "result.vertical_alignment": result_vertical_alignment,
            "output.format": output_format,
            "output.jpeg_quality": output_jpeg_quality,
        }

        if image_path:
            files = {"image": open(image_path, "rb")}
        elif image_base64:
            data.update({"image.base64": image_base64})
        elif image_url:
            data.update({"image.url": image_url})

        response = requests.post(
            url, data=data, files=files, auth=(self.api_id, self.api_secret)
        )

        if not response.status_code == requests.codes.ok:
            raise PixianAIException(message=response.text)

        return PixianAIResponse(response.content)
