🧠 Spring Boot vs Python Configuration
In Spring Boot, you use:

application.properties
application.yml

👉 For Python, there is no single standard, but there are common equivalents ✅

✅ 1. .env file (MOST COMMON ✅)
👉 This is the closest equivalent to Spring Boot config files.
Example .env
DB_HOST=localhost
DB_PORT=27017
DB_NAME=mydb
DB_USER=admin
DB_PASSWORD=secret

Use in Python:
Install:
Shellpip install python-dotenvShow more lines
Code:
Pythonimport osfrom dotenv import load_dotenvload_dotenv()host = os.getenv("DB_HOST")port = os.getenv("DB_PORT")db_name = os.getenv("DB_NAME")Show more lines

✅ This is widely used in:

Flask
FastAPI
Django (optional)

✅ 2. config.py (Python-style config)
👉 Instead of external files, Python often uses a config class.
Pythonclass Config: DB_HOST = "localhost" DB_PORT = 27017 DB_NAME = "mydb"Show more lines
Use:
Pythonfrom config import Configprint(Config.DB_HOST)Show more lines

✅ 3. YAML file (like Spring Boot ✅)
👉 Yes, Python also supports YAML just like Spring Boot.
Install:
Shellpip install pyyamlShow more lines
config.yaml
YAMLdatabase: host: localhost port: 27017 name: mydbShow more lines
Load in Python:
Pythonimport yamlwith open("config.yaml") as f: config = yaml.safe_load(f)print(config["database"]["host"])Show more lines

✅ 4. JSON config
config.json
Python{ "database": { "host": "localhost", "port": 27017 }}Show more lines
Python:
Pythonimport jsonwith open("config.json") as f: config = json.load(f)Show more lines

✅ 5. Framework-specific configs
🔹 Django

Uses settings.py

🔹 Flask / FastAPI

Use .env + config.py

✅ 6. MongoDB-specific example (like Spring Boot)
.env
MONGO_URI=mongodb://localhost:27017/mydatabase

Python:
Pythonfrom pymongo import MongoClientimport osfrom dotenv import load_dotenvload_dotenv()client = MongoClient(os.getenv("MONGO_URI"))db = client.get_default_database()Show more lines

🔥 Best Practice (Industry Standard)
👉 Use combination:
✅ .env → secrets (passwords, URLs)
✅ config.py → app settings
✅ optional YAML → complex configs

🧾 Mapping (Spring Boot → Python)

Spring BootPython Equivalentapplication.properties.envapplication.ymlconfig.yaml@Valueos.getenv()@ConfigurationPropertiesconfig dictionary / class

💡 Example Structure
project/
│
├── app.py
├── config.py
├── .env
├── config.yaml
└── requirements.txt

✅ Final takeaway
👉 Python does NOT enforce one config style
👉 But most common in real projects:
✔ .env (VERY important)
✔ config.py
✔ YAML (optional, like Spring)

## Real Project Python project structure
