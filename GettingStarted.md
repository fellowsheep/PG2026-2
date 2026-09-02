
## 📌 Próximos Passos

✅ Adicionar os exercícios dentro da pasta `src/`
```
📁 src/
│── Hello3D.cpp
│── Transformacoes.cpp
│── Iluminacao.cpp
```

✅ Para cada exercício novo, atualizar o arquivo `CMakeLists.txt`
```cmake
set(EXERCISES 
    Hello3D
    Transformacoes
    Iluminacao
)
```
✅ Atualmente, o `CMakelists.txt` já está configurado para compilar e gerar o excutável de cada código acrescentado no set EXERCISES. Se necessário, adicionar novas dependências
```cmake
foreach(EXERCISE ${EXERCISES})
    add_executable(${EXERCISE} src/${EXERCISE}.cpp Common/glad.c)
    target_link_libraries(${EXERCISE} glfw opengl32)
endforeach()
```
✅ Isso faz com que cada exercício gere seu próprio executável dentro da pasta build/.

✅ Portanto, se adicionar mais arquivos .cpp, basta incluir o nome na lista EXERCISES e rodar o CMake novamente.
