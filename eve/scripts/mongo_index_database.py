"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Connect to MongoDB, index the osrsbox-db database collections.

Copyright (c) 2020, PH01L

###############################################################################
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################
"""
import os

import pymongo

class ConnectionProperties():
    def __init__(self):
        self.username = os.getenv("PROJECT_USERNAME")
        self.password = os.getenv("PROJECT_PASSWORD")
        self.port = os.getenv("MONGO_PORT")
        self.db_name = os.getenv("DATABASE_NAME")

cp = ConnectionProperties()

try:
    client = pymongo.MongoClient(f"mongodb://{cp.username}:{cp.password}@osrsbox-api-mongo:{cp.port}/{cp.db_name}")
    db = client[cp.db_name]
    print("MongoDB connection successful")
except pymongo.errors.ConnectionError as e:
    print(f"MongoDB connection error: {e}")

def main():
    # Set names of collections to index
    collection_names = [
        "items",
        "monsters",
        "prayers",
        "icons_items",
        "icons_prayers"
    ]

    # Index each collection by ID property
    for collection_name in collection_names:
        print("  > Indexing:", collection_name)
        collection = db[collection_name]
        collection.create_index("id")
        if collection_name in ["items", "monsters"]:
            collection.create_index([("name", pymongo.TEXT)], default_language="english")

if __name__ == "__main__":
    main()
