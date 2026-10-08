
#include <iostream>

using namespace std;

// GLAD
#include <glad/glad.h>

// GLFW
#include <GLFW/glfw3.h>

// GLM 
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

using namespace glm;

class Sprite 
{
    private:
    GLuint VAO;
    GLuint texID;
    GLuint *shaderID;

    vec3 position;
    float angle;
    vec3 dimensions;
    int nAnimations, nFrames;
    float ds,dt;


    public:
    Sprite() {}
    Sprite(GLuint texID, GLuint *shaderID, vec3 pos = vec3(0.0,0.0,0.0), vec3 dimensions = vec3(1.0,1.0,1.0),int nAnimations=1,int nFrames = 1, float angle = 0.0);
    void inicializar(GLuint texID, GLuint *shaderID, vec3 pos = vec3(0.0,0.0,0.0), vec3 dimensions = vec3(1.0,1.0,1.0),int nAnimations=1,int nFrames = 1,float angle = 0.0);
    void atualizar();
    void desenhar();
    ~Sprite() {}

};