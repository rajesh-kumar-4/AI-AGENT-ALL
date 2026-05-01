# Python MongoDB CRUD Operations - Complete Debugging Guide

This guide provides step-by-step instructions to debug all CRUD (Create, Read, Update, Delete) operations with MongoDB.

## Table of Contents

1. [Prerequisites & Setup](#prerequisites--setup)
2. [MongoDB Connection Debugging](#mongodb-connection-debugging)
3. [CREATE Operation Debugging](#create-operation-debugging)
4. [READ Operation Debugging](#read-operation-debugging)
5. [UPDATE Operation Debugging](#update-operation-debugging)
6. [DELETE Operation Debugging](#delete-operation-debugging)
7. [MongoDB Compass Integration](#mongodb-compass-integration)
8. [Error Handling & Troubleshooting](#error-handling--troubleshooting)

---

## Prerequisites & Setup

### Step 1: Verify MongoDB Installation

```powershell
# Check if MongoDB is running (Windows)
Get-Service MongoDB
# Output should show: Running

# Or manually start MongoDB
mongod
```

### Step 2: Verify Python Environment

```powershell
# Activate virtual environment
venv\Scripts\activate.bat

# Verify Python and required packages
python --version
pip list | findstr pymongo
# Should output: pymongo 4.7.2 (or higher)
```

### Step 3: Setup Environment Variables

Create/update `.env` file in project root:

```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=raraphsopvt
DEBUG_MODE=True
LOG_LEVEL=DEBUG
```

### Step 4: Configure Logging for MongoDB Operations

Create `mongo_debug_config.py`:

```python
import logging
import sys

# Configure MongoDB debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('mongodb_debug.log')
    ]
)

# Enable pymongo debugging
logging.getLogger('pymongo').setLevel(logging.DEBUG)
logging.getLogger('bson').setLevel(logging.DEBUG)

debug_logger = logging.getLogger(__name__)
```

---

## MongoDB Connection Debugging

### Step 1: Test Connection

Create `test_mongo_connection.py`:

```python
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Connection test
def test_connection():
    try:
        logger.info("🔌 Attempting to connect to MongoDB...")

        client = MongoClient(
            "mongodb://localhost:27017",
            serverSelectionTimeoutMS=5000
        )

        # Verify connection by pinging server
        logger.info("📍 Pinging MongoDB server...")
        client.admin.command('ping')

        logger.info("✅ MongoDB connection successful!")
        logger.info(f"🗂️ Available databases: {client.list_database_names()}")

        return client

    except ServerSelectionTimeoutError as e:
        logger.error(f"❌ MongoDB server not reachable: {e}")
        raise
    except ConnectionFailure as e:
        logger.error(f"❌ Connection failed: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        raise

if __name__ == "__main__":
    try:
        client = test_connection()
        client.close()
    except Exception as e:
        print(f"Connection test failed: {e}")
```

### Step 2: Run Connection Test

```powershell
python test_mongo_connection.py
```

Expected output:

```
🔌 Attempting to connect to MongoDB...
📍 Pinging MongoDB server...
✅ MongoDB connection successful!
🗂️ Available databases: ['admin', 'config', 'local', 'raraphsopvt']
```

---

## CREATE Operation Debugging

### Step 1: Debug CREATE with Logging

Create `debug_create.py`:

```python
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import logging
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = MongoClient("mongodb://localhost:27017")
db = client["raraphsopvt"]
tasks_collection = db.tasks

def create_task_debug(title: str, description: str) -> str:
    try:
        logger.info(f"➕ Creating task with title: '{title}'")

        document = {
            "title": title.strip(),
            "description": description.strip(),
            "completed": False,
            "created_at": datetime.utcnow().isoformat(),
        }

        logger.debug(f"📋 Document to insert: {json.dumps(document, indent=2, default=str)}")

        # Insert document
        logger.info("💾 Inserting document into collection...")
        result = tasks_collection.insert_one(document)

        inserted_id = str(result.inserted_id)
        logger.info(f"✅ Task created successfully!")
        logger.info(f"🆔 Inserted ID: {inserted_id}")

        # Verify insertion by reading back
        logger.info("🔍 Verifying insertion...")
        verify_doc = tasks_collection.find_one({"_id": result.inserted_id})
        logger.debug(f"📝 Verified document: {json.dumps(verify_doc, indent=2, default=str)}")

        return inserted_id

    except PyMongoError as e:
        logger.error(f"❌ MongoDB error during CREATE: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        raise

if __name__ == "__main__":
    try:
        # Test CREATE
        task_id = create_task_debug(
            "Learn MongoDB Debugging",
            "Master CRUD operations with comprehensive logging"
        )
        print(f"\n✨ Created task ID: {task_id}")

    except Exception as e:
        print(f"❌ Operation failed: {e}")
    finally:
        client.close()
```

### Step 2: Run CREATE Debug Test

```powershell
python debug_create.py
```

Expected output:

```
➕ Creating task with title: 'Learn MongoDB Debugging'
📋 Document to insert: { "title": "Learn MongoDB Debugging", ... }
💾 Inserting document into collection...
✅ Task created successfully!
🆔 Inserted ID: 507f1f77bcf86cd799439011
🔍 Verifying insertion...
📝 Verified document: { "_id": "507f...", "title": "Learn MongoDB Debugging", ... }
```

---

## READ Operation Debugging

### Step 1: Debug READ with Multiple Scenarios

Create `debug_read.py`:

```python
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError
import logging
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = MongoClient("mongodb://localhost:27017")
db = client["raraphsopvt"]
tasks_collection = db.tasks

def read_task_by_id_debug(task_id: str) -> dict | None:
    try:
        logger.info(f"🔍 Reading task with ID: {task_id}")

        # Validate ObjectId format
        try:
            object_id = ObjectId(task_id)
            logger.debug(f"✓ Valid ObjectId format")
        except Exception as e:
            logger.error(f"❌ Invalid ObjectId format: {e}")
            raise

        # Query database
        logger.info("📊 Querying database...")
        document = tasks_collection.find_one({"_id": object_id})

        if document:
            logger.info(f"✅ Task found!")
            logger.debug(f"📝 Document content: {json.dumps(document, indent=2, default=str)}")
            return document
        else:
            logger.warning(f"⚠️ Task with ID '{task_id}' not found in collection")
            return None

    except PyMongoError as e:
        logger.error(f"❌ MongoDB error during READ: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        raise

def read_all_tasks_debug() -> list:
    try:
        logger.info("📚 Reading all tasks from collection")

        # Get count
        count = tasks_collection.count_documents({})
        logger.info(f"📊 Total documents in collection: {count}")

        # Fetch all with sorting
        logger.info("⬇️ Fetching documents sorted by created_at (descending)...")
        documents = list(tasks_collection.find().sort("created_at", -1))

        logger.info(f"✅ Retrieved {len(documents)} tasks")

        for idx, doc in enumerate(documents):
            logger.debug(f"Task {idx + 1}: {doc['title']} (ID: {doc['_id']})")

        return documents

    except PyMongoError as e:
        logger.error(f"❌ MongoDB error during READ ALL: {e}")
        raise

def read_tasks_by_filter_debug(filter_dict: dict) -> list:
    try:
        logger.info(f"🔎 Reading tasks with filter: {filter_dict}")

        count = tasks_collection.count_documents(filter_dict)
        logger.info(f"📊 Matching documents: {count}")

        documents = list(tasks_collection.find(filter_dict))

        logger.info(f"✅ Retrieved {len(documents)} matching tasks")

        return documents

    except PyMongoError as e:
        logger.error(f"❌ MongoDB error during filtered READ: {e}")
        raise

if __name__ == "__main__":
    try:
        # Read all tasks
        logger.info("=" * 50)
        logger.info("TEST 1: Read All Tasks")
        logger.info("=" * 50)
        all_tasks = read_all_tasks_debug()

        if all_tasks:
            # Test read by ID
            logger.info("\n" + "=" * 50)
            logger.info("TEST 2: Read Task by ID")
            logger.info("=" * 50)
            first_task_id = str(all_tasks[0]['_id'])
            read_task_by_id_debug(first_task_id)

            # Test filtered read
            logger.info("\n" + "=" * 50)
            logger.info("TEST 3: Read Completed Tasks")
            logger.info("=" * 50)
            completed_tasks = read_tasks_by_filter_debug({"completed": True})
            logger.info(f"Found {len(completed_tasks)} completed tasks")

    except Exception as e:
        print(f"❌ Operation failed: {e}")
    finally:
        client.close()
```

### Step 2: Run READ Debug Test

```powershell
python debug_read.py
```

---

## UPDATE Operation Debugging

### Step 1: Debug UPDATE with Validation

Create `debug_update.py`:

```python
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError
import logging
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = MongoClient("mongodb://localhost:27017")
db = client["raraphsopvt"]
tasks_collection = db.tasks

def update_task_debug(task_id: str, update_data: dict) -> bool:
    try:
        logger.info(f"✏️ Updating task with ID: {task_id}")
        logger.debug(f"📝 Update data: {json.dumps(update_data, indent=2, default=str)}")

        # Validate ObjectId
        try:
            object_id = ObjectId(task_id)
        except Exception as e:
            logger.error(f"❌ Invalid ObjectId format: {e}")
            raise

        # Fetch document BEFORE update
        logger.info("📸 Fetching document BEFORE update...")
        before_doc = tasks_collection.find_one({"_id": object_id})

        if not before_doc:
            logger.warning(f"⚠️ Task not found. Cannot update non-existent task.")
            return False

        logger.debug(f"Before: {json.dumps(before_doc, indent=2, default=str)}")

        # Perform update
        logger.info("🔄 Executing update...")
        result = tasks_collection.update_one(
            {"_id": object_id},
            {"$set": update_data}
        )

        logger.info(f"📊 Update result:")
        logger.info(f"   - Matched documents: {result.matched_count}")
        logger.info(f"   - Modified documents: {result.modified_count}")

        if result.modified_count == 0:
            logger.warning("⚠️ No documents were modified. Check your filter.")
            return False

        # Fetch document AFTER update for verification
        logger.info("📸 Fetching document AFTER update...")
        after_doc = tasks_collection.find_one({"_id": object_id})
        logger.debug(f"After: {json.dumps(after_doc, indent=2, default=str)}")

        # Highlight changes
        logger.info("🔄 Changes made:")
        for key, value in update_data.items():
            logger.info(f"   {key}: {before_doc.get(key)} → {after_doc.get(key)}")

        logger.info("✅ Task updated successfully!")
        return True

    except PyMongoError as e:
        logger.error(f"❌ MongoDB error during UPDATE: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        raise

def increment_field_debug(task_id: str, field: str, increment_by: int = 1) -> bool:
    try:
        logger.info(f"➕ Incrementing {field} by {increment_by}")

        object_id = ObjectId(task_id)

        logger.info("🔄 Executing increment operation...")
        result = tasks_collection.update_one(
            {"_id": object_id},
            {"$inc": {field: increment_by}}
        )

        logger.info(f"✅ Increment completed. Modified: {result.modified_count}")
        return result.modified_count > 0

    except Exception as e:
        logger.error(f"❌ Error during increment: {e}")
        raise

if __name__ == "__main__":
    try:
        # Get first task
        first_task = tasks_collection.find_one()

        if first_task:
            task_id = str(first_task['_id'])

            # Test UPDATE
            logger.info("=" * 50)
            logger.info("TEST: Update Task")
            logger.info("=" * 50)

            update_task_debug(task_id, {
                "completed": True,
                "description": "Updated via debug script"
            })

    except Exception as e:
        print(f"❌ Operation failed: {e}")
    finally:
        client.close()
```

### Step 2: Run UPDATE Debug Test

```powershell
python debug_update.py
```

---

## DELETE Operation Debugging

### Step 1: Debug DELETE with Safety Checks

Create `debug_delete.py`:

```python
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError
import logging
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = MongoClient("mongodb://localhost:27017")
db = client["raraphsopvt"]
tasks_collection = db.tasks

def delete_task_debug(task_id: str, force: bool = False) -> bool:
    try:
        logger.info(f"🗑️ Attempting to delete task with ID: {task_id}")

        # Validate ObjectId
        try:
            object_id = ObjectId(task_id)
        except Exception as e:
            logger.error(f"❌ Invalid ObjectId format: {e}")
            raise

        # Fetch document BEFORE deletion (safety check)
        logger.info("📸 Fetching document BEFORE deletion...")
        doc_before = tasks_collection.find_one({"_id": object_id})

        if not doc_before:
            logger.warning(f"⚠️ Task not found. Nothing to delete.")
            return False

        logger.debug(f"Document to delete: {json.dumps(doc_before, indent=2, default=str)}")

        # Confirmation for safety
        if not force:
            logger.warning(f"⚠️ CONFIRMATION REQUIRED")
            logger.warning(f"   Title: {doc_before.get('title')}")
            logger.warning(f"   ID: {task_id}")

            confirm = input("\n⚠️ Are you sure you want to delete this task? (yes/no): ")
            if confirm.lower() != "yes":
                logger.info("❌ Deletion cancelled by user")
                return False

        # Perform deletion
        logger.info("🔄 Executing deletion...")
        result = tasks_collection.delete_one({"_id": object_id})

        logger.info(f"📊 Deletion result:")
        logger.info(f"   - Deleted documents: {result.deleted_count}")

        if result.deleted_count == 0:
            logger.warning("⚠️ No documents were deleted")
            return False

        # Verify deletion
        logger.info("🔍 Verifying deletion...")
        doc_after = tasks_collection.find_one({"_id": object_id})

        if doc_after is None:
            logger.info("✅ Task deleted successfully!")
            return True
        else:
            logger.error("❌ Deletion verification failed. Document still exists.")
            return False

    except PyMongoError as e:
        logger.error(f"❌ MongoDB error during DELETE: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        raise

def delete_multiple_debug(filter_dict: dict) -> int:
    try:
        logger.info(f"🗑️ Deleting multiple documents matching filter: {filter_dict}")

        # Count matching documents
        count = tasks_collection.count_documents(filter_dict)
        logger.info(f"📊 Documents matching filter: {count}")

        if count == 0:
            logger.warning("⚠️ No documents match the filter")
            return 0

        # Show preview
        logger.warning(f"⚠️ About to delete {count} document(s)")
        confirm = input("Continue? (yes/no): ")

        if confirm.lower() != "yes":
            logger.info("❌ Deletion cancelled")
            return 0

        # Perform deletion
        result = tasks_collection.delete_many(filter_dict)
        logger.info(f"✅ Deleted {result.deleted_count} documents")

        return result.deleted_count

    except Exception as e:
        logger.error(f"❌ Error during multi-delete: {e}")
        raise

if __name__ == "__main__":
    try:
        # Note: Uncomment to test deletion
        # first_task = tasks_collection.find_one()
        # if first_task:
        #     delete_task_debug(str(first_task['_id']), force=False)

        logger.info("⚠️ DELETE test scripts are commented out for safety.")
        logger.info("Uncomment the main block to test deletion operations.")

    except Exception as e:
        print(f"❌ Operation failed: {e}")
    finally:
        client.close()
```

### Step 2: Run DELETE Debug Test

```powershell
python debug_delete.py
```

---

## MongoDB Compass Integration

### Step 1: Install MongoDB Compass

- Download from: https://www.mongodb.com/products/tools/compass
- Install and launch

### Step 2: Connect to MongoDB

```
Connection String: mongodb://localhost:27017
Database: raraphsopvt
```

### Step 3: Visual Debugging in Compass

1. **View Documents**: Click on `tasks` collection
2. **Filter Documents**: Use filter bar
   ```json
   { "completed": true }
   ```
3. **Edit Documents**: Click pencil icon to modify
4. **Add Documents**: Click "+" to insert new document
5. **Delete Documents**: Click trash icon
6. **View Schema**: Check schema tab for structure analysis
7. **Aggregation**: Use aggregation pipeline for complex queries

### Step 4: Export/Import Data

```powershell
# Export collection
mongoexport --uri "mongodb://localhost:27017/raraphsopvt" --collection tasks --out tasks_backup.json

# Import collection
mongoimport --uri "mongodb://localhost:27017/raraphsopvt" --collection tasks --file tasks_backup.json
```

---

## Error Handling & Troubleshooting

### Common Errors & Solutions

#### 1. **Connection Refused**

```
Error: [Errno 10061] No connection could be made
```

**Solution**:

```powershell
# Check if MongoDB is running
Get-Service MongoDB

# Start MongoDB
mongod

# Or start MongoDB service
Start-Service MongoDB
```

#### 2. **Invalid ObjectId**

```
Error: invalid ObjectId hex string: '...'
```

**Solution**:

```python
from bson.objectid import ObjectId

try:
    object_id = ObjectId(task_id)
except Exception as e:
    logger.error(f"Invalid format: {e}")
    # Validate format before use
```

#### 3. **Authentication Failure**

```
Error: Authentication failed
```

**Solution**:

```python
# Use correct URI with credentials
client = MongoClient(
    f"mongodb://{username}:{password}@localhost:27017/raraphsopvt"
)
```

#### 4. **Duplicate Key Error**

```
Error: E11000 duplicate key error
```

**Solution**:

```python
# Create unique index
tasks_collection.create_index("email", unique=True)

# Handle error
try:
    result.insert_one(document)
except DuplicateKeyError:
    logger.error("Document with this key already exists")
```

#### 5. **Session Timeout**

```
Error: No servers chosen by WithConnectionPool
```

**Solution**:

```python
# Increase timeout and add retry logic
client = MongoClient(
    "mongodb://localhost:27017",
    serverSelectionTimeoutMS=10000,  # Increase timeout
    retryWrites=True
)
```

### Debug Checklist

- [ ] MongoDB service is running
- [ ] Python environment is activated
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Environment variables in `.env` are set correctly
- [ ] Database and collection exist in MongoDB
- [ ] ObjectId format is valid for queries
- [ ] Connection string is correct
- [ ] Logging is configured properly
- [ ] Error messages are captured in logs

### Enable Full Debug Mode

Create `enable_debug.py`:

```python
import logging
import sys

# Enable all debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    stream=sys.stdout
)

# Enable pymongo debug logging
logging.getLogger('pymongo').setLevel(logging.DEBUG)
logging.getLogger('bson').setLevel(logging.DEBUG)

# Enable command logging
import pymongo
pymongo.set_debug_mode(True)

print("✅ Debug mode enabled. All operations will be logged.")
```

---

## Complete Integration Test

Create `complete_crud_test.py` to test all operations together:

```python
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
import logging
import json

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

client = MongoClient("mongodb://localhost:27017")
db = client["raraphsopvt"]
tasks = db.tasks

def full_crud_test():
    logger.info("\n" + "=" * 60)
    logger.info("COMPLETE CRUD TEST")
    logger.info("=" * 60)

    try:
        # CREATE
        logger.info("\n1️⃣ CREATE OPERATION")
        task_doc = {
            "title": "CRUD Test Task",
            "description": "Testing all operations",
            "completed": False,
            "created_at": datetime.utcnow().isoformat()
        }
        result = tasks.insert_one(task_doc)
        task_id = result.inserted_id
        logger.info(f"✅ Created: {task_id}")

        # READ
        logger.info("\n2️⃣ READ OPERATION")
        read_doc = tasks.find_one({"_id": task_id})
        logger.info(f"✅ Read: {read_doc['title']}")

        # UPDATE
        logger.info("\n3️⃣ UPDATE OPERATION")
        update_result = tasks.update_one(
            {"_id": task_id},
            {"$set": {"completed": True}}
        )
        logger.info(f"✅ Updated: {update_result.modified_count} doc(s)")

        # READ after UPDATE
        logger.info("\n4️⃣ READ AFTER UPDATE")
        updated_doc = tasks.find_one({"_id": task_id})
        logger.info(f"✅ Completed: {updated_doc['completed']}")

        # DELETE
        logger.info("\n5️⃣ DELETE OPERATION")
        delete_result = tasks.delete_one({"_id": task_id})
        logger.info(f"✅ Deleted: {delete_result.deleted_count} doc(s)")

        # VERIFY DELETION
        logger.info("\n6️⃣ VERIFY DELETION")
        verify_doc = tasks.find_one({"_id": task_id})
        if verify_doc is None:
            logger.info("✅ Confirmed: Document deleted successfully")

        logger.info("\n" + "=" * 60)
        logger.info("✨ ALL TESTS PASSED!")
        logger.info("=" * 60 + "\n")

    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    full_crud_test()
```

### Run Full Test

```powershell
python complete_crud_test.py
```

---

## Quick Reference Commands

```powershell
# Start MongoDB
mongod

# Connect to MongoDB shell
mongosh

# View databases
show dbs

# Use database
use raraphsopvt

# View collections
show collections

# Count documents
db.tasks.countDocuments()

# Find all
db.tasks.find()

# Find with filter
db.tasks.find({ "completed": true })

# Insert
db.tasks.insertOne({ "title": "Test", "completed": false })

# Update
db.tasks.updateOne({ "_id": ObjectId("...") }, { $set: { "completed": true } })

# Delete
db.tasks.deleteOne({ "_id": ObjectId("...") })
```

---

## Summary

This guide covers:

- ✅ Connection debugging
- ✅ CREATE operations with logging
- ✅ READ operations (single, multiple, filtered)
- ✅ UPDATE operations with before/after verification
- ✅ DELETE operations with safety checks
- ✅ MongoDB Compass integration
- ✅ Error handling and troubleshooting
- ✅ Complete CRUD test workflow

Use these debugging techniques to develop robust MongoDB CRUD applications!
