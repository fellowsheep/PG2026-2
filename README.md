# Processamento Gráfico 2026/2

Este repositório contém exemplos e códigos utilizados na disciplina de **Processamento Gráfico: Fundamentos** do curso Ciência da Computação da Unisinos. Ele é estruturado para facilitar a organização dos arquivos e a compilação dos projetos utilizando CMake.

## 📂 Estrutura do Repositório

```plaintext
📂 PG2026-2/
├── 📂 include/                # Cabeçalhos e bibliotecas de terceiros
│   ├── 📂 glad/               # Cabeçalhos da GLAD (OpenGL Loader)
│   │   ├── glad.h
│   │   ├── 📂 KHR/            # Diretório com cabeçalhos da Khronos (GLAD)
│   │       ├── khrplatform.h
├── 📂 common/                 # Código reutilizável entre os projetos
│   ├── glad.c                 # Implementação da GLAD
├── 📂 src/                    # Código-fonte dos exemplos e exercícios
|   ├── 📁 Exemplos/           # Exemplos dados em aula
│   │   └── 📂 HelloTriangle/ # O "Olá mundo!" do OpenGL
|   |       └── main.cpp
│   ├── 📂 Exercicios/        # Correções e/ou base para alguns exercicios
│   │   └── ...                # Exercícios futuros
├── 📂 build/                 # Diretório gerado pelo CMake (não incluído no repositório)
├── 📄 CMakeLists.txt         # Configuração do CMake para compilar os projetos
├── 📄 README.md              # Este arquivo, com a documentação do repositório
├── 📄 GettingStarted.md      # Tutorial detalhado sobre como compilar usando o CMake
├── 📄 ...
```

### ⚙️ **Configuração necessária:**
- **API:** OpenGL  
- **Version:** 4.6
- **Profile:** Compatibility  
- **Language:** C/C++  

---

## 📚 Sugestão de Estrutura para seu próprio repositório

Recomendamos que você crie um repositório próprio, estruturado com subdiretórios dentro de `src`, para organizar suas atividades da disciplina:

```
📁 PG2026-2/
├── 📁 src/
│   ├── 📁 Exemplos/
│   │   └── ...
│   └── 📁 Exercicios/
│       ├── 📁 Lista1/
│       │   ├── 📁 Ex1/
│       │   │   └── main.cpp
│       │   ├── 📁 Ex2/
│       │   │   └── main.cpp
│       │   ├── 📁 Ex3/
│       │   │   └── main.cpp
│       │   └── README.md
│       ├── 📁 Lista2/
│       │   ├── 📁 Ex1/
│       │   │   └── main.cpp
│       │   ├── 📁 Ex2/
│       │   │   └── main.cpp
│       │   ├── 📁 Ex3/
│       │   │   └── main.cpp
│       │   └── README.md
│       ├── 📁 TrabalhoGrauA/
│       │   ├── main.cpp
│       │   ├── Object.cpp
│       │   ├── Object.h
│       │   ├── Shader.cpp
│       │   ├── Shader.h
│       │   └── README.md
│       └── ...
├── 📁 include/ # Cabeçalhos comuns (se necessário)
├── 📁 common/  # Arquivos comuns (como glad.c)
├── 📄 CMakeLists.txt
└── 📄 README.md
```
