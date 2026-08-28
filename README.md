# 📋 Instant Meeting Action Taker

A Generative AI-powered web application that converts meeting notes or transcripts into clear and actionable tasks.

The application analyzes meeting discussions, identifies action items, and extracts details such as task owners, deadlines, priorities, and follow-up activities. Users can review and edit the extracted tasks, save them to Google Sheets, or download them as a CSV file.

---

## ✨ Features

* 🤖 Extract action items from meeting notes using Generative AI
* 👤 Identify task owners
* 📅 Extract deadlines
* 🚨 Detect task priorities
* 🔄 Identify follow-up activities
* ✏️ Edit extracted action items before saving
* 📊 Track task status
* ☁️ Save action items directly to Google Sheets
* 📥 Download action items as a CSV file
* 🔗 Open the generated Google Sheet directly after saving

---

## 🛠️ Technologies Used

* **Python**
* **Streamlit** – Web application framework
* **Google Gemini API** – Generative AI for extracting meeting action items
* **Pydantic** – Structured data validation
* **Pandas** – Data handling and CSV generation
* **gspread** – Google Sheets integration
* **Google Drive API** – Sharing generated spreadsheets
* **Google OAuth 2.0** – Authentication for Google services

---

## 📁 Project Structure

```text
instant-meeting-action-taker/
│
├── app.py
├── ai_service.py
├── config.py
├── google_sheets.py
├── models.py
├── styles.py
├── requirements.txt
├── .gitignore
├── .env
├── credentials.json
└── token.json
```

> **Note:** `.env`, `credentials.json`, and `token.json` contain sensitive information and should not be uploaded to GitHub.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Alanj7788/Instant-Meeting-Action-Taker.git
```

### 2. Navigate to the project folder

```bash
cd Instant-Meeting-Action-Taker
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

#### Windows

```bash
.venv\Scripts\activate
```

#### macOS/Linux

```bash
source .venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Configuration

Create a `.env` file in the project root and add your Google Gemini API key.

```env
GEMINI_API_KEY=your_api_key_here
```

You also need to create Google OAuth credentials and save the downloaded file as:

```text
credentials.json
```

When the application connects to Google Sheets for the first time, Google authentication will be required. After successful authentication, a `token.json` file will be created automatically.

---

## 🚀 Running the Application

Run the following command:

```bash
streamlit run app.py
```

Then open the local URL displayed in the terminal.

---

## 📖 How It Works

1. Enter a meeting title.
2. Paste the meeting notes or transcript.
3. Click **Extract Action Items**.
4. The Generative AI analyzes the meeting content.
5. Action items are extracted with:

   * Task
   * Owner
   * Deadline
   * Priority
   * Follow-up
   * Status
6. Review and edit the generated action items.
7. Save the results to Google Sheets or download them as a CSV file.

---

## 🔒 Security

The following files should be excluded from version control:

```text
.env
credentials.json
token.json
__pycache__/
.venv/
```

These files are included in `.gitignore` to prevent sensitive credentials and local environment files from being uploaded to GitHub.

---

## 👨‍💻 Author

**Alan Jose**

B.Tech Computer Science and Engineering

---

## 📄 License

This project was developed for educational and project submission purposes.
