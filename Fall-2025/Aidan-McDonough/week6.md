# Design Log Week 6

## Status: 

I am not currently stuck or blocked.

## Work Completed

### Design Review Presentation

- Discussed structure of presentation
  - Must include hardware requirements, graphic pipeline, graphic library, benchmark program, and design tradeoffs

|Design| Purpose |Tradeoff|
| --- | --- | --- |
|C Language| Simplicity |Less Abstraction|
|Trig Functions | Faster Computation | Additional Hardware, More Area/Complexity|
|No Matrx Multiplier/Other Special Function Units| Easier Design and Less Area| Lower Throughput on MultAdd Ops|
|No Lighting/Reflections| Less Computationally Heavy, Easier Design| Less Realistic Picture|

    
- Created [slides](https://docs.google.com/presentation/d/1M33G-WqNQMKs6h0JDbxaD1RH-Oab2VH1/edit?usp=sharing&ouid=103722050532182315918&rtpof=true&sd=true)

### OpenGL [Tutorial](https://www.youtube.com/watch?v=u-00hjlfMKc&list=PLPaoO-vpZnumdcb4tZc4x5Q-v7CkrQ6M-&index=7)

- Created 2D square with custom jpg textures mapped on onto face
- OpenGL Workflow for Texture:
  1. Load image (CPU): `stbi_load(...)` to get `bytes`, `widthImg`, `heightImg`, `numColCh`.
  2. Create and bind texture (GPU): `glGenTextures`, `glActiveTexture(GL_TEXTURE0)`, `glBindTexture(GL_TEXTURE_2D, texture)`.
  3. Set sampling andwrapping: `GL_TEXTURE_MIN_FILTER/MAG_FILTER = GL_NEAREST`; `GL_TEXTURE_WRAP_S/T = GL_REPEAT`.
  4. Upload pixels and build mipmaps: `glTexImage2D(..., GL_RGB, GL_UNSIGNED_BYTE, bytes);` then `glGenerateMipmap(GL_TEXTURE_2D)`.  
     - To actually use mipmaps, choose a mipmapped min filter (e.g., `GL_LINEAR_MIPMAP_LINEAR`).
  5. Free CPU copy and unbind: `stbi_image_free(bytes);` then `glBindTexture(GL_TEXTURE_2D, 0)`.
  6. Link to shader sampler: `glGetUniformLocation(..., "tex0");` use program; set sampler to unit 0 with `glUniform1i(tex0Uni, 0);`.
  7. Render loop: clear, use program, ensure `glActiveTexture(GL_TEXTURE0); glBindTexture(GL_TEXTURE_2D, texture);` bind VAO, draw, swap, poll.
  8. Cleanup: delete VAO/VBO/EBO, textures, and program.
 

```
	int widthImg, heightImg, numColCh;
	stbi_set_flip_vertically_on_load(true);
	unsigned char* bytes = stbi_load("rex.jpg", &widthImg, &heightImg, &numColCh, 0);

	GLuint texture;
	glGenTextures(1, &texture);
	glActiveTexture(GL_TEXTURE0);
	glBindTexture(GL_TEXTURE_2D, texture);

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, widthImg, heightImg, 0, GL_RGB, GL_UNSIGNED_BYTE, bytes);
	glGenerateMipmap(GL_TEXTURE_2D);

	stbi_image_free(bytes);
	glBindTexture(GL_TEXTURE_2D, 0);

	GLuint tex0Uni = glGetUniformLocation(shaderProgram.ID, "tex0");
	shaderProgram.Activate();
	glUniform1f(tex0Uni, 0);

	while (!glfwWindowShouldClose(window)) {
		glClearColor(0.07f, 0.13f, 0.17f, 1.0f);
		glClear(GL_COLOR_BUFFER_BIT);
		shaderProgram.Activate();
		glUniform1f(uniID, 0.5f);
		glBindTexture(GL_TEXTURE_2D, texture);
		VAO1.Bind();
		glDrawElements(GL_TRIANGLES, 9, GL_UNSIGNED_INT, 0);
		glfwSwapBuffers(window);
		glfwPollEvents();
	}
```

- `stbi_set_flip_vertically_on_load(true)` – flip loaded image so UV (0,0) matches OpenGL’s lower-left.
- `stbi_load(...)` – load image bytes on the CPU and return width/height/channels.
- `glGenTextures(1, &texture)` – create a new texture object handle.
- `glActiveTexture(GL_TEXTURE0)` – select texture unit 0 for subsequent binds/uniforms.
- `glBindTexture(GL_TEXTURE_2D, texture)` – bind the texture object to the 2D target on the active unit.
- `glTexParameteri(target, pname, param)` – set sampling (min/mag) and wrapping (S/T) behavior.
- `glTexImage2D(...)` – allocate GPU storage for the texture and upload pixel data.
- `glGenerateMipmap(GL_TEXTURE_2D)` – build the full mipmap chain from level 0.
- `stbi_image_free(bytes)` – free the CPU copy of the pixel data.
- `glGetUniformLocation(program, "tex0")` – get the location/index of the `sampler2D` uniform.
- `shaderProgram.Activate()` – make this shader program current (`glUseProgram` under the hood).
- `glUniform1i(tex0Uni, 0)` – tell the sampler to read from texture unit 0.
- `glClearColor(r,g,b,a)` – set the color used when clearing the framebuffer.
- `glClear(GL_COLOR_BUFFER_BIT)` – clear the color buffer to the set clear color.
- `VAO1.Bind()` – bind vertex array state (attributes, element buffer).
- `glDrawElements(GL_TRIANGLES, 9, GL_UNSIGNED_INT, 0)` – draw indexed triangles using the bound VAO.
- `glfwSwapBuffers(window)` – present the rendered frame to the screen.
- `glfwPollEvents()` – process window/input events.
