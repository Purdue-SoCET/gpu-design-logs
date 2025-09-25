
# Design Log Week 5

## Status: 

I am not currently stuck or blocked.

## Useful Reading  

### [CS334](https://cs.purdue.edu/cgvlab/courses/334/Fall_2025/Lectures/)
- Basics of Graphics pipeline

### [Learning OpenGL](https://learnopengl.com/book/book_pdf.pdf)

### [Math for Graphics Textbook](https://theswissbay.ch/pdf/Gentoomen%20Library/Game%20Development/Programming/Mathematics%20for%20Computer%20Graphics.pdf)
- Determining FU
- Many Linear Transformations
- Some Cos/Sin/Tan
- Some power/sqrt

## Current Project Ideas

### Functional Units

- Needed:
  - int32 (add, mul, div)
  - fp32 (add, mul, div)
  - ld/st (int32, fp32, memory fence?)
  - trig func (sin, cos)
- Maybe:
  - int16/FP16 
  - graphics specific (shader core?, z/stencil buffers? rasterizer?)
  - T$?
  - special (sqrt, 3x3 matrix?, Control/Status Registers? hardware performance counters?)
    
### Workflow
<img width="1266" height="291" alt="image" src="https://github.com/user-attachments/assets/49070b95-3c56-4fdc-8466-64953bf78109" />
(https://docs.imgtec.com/starter-guides/powervr-architecture/html/topics/tile-based-deferred-rendering-index.html)

- Drop Alpha Steps

## Work Completed

### Presentation
- Created Presentation for Team Leads Meeting
  
### [OpenGL Tutorial](https://www.youtube.com/watch?v=greXpRqCTKs&list=PLPaoO-vpZnumdcb4tZc4x5Q-v7CkrQ6M-&index=5) 
- Completed up to Textures

**OpenGL Flow**:
- Initlize Window
- Define Vertices/Indices
```
// Vertices coordinates
GLfloat vertices[] =
{ //               COORDINATES                  /     COLORS           //
	-0.5f, -0.5f * float(sqrt(3)) * 1 / 3, 0.0f,     0.8f, 0.3f,  0.02f, // Lower left corner
	 0.5f, -0.5f * float(sqrt(3)) * 1 / 3, 0.0f,     0.8f, 0.3f,  0.02f, // Lower right corner
	 0.0f,  0.5f * float(sqrt(3)) * 2 / 3, 0.0f,     1.0f, 0.6f,  0.32f, // Upper corner
	-0.25f, 0.5f * float(sqrt(3)) * 1 / 6, 0.0f,     0.9f, 0.45f, 0.17f, // Inner left
	 0.25f, 0.5f * float(sqrt(3)) * 1 / 6, 0.0f,     0.9f, 0.45f, 0.17f, // Inner right
	 0.0f, -0.5f * float(sqrt(3)) * 1 / 3, 0.0f,     0.8f, 0.3f,  0.02f  // Inner down
};


GLuint indices[] =
{
	0, 3, 5, // lower left triangle
	3, 2, 4, // lower right triangle
	5, 4, 1  // upper triangle
};
```
- Create Window
```
	//Initilize Window
	glfwInit();

	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
	glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);


	//Create Window 
	GLFWwindow* window = glfwCreateWindow(800, 800, "opengltutorial", NULL, NULL);
	if (window == NULL)
	{
		std::cout << "Failed to create window" << std::endl;
		glfwTerminate();
		return -1;
	}

	glfwMakeContextCurrent(window);

	gladLoadGL();

	glViewport(0, 0, 800, 800);
```
- Shaders:
  - Vertex -> modify properties of the vertex such as position, color, and texture coordinates, set vertices and indices
```
    #version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;

out vec3 color;

uniform float scale;

void main()
{
   gl_Position = vec4(aPos.x + aPos.x * scale, aPos.y + aPos.y * scale, aPos.z + aPos.z * scale, 1.0);
   color = aColor;
}
```
  - Fragment -> calculating individual fragment colors, set RGBA
```
#version 330 core
out vec4 FragColor;

in vec3 color;

void main()
{
   FragColor = vec4(color, 1.0f);
}
```
  - Shader to GPU
```
Shader::Shader(const char* vertexFile, const char* fragmentFile)
{
    std::string vertexCode = get_file_contents(vertexFile);
    std::string fragmentCode = get_file_contents(fragmentFile);

    const char* vertexSource = vertexCode.c_str();
    const char* fragmentSource = fragmentCode.c_str();

    GLuint vertexShader = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertexShader, 1, &vertexSource, NULL);
    glCompileShader(vertexShader);

    compileErrors(vertexShader, "VERTEX");

    GLuint fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragmentShader, 1, &fragmentSource, NULL);
    glCompileShader(fragmentShader);

    compileErrors(fragmentShader, "FRAGMENT");

    ID = glCreateProgram();

    glAttachShader(ID, vertexShader);
    glAttachShader(ID, fragmentShader);
    glLinkProgram(ID);
    compileErrors(ID, "PROGRAM");

    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);
}
```
 
- uniform -> like global variable in openGL to adjust shaders
  
<img width="685" height="313" alt="image" src="https://github.com/user-attachments/assets/bba3b1bc-864b-4b86-94bd-b82e142a31fe" />

- Buffers:
  - need to generate, bind, and add data
  - VAO -> stores state required to supply vertex data
```
  void VAO::LinkAttrib(VBO& VBO, GLuint layout, GLuint numComponents, GLenum type, GLsizeiptr stride, void* offset)
{
	VBO.Bind();
	glVertexAttribPointer(layout, numComponents, type, GL_FALSE, stride, offset);
	glEnableVertexAttribArray(layout);
	VBO.Unbind();
}
```
  - VBO -> stores vertex data in GPU memory
```
VBO::VBO(GLfloat* vertices, GLsizeiptr size)
{
	glGenBuffers(1, &ID);
	glBindBuffer(GL_ARRAY_BUFFER, ID);
	glBufferData(GL_ARRAY_BUFFER, size, vertices, GL_STATIC_DRAW);
}

void VBO::Bind()
{
	glBindBuffer(GL_ARRAY_BUFFER, ID);
}

void VBO::Unbind()
{
	glBindBuffer(GL_ARRAY_BUFFER, 0);
}
```
  - EBO -> stores indicies data
```
EBO::EBO(GLuint* indices, GLsizeiptr size)
{
	glGenBuffers(1, &ID);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ID);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, size, indices, GL_STATIC_DRAW);
}

void EBO::Bind()
{
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ID);
}

void EBO::Unbind()
{
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);
}
```
- in main:
```
  	VAO VAO1;
	VAO1.Bind();

	VBO VBO1(vertices, sizeof(vertices));
	EBO EBO1(indices, sizeof(indices));

	VAO1.LinkAttrib(VBO1, 0, 3, GL_FLOAT, 6 * sizeof(GL_FLOAT), (void*)0);
	VAO1.LinkAttrib(VBO1, 1, 3, GL_FLOAT, 6 * sizeof(GL_FLOAT), (void*)(3 * sizeof(float)));

	VAO1.Unbind();

	VBO1.Unbind();
	EBO1.Unbind();
  ```

- Render Image using shader program and draw element
```
	while (!glfwWindowShouldClose(window)) {
		glClearColor(0.07f, 0.13f, 0.17f, 1.0f);
		glClear(GL_COLOR_BUFFER_BIT);
		shaderProgram.Activate();
		glUniform1f(uniID, 0.5f);
		VAO1.Bind();
		glDrawElements(GL_TRIANGLES, 9, GL_UNSIGNED_INT, 0);
		glfwSwapBuffers(window);

		glfwPollEvents();
	}
```
- Clean up
```
	VAO1.Delete();
	VBO1.Delete();
	EBO1.Delete();
	shaderProgram.Delete();

	glfwDestroyWindow(window);
	glfwTerminate();
```

