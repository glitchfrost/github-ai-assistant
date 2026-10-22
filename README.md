# GitHub AI Assistant

GitHub AI Assistant is a project I built to make understanding and exploring code repositories easier. It combines a Spring Boot backend, a React frontend, and a Python-based AI service to help developers interact with repository code using natural language.

The idea is to retrieve relevant code from a repository and use that context to generate more useful answers instead of relying only on a general-purpose language model.

## What it does

- Allows users to interact with repository code through an AI-powered chat interface.
- Indexes source code so relevant files and code snippets can be retrieved.
- Uses vector embeddings and ChromaDB for semantic search.
- Connects the backend with an AI service for repository-related queries.
- Provides a dashboard for code analysis and repository interaction.

## Tech Stack

- **Frontend:** React, JavaScript, Vite
- **Backend:** Java 21, Spring Boot, REST APIs
- **AI Service:** Python, FastAPI
- **Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)
- **Vector Database:** ChromaDB
- **Language Model:** Ollama with Llama 3
- **Database:** MySQL

## How it works

1. The user interacts with the application through the React frontend.
2. The Spring Boot backend handles API requests and repository operations.
3. The AI service processes code and generates embeddings for semantic retrieval.
4. ChromaDB stores the embeddings and helps retrieve relevant code context.
5. The retrieved context is used by the language model to generate a response.

## Project Structure

```text
github-ai-assistant/
├── ai-service/    # Python AI service and vector search
├── backend/       # Spring Boot application
├── frontend/      # React user interface
└── README.md
```

## Running Locally

### Prerequisites

- Java 21
- Node.js and npm
- Python 3
- MySQL
- Ollama with the required model

### 1. Clone the repository

```bash
git clone https://github.com/glitchfrost/github-ai-assistant.git
cd github-ai-assistant
```

### 2. Set up MySQL

Create the database:

```sql
CREATE DATABASE github_assistant;
```

Configure the database connection using environment variables:

```powershell
$env:DB_URL="jdbc:mysql://localhost:3306/github_assistant"
$env:DB_USERNAME="root"
$env:DB_PASSWORD="your_mysql_password"
```

### 3. Start the backend

```powershell
cd backend/backend
.\mvnw.cmd spring-boot:run
```

The backend uses port `8080` by default.

### 4. Start the frontend

Open another terminal from the project root:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL shown in the terminal, usually `http://localhost:5173`.

The Python AI service, MySQL, and Ollama must also be configured and running for the complete application to work.

## What I learned

Building this project gave me practical experience with Spring Boot REST APIs, React integration, database connectivity, Python service integration, vector embeddings, and retrieval-augmented generation.

## Author

**Himesh Kumar Kumawat**

[GitHub Profile](https://github.com/glitchfrost)
