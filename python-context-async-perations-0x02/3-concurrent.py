import asyncio
import aiosqlite

async def async_fetch_users():
    """Fetch all users from the database"""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("All users fetched:")
            for row in results:
                print(row)
            return results

async def async_fetch_older_users():
    """Fetch users older than 40 from the database"""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            print("Users older than 40 fetched:")
            for row in results:
                print(row)
            return results

async def fetch_concurrently():
    """Run both queries concurrently using asyncio.gather"""
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results

# Run the concurrent fetch
if __name__ == "__main__":
    all_users, older_users = asyncio.run(fetch_concurrently())
    print("\nConcurrent fetch completed!")
    print(f"Total users: {len(all_users)}")
    print(f"Users over 40: {len(older_users)}")