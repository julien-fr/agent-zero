### imagen_generate:
Generate images using Google's Imagen models via the Google GenAI SDK.
Supports configuring aspect ratio, number of images, and model selection.
Generated images are saved to the specified output directory and can be displayed directly in the UI.

#### Arguments
* `prompt` (string, required) - The text description of the image to generate.
* `number_of_images` (int, optional) - Number of images to generate (1-4). Default: 1.
* `aspect_ratio` (string, optional) - Aspect ratio of the generated image. Options: "1:1", "3:4", "4:3", "16:9", "9:16". Default: "1:1".
* `model` (string, optional) - The model version to use. Default: "imagen-4.0-fast-generate-001".
* `output_dir` (string, optional) - Directory to save generated images. Default: "/a0/tmp/generated_images".
* `display_image` (boolean, optional) - Whether to display the generated images in the UI notification. Default: true.

#### Usage
##### 1. Generate a single square image
~~~json
{
    "thoughts": [
        "I need a picture of a futuristic city."
    ],
    "headline": "Generating futuristic city image",
    "tool_name": "imagen_generate",
    "tool_args": {
        "prompt": "A futuristic city with flying cars and neon lights, cyberpunk style"
    }
}
~~~

##### 2. Generate multiple landscape images without display
~~~json
{
    "thoughts": [
        "Generating landscape wallpapers for background use."
    ],
    "headline": "Generating landscape nature scenes",
    "tool_name": "imagen_generate",
    "tool_args": {
        "prompt": "Peaceful mountain lake at sunset, photorealistic",
        "number_of_images": 4,
        "aspect_ratio": "16:9",
        "display_image": false
    }
}
~~~
