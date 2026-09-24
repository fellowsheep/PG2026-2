/*
 * Hello Triangle - Código adaptado de:
 *   - https://learnopengl.com/#!Getting-started/Hello-Triangle
 *   - https://antongerdelan.net/opengl/glcontext2.html
 *
 * Adaptado por: Rossana Baptista Queiroz
 *
 * Disciplinas:
 *   - Processamento Gráfico (Ciência da Computação - Híbrido)
 *   - Processamento Gráfico: Fundamentos (Ciência da Computação - Presencial)
 *   - Fundamentos de Computação Gráfica (Jogos Digitais)
 *
 * Descrição:
 *   Este código é o "Olá Mundo" da Computação Gráfica, utilizando OpenGL Moderna.
 *   No pipeline programável, o desenvolvedor pode implementar as etapas de
 *   Processamento de Geometria e Processamento de Pixel utilizando shaders.
 *   Um programa de shader precisa ter, obrigatoriamente, um Vertex Shader e um Fragment Shader,
 *   enquanto outros shaders, como o de geometria, são opcionais.
 *
 * Histórico:
 *   - Versão inicial: 07/04/2017
 *   - Última atualização: 05/08/2025
 *
 */

#include <iostream>
#include <string>
#include <assert.h>

using namespace std;

// GLAD
#include <glad/glad.h>

// GLFW
#include <GLFW/glfw3.h>

// GLM 
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

// STB image
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

using namespace glm;

// Protótipo da função de callback de teclado
void key_callback(GLFWwindow *window, int key, int scancode, int action, int mode);

// Protótipos das funções
int setupShader();
int setupGeometry();
int loadTexture(string filePath);

// Dimensões da janela (pode ser alterado em tempo de execução)
const GLuint WIDTH = 800, HEIGHT = 600;

// Código fonte do Vertex Shader (em GLSL): ainda hardcoded
const GLchar *vertexShaderSource = R"glsl(
 #version 400
 layout (location = 0) in vec3 position;
 layout (location = 1) in vec2 texc;
 uniform mat4 projection;
 uniform mat4 model;
 out vec2 texCoord;
 void main()
 {
	 gl_Position = projection * model * vec4(position.x, position.y, position.z, 1.0);
	 texCoord = vec2(texc.s, 1.0 - texc.t);
 }
 )glsl";

// Código fonte do Fragment Shader (em GLSL): ainda hardcoded
const GLchar *fragmentShaderSource = R"glsl(
 #version 400
 uniform vec4 inputColor;
 uniform sampler2D texBuffer; 
 out vec4 color;
 in vec2 texCoord;

 void main()
 {
	color = texture(texBuffer,texCoord);
 }
 )glsl";

// Função MAIN
int main()
{
	// Inicialização da GLFW
	glfwInit();

	// Muita atenção aqui: alguns ambientes não aceitam essas configurações
	// Você deve adaptar para a versão do OpenGL suportada por sua placa
	// Sugestão: comente essas linhas de código para desobrir a versão e
	// depois atualize (por exemplo: 4.5 com 4 e 5)
	// glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4);
	// glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 0);
	// glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
	// glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

	// Ativa a suavização de serrilhado (MSAA) com 8 amostras por pixel
	// glfwWindowHint(GLFW_SAMPLES, 8);

	// Essencial para computadores da Apple
	// #ifdef __APPLE__
	//	glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
	// #endif

	// Criação da janela GLFW
	GLFWwindow *window = glfwCreateWindow(WIDTH, HEIGHT, "Ola Triangulo! -- Rossana", nullptr, nullptr);
	if (!window)
	{
		std::cerr << "Falha ao criar a janela GLFW" << std::endl;
		glfwTerminate();
		return -1;
	}
	glfwMakeContextCurrent(window);

	// Fazendo o registro da função de callback para a janela GLFW
	glfwSetKeyCallback(window, key_callback);

	// GLAD: carrega todos os ponteiros d funções da OpenGL
	if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
	{
		std::cerr << "Falha ao inicializar GLAD" << std::endl;
		return -1;
	}

	// Obtendo as informações de versão
	const GLubyte *renderer = glGetString(GL_RENDERER); /* get renderer string */
	const GLubyte *version = glGetString(GL_VERSION);	/* version as a string */
	cout << "Renderer: " << renderer << endl;
	cout << "OpenGL version supported " << version << endl;

	
	//Exercicio 3 da Lista 2
	//glViewport(400, 100, 400, 300);

	
	// Compilando e buildando o programa de shader
	GLuint shaderID = setupShader();

	// Gerando um buffer simples, com a geometria de um triângulo
	GLuint VAO = setupGeometry();

	// Enviando a cor desejada (vec4) para o fragment shader
	// Utilizamos a variáveis do tipo uniform em GLSL para armazenar esse tipo de info
	// que não está nos buffers
	GLint colorLoc = glGetUniformLocation(shaderID, "inputColor");

	glUseProgram(shaderID); // Reseta o estado do shader para evitar problemas futuros

	double prev_s = glfwGetTime();	// Define o "tempo anterior" inicial.
	double title_countdown_s = 0.1; // Intervalo para atualizar o título da janela com o FPS.

	// Criação da matriz de projeção - projection matrix

	// Ex 1 Lista 2
	//mat4 projection = ortho(-10.0,10.0,-10.0,10.0,-1.0,1.0);
	// Ex 2 Lista 2
	mat4 projection = ortho(0.0,800.0,0.0,600.0,-1.0,1.0);
	// Para mandar pro shader
	GLint projLoc = glGetUniformLocation(shaderID,"projection");
	glUniformMatrix4fv(projLoc,1,GL_FALSE,value_ptr(projection));

	// Fazer o carregamento de uma img de textura
	//GLint texID = loadTexture("../assets/tex/Bricks_1k.png");
	GLint texID = loadTexture("../assets/sprites/pipo-nekonin022.png");

	// Enviar/Registrar no shader a variável que vai ter o buffer da tex carregada
	glUniform1i(glGetUniformLocation(shaderID,"texBuffer"),0);

	// Habilitar o primeiro buffer de textura da OpenGL
	glActiveTexture(GL_TEXTURE0);

	float angle = 0.0;
	// Loop da aplicação - "game loop"
	while (!glfwWindowShouldClose(window))
	{
		// Este trecho de código é totalmente opcional: calcula e mostra a contagem do FPS na barra de título
		{
			double curr_s = glfwGetTime();		// Obtém o tempo atual.
			double elapsed_s = curr_s - prev_s; // Calcula o tempo decorrido desde o último frame.
			prev_s = curr_s;					// Atualiza o "tempo anterior" para o próximo frame.

			// Exibe o FPS, mas não a cada frame, para evitar oscilações excessivas.
			title_countdown_s -= elapsed_s;
			if (title_countdown_s <= 0.0 && elapsed_s > 0.0)
			{
				double fps = 1.0 / elapsed_s; // Calcula o FPS com base no tempo decorrido.

				// Cria uma string e define o FPS como título da janela.
				char tmp[256];
				sprintf(tmp, "Ola Triangulo! -- Rossana\tFPS %.2lf", fps);
				glfwSetWindowTitle(window, tmp);

				title_countdown_s = 0.1; // Reinicia o temporizador para atualizar o título periodicamente.
			}
		}

		// Checa se houveram eventos de input (key pressed, mouse moved etc.) e chama as funções de callback correspondentes
		glfwPollEvents();

		// Definindo as dimensões da viewport com as mesmas dimensões da janela da aplicação
		int width, height;
		glfwGetFramebufferSize(window, &width, &height);
		glViewport(0, 0, width, height);

		// Limpa o buffer de cor
		glClearColor(0.0f, 0.0f, 0.0f, 1.0f); // cor de fundo
		glClear(GL_COLOR_BUFFER_BIT);

		glLineWidth(10);
		glPointSize(20);

		glBindVertexArray(VAO); // Conectando ao buffer de geometria
		glBindTexture(GL_TEXTURE_2D, texID);
		glUniform4f(colorLoc, 0.0f, 0.0f, 1.0f, 1.0f); // enviando cor para variável uniform inputColor

	//Matriz de transformações do objeto (triângulo) - model matrix
	mat4 model = mat4(1); // matriz identidade
	angle = glfwGetTime();
	model = translate(model, vec3(400.0, 300.0, 0.0));
	//model = rotate(model, angle,vec3(0.0,0.0,1.0));
	model = scale(model,vec3(400.0,400.0,1.0));
	GLint modelLoc = glGetUniformLocation(shaderID,"model");
	glUniformMatrix4fv(modelLoc,1,GL_FALSE,value_ptr(model));

		// Chamada de desenho - drawcall
		// GL_TRIANGLE_STRIP
		glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);

		// glBindVertexArray(0); // Desnecessário aqui, pois não há múltiplos VAOs

		// Troca os buffers da tela
		glfwSwapBuffers(window);
	}
	// Pede pra OpenGL desalocar os buffers
	glDeleteVertexArrays(1, &VAO);
	// Finaliza a execução da GLFW, limpando os recursos alocados por ela
	glfwTerminate();
	return 0;
}

// Função de callback de teclado - só pode ter uma instância (deve ser estática se
// estiver dentro de uma classe) - É chamada sempre que uma tecla for pressionada
// ou solta via GLFW
void key_callback(GLFWwindow *window, int key, int scancode, int action, int mode)
{
	if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
		glfwSetWindowShouldClose(window, GL_TRUE);
}

// Esta função está bastante hardcoded - objetivo é compilar e "buildar" um programa de
//  shader simples e único neste exemplo de código
//  O código fonte do vertex e fragment shader está nos arrays vertexShaderSource e
//  fragmentShader source no iniçio deste arquivo
//  A função retorna o identificador do programa de shader
int setupShader()
{
	// Vertex shader
	GLuint vertexShader = glCreateShader(GL_VERTEX_SHADER);
	glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
	glCompileShader(vertexShader);
	// Checando erros de compilação (exibição via log no terminal)
	GLint success;
	GLchar infoLog[512];
	glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);
	if (!success)
	{
		glGetShaderInfoLog(vertexShader, 512, NULL, infoLog);
		std::cout << "ERROR::SHADER::VERTEX::COMPILATION_FAILED\n"
				  << infoLog << std::endl;
	}
	// Fragment shader
	GLuint fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
	glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
	glCompileShader(fragmentShader);
	// Checando erros de compilação (exibição via log no terminal)
	glGetShaderiv(fragmentShader, GL_COMPILE_STATUS, &success);
	if (!success)
	{
		glGetShaderInfoLog(fragmentShader, 512, NULL, infoLog);
		std::cout << "ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n"
				  << infoLog << std::endl;
	}
	// Linkando os shaders e criando o identificador do programa de shader
	GLuint shaderProgram = glCreateProgram();
	glAttachShader(shaderProgram, vertexShader);
	glAttachShader(shaderProgram, fragmentShader);
	glLinkProgram(shaderProgram);
	// Checando por erros de linkagem
	glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);
	if (!success)
	{
		glGetProgramInfoLog(shaderProgram, 512, NULL, infoLog);
		std::cout << "ERROR::SHADER::PROGRAM::LINKING_FAILED\n"
				  << infoLog << std::endl;
	}
	glDeleteShader(vertexShader);
	glDeleteShader(fragmentShader);

	return shaderProgram;
}

// Esta função está bastante harcoded - objetivo é criar os buffers que armazenam a
// geometria de um triângulo
// Apenas atributo coordenada nos vértices
// 1 VBO com as coordenadas, VAO com apenas 1 ponteiro para atributo
// A função retorna o identificador do VAO
int setupGeometry()
{
	// Aqui setamos as coordenadas x, y e z do triângulo e as armazenamos de forma
	// sequencial, já visando mandar para o VBO (Vertex Buffer Objects)
	// Cada atributo do vértice (coordenada, cores, coordenadas de textura, normal, etc)
	// Pode ser arazenado em um VBO único ou em VBOs separados
	GLfloat vertices[] = {
		// x   y     z      s     t
		// T0
		-0.5 ,  0.5 , 0.0 , 0.0, 1.0/4.0,  // v0
		-0.5 , -0.5 , 0.0 ,	0.0, 0.0,  // v1
		 0.5 ,  0.5 , 0.0,  1.0/3.0, 1.0/4.0,  // v2
		 0.5 , -0.5 , 0.0,  1.0/3.0, 0.0  //  v3
		// T1

	};

	GLuint VBO, VAO;
	// Geração do identificador do VBO
	glGenBuffers(1, &VBO);
	// Faz a conexão (vincula) do buffer como um buffer de array
	glBindBuffer(GL_ARRAY_BUFFER, VBO);
	// Envia os dados do array de floats para o buffer da OpenGl
	glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

	// Geração do identificador do VAO (Vertex Array Object)
	glGenVertexArrays(1, &VAO);
	// Vincula (bind) o VAO primeiro, e em seguida  conecta e seta o(s) buffer(s) de vértices
	// e os ponteiros para os atributos
	glBindVertexArray(VAO);
	// Para cada atributo do vertice, criamos um "AttribPointer" (ponteiro para o atributo), indicando:
	//  Localização no shader * (a localização dos atributos devem ser correspondentes no layout especificado no vertex shader)
	//  Numero de valores que o atributo tem (por ex, 3 coordenadas xyz)
	//  Tipo do dado
	//  Se está normalizado (entre zero e um)
	//  Tamanho em bytes
	//  Deslocamento a partir do byte zero
	
	// Atributo posição - x, y, z
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), (GLvoid *)0);
	glEnableVertexAttribArray(0);

	// Coordenada de textura - s, t
	glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), (GLvoid *)(3 *sizeof(GLfloat)));
	glEnableVertexAttribArray(1);

	// Observe que isso é permitido, a chamada para glVertexAttribPointer registrou o VBO como o objeto de buffer de vértice
	// atualmente vinculado - para que depois possamos desvincular com segurança
	glBindBuffer(GL_ARRAY_BUFFER, 0);

	// Desvincula o VAO (é uma boa prática desvincular qualquer buffer ou array para evitar bugs medonhos)
	glBindVertexArray(0);

	return VAO;
}

int loadTexture(string filePath)
{
	GLuint texID;

	//Gera o id de textura na memória
	glGenTextures(1,&texID);
	glBindTexture(GL_TEXTURE_2D,texID);

	// Configura como fazer o wrapping
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT); 
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

	// Configura como fazer o filtering
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);

	int width, height, nrChannels;

	// Carregando a info (pixels) da imagem
	unsigned char *data = stbi_load(filePath.c_str(),&width, &height, &nrChannels,0);

	if (data)
	{
		if (nrChannels == 3) // imagem RGB - jpg, bmp
		{
			glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,width,height,0,GL_RGB,GL_UNSIGNED_BYTE,data);
		}
		else if (nrChannels == 4) // imagem RGBA - png
		{
			glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,width,height,0,GL_RGBA,GL_UNSIGNED_BYTE,data);
		}
		glGenerateMipmap(GL_TEXTURE_2D);
		stbi_image_free(data);
		glBindTexture(GL_TEXTURE_2D,0);

	}
	else 
	{
		cout << "Nao foi possivel carregar a textura " << filePath <<endl;
		return -1;
	}

    return texID;
}
