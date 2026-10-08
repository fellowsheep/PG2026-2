#include "Sprite.h"

Sprite::Sprite(GLuint texID, GLuint *shaderID, vec3 pos, vec3 dimensions, int nAnimations, int nFrames,float angle)
{
    inicializar(texID,shaderID,pos,dimensions,nAnimations,nFrames,angle);
}

void Sprite::inicializar(GLuint texID, GLuint *shaderID, vec3 pos, vec3 dimensions, int nAnimations, int nFrames, float angle)
{

    this->nAnimations = nAnimations;
    this->nFrames = nFrames;
    ds = 1.0/(float) nFrames;
    dt = 1.0/(float) nAnimations;

    cout << texID << " " << this->nAnimations << " " << this->nFrames << endl;

    // Criação do VAO (buffer de Geometria) do sprite
    GLfloat vertices[] = {
		// x   y     z      s     t
		// T0
		-0.5 ,  0.5 , 0.0 , 0.0, dt,  // v0
		-0.5 , -0.5 , 0.0 ,	0.0, 0.0,  // v1
		 0.5 ,  0.5 , 0.0,  ds, dt,  // v2
		 0.5 , -0.5 , 0.0,  ds, 0.0  //  v3
		// T1

	};

	GLuint VBO;
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

    // Setando os outros atributos com os valores passados por parâmetro
    this->texID = texID;
    this->position = pos;
    this->dimensions = dimensions;
    this->angle = angle;
    this->shaderID = shaderID;
    
}

void Sprite::atualizar()
{
}

void Sprite::desenhar()
{
    glBindTexture(GL_TEXTURE_2D, texID);
    glBindVertexArray(VAO); // Conectando ao buffer de geometria
    //Matriz de transformações do objeto (triângulo) - model matrix
	mat4 model = mat4(1); // matriz identidade
	model = translate(model, position);
	model = rotate(model, angle,vec3(0.0,0.0,1.0));
	model = scale(model,dimensions);
	GLint modelLoc = glGetUniformLocation(*shaderID,"model");
	glUniformMatrix4fv(modelLoc,1,GL_FALSE,value_ptr(model));

	// Chamada de desenho - drawcall
	// GL_TRIANGLE_STRIP
	glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);

    glBindVertexArray(0);
}
