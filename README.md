## **Gemini Chat Assistant**

**Gemini Chat Assistant** is an AI-powered chatbot application developed using Streamlit. It allows users to interact conversationally with an AI model, offering a dynamic and highly customizable chat experience. Whether you're gathering information, seeking expert advice, or engaging in creative discussions, this tool adapts to your needs.

---

### **Key Features**

#### 🔹 Model and Persona Customization

* Select from multiple AI models to optimize performance according to your preferences.
* Choose a communication style (persona) for tailored responses:

  * **Default:** Friendly and supportive assistant.
  * **Expert:** Provides technical, detailed insights.
  * **Creative:** Delivers imaginative, analogy-rich responses.

#### 🔹 Contextual Awareness

* The assistant remembers recent messages to deliver context-sensitive replies.
* You can configure how many past interactions the AI retains for improved continuity.

#### 🔹 Clean & Interactive Interface

* Displays chat messages in a user-friendly format.
* Includes controls to clear chat history or start fresh conversations.

#### 🔹 Real-Time Metrics

* Monitor key session statistics like message count and chat duration.

#### 🔹 Robust Error Handling & Data Security

* Smoothly manages runtime errors with informative user messages.
* Protects sensitive information by sourcing API keys from environment variables.

---

### **Project Setup Guide**

#### 1️⃣ Clone the Repository

```bash
git clone <repository-url>
cd <project-folder>
```

#### 2️⃣ Create a Virtual Environment

```bash
conda create -p env python=3.10 -y
```

#### 3️⃣ Activate the Environment

```bash
conda activate env/
```

#### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

#### 5️⃣ Set Environment Variables

Create a `.env` file in the root directory with the following:

```
GROQ_API_KEY=your_api_key
```

#### 6️⃣ Launch the Application

```bash
streamlit run app.py
```

---

### **How to Use**

* **Model & Persona:** Pick your preferred AI model and conversation persona from the sidebar.
* **Memory Settings:** Define how many past messages the assistant should remember.
* **Start Chatting:** Type messages and interact with the assistant in real-time.
* **Manage Conversations:** Use options to reset the chat or begin a new discussion.
* **View Statistics:** Keep track of your session’s stats from the sidebar.
