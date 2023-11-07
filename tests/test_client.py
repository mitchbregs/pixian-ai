import unittest
from unittest.mock import patch, Mock, mock_open
from pixian_ai.client import PixianAI, PixianAIException


class TestPixianAI(unittest.TestCase):
    @patch("pixian_ai.client.requests.post")
    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_remove_background_with_image_path(self, mock_file, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"some content"
        mock_post.return_value = mock_response

        pixian = PixianAI(api_id="some-api-id", api_secret="some-api-secret")
        response = pixian.remove_background(image_path="some-image-path.jpg")

        self.assertEqual(response.content, b"some content")
        mock_file.assert_called_once_with("some-image-path.jpg", "rb")
        mock_post.assert_called_once_with(
            "https://api.pixian.ai/api/v2/remove-background",
            data={
                "max_pixels": 25000000,
                "background.color": None,
                "result.crop_to_foreground": False,
                "result.margin": "0px",
                "result.target_size": None,
                "result.vertical_alignment": "middle",
                "output.format": "auto",
                "output.jpeg_quality": 75,
            },
            files={"image": mock_file()},
            auth=("some-api-id", "some-api-secret"),
        )

    @patch("pixian_ai.client.requests.post")
    def test_remove_background_with_image_base64(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"base64 image response"
        mock_post.return_value = mock_response

        pixian = PixianAI(api_id="some-api-id", api_secret="some-api-secret")

        response = pixian.remove_background(image_base64="base64-string-of-the-image")

        self.assertEqual(response.content, b"base64 image response")

        mock_post.assert_called_once_with(
            "https://api.pixian.ai/api/v2/remove-background",
            data={
                "image.base64": "base64-string-of-the-image",
                "max_pixels": 25000000,
                "background.color": None,
                "result.crop_to_foreground": False,
                "result.margin": "0px",
                "result.target_size": None,
                "result.vertical_alignment": "middle",
                "output.format": "auto",
                "output.jpeg_quality": 75,
            },
            files={},
            auth=("some-api-id", "some-api-secret"),
        )

    @patch("pixian_ai.client.requests.post")
    def test_remove_background_with_image_url(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"image with background removed"
        mock_post.return_value = mock_response

        pixian = PixianAI(api_id="dummy-api-id", api_secret="dummy-api-secret")

        image_url = "http://example.com/image.jpg"
        response = pixian.remove_background(image_url=image_url)

        self.assertEqual(response.content, b"image with background removed")

        mock_post.assert_called_once_with(
            "https://api.pixian.ai/api/v2/remove-background",
            data={
                "image.url": image_url,
                "max_pixels": 25000000,
                "background.color": None,
                "result.crop_to_foreground": False,
                "result.margin": "0px",
                "result.target_size": None,
                "result.vertical_alignment": "middle",
                "output.format": "auto",
                "output.jpeg_quality": 75,
            },
            files={},
            auth=("dummy-api-id", "dummy-api-secret"),
        )

    def test_remove_background_with_invalid_background_color(self):
        pixian = PixianAI(api_id="dummy-api-id", api_secret="dummy-api-secret")
        with self.assertRaises(ValueError):
            pixian.remove_background(
                image_path="dummy-path.jpg", background_color="ZZZ"
            )

    def test_remove_background_with_invalid_result_margin(self):
        pixian = PixianAI(api_id="dummy-api-id", api_secret="dummy-api-secret")
        with self.assertRaises(ValueError):
            pixian.remove_background(
                image_path="dummy-path.jpg", result_margin="invalid-margin"
            )

    def test_remove_background_with_invalid_result_target_size(self):
        pixian = PixianAI(api_id="dummy-api-id", api_secret="dummy-api-secret")
        with self.assertRaises(ValueError):
            pixian.remove_background(
                image_path="dummy-path.jpg", result_target_size="invalid-size"
            )

    def test_remove_background_with_invalid_result_vertical_alignment(self):
        pixian = PixianAI(api_id="dummy-api-id", api_secret="dummy-api-secret")
        with self.assertRaises(ValueError):
            pixian.remove_background(
                image_path="dummy-path.jpg",
                result_vertical_alignment="invalid-alignment",
            )

    def test_remove_background_with_invalid_output_format(self):
        pixian = PixianAI(api_id="dummy-api-id", api_secret="dummy-api-secret")
        with self.assertRaises(ValueError):
            pixian.remove_background(
                image_path="dummy-path.jpg", output_format="invalid-format"
            )

    def test_remove_background_with_invalid_output_jpeg_quality(self):
        pixian = PixianAI(api_id="dummy-api-id", api_secret="dummy-api-secret")
        with self.assertRaises(ValueError):
            pixian.remove_background(
                image_path="dummy-path.jpg", output_jpeg_quality=101
            )
