from datetime import datetime
import aiosqlite

class DataBase:
    def __init__(self, db_path: str):
        self._db_path = db_path

    async def db_request(self, query: str, param: tuple = (), fetchone: bool = False, fetchall: bool = False):
        async with aiosqlite.connect(self._db_path) as connection:
            async with connection.execute(query, param) as cursor:
                await connection.commit()
                if fetchone:
                    return await cursor.fetchone()
                elif fetchall:
                    return await cursor.fetchall()

    async def add_client(self, user_id: int, username: str, balance: int = 0):
        try:
            await self.db_request("INSERT INTO client VALUES(?, ?, ?, ?)", (user_id, balance, datetime.now(), username,))
        except aiosqlite.IntegrityError: pass

    async def add_referral(self, user_id: int, referrer_id: int = None) -> None:
        if referrer_id is not None:
            await self.db_request("INSERT INTO referral ('user_id', 'referrer_id') VALUES (?, ?)", (user_id, referrer_id,))
        else:
            await self.db_request("INSERT INTO referral ('user_id') VALUES (?)", (user_id,))

    async def client_exists(self, user_id: int, table: str = "client") -> bool:
        result = await self.db_request(f"SELECT * FROM {table} WHERE user_id = ?", (user_id,), fetchone=True)
        return bool(result)

    async def get_client_date(self, user_id: int, data: tuple) -> tuple:
        result = await self.db_request(f"SELECT {', '.join(data)} FROM client WHERE user_id = ?", (user_id,), fetchall=True)
        return result[0]

    async def update_data(self, user_id: int, data: tuple) -> None:
        await self.db_request(f"UPDATE client SET {data[0]} = ? WHERE user_id = ?", (data[1], user_id,))

    async def count_referrals(self, user_id: int) -> int:
        result = await self.db_request("SELECT COUNT(id) as count FROM referral WHERE referrer_id = ?", (user_id,),
                                       fetchone=True)
        return result[0]

    async def get_clients_reg_date(self) -> list:
        return [i[0] for i in await self.db_request("SELECT register_time FROM client", fetchall=True)]

    async def get_all_client(self) -> list:
        return [user_id[0] for user_id in await self.db_request("SELECT user_id FROM client", fetchall=True)]

    async def get_task_data(self, task_id: int = None, completed_tasks: list = None) -> dict:
        if task_id:
            result = await self.db_request("SELECT description, reward, channel_id FROM tasks WHERE task_id = ?", (task_id,), fetchall=True)
        else:
            result = await self.db_request("SELECT * FROM tasks", fetchall=True)
        if completed_tasks is not None:
            return {index: {"description": description, "reward": reward, "channel_id": channel_id} for index, description, reward, channel_id in result if index not in completed_tasks}
        return {"description": result[0][0], "reward": result[0][1], "channel_id": result[0][2]}

    async def add_task(self, description: str, reward: int, channel_id: int = None):
        await self.db_request("INSERT INTO tasks (description, reward, channel_id) VALUES(?, ?, ?)", (description, reward, channel_id,))

    async def task_exists(self, task_id: int) -> bool:
        result = await self.db_request("SELECT 1 FROM tasks WHERE task_id = ?", (task_id,), fetchone=True)
        return bool(result)

    async def delete_task(self, task_id: int):
        async with aiosqlite.connect(self._db_path) as connection:
            await connection.execute("BEGIN")
            await connection.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
            await connection.execute("DELETE FROM client_tasks WHERE task_id = ?", (task_id,))
            await connection.execute("UPDATE tasks SET task_id = task_id - 1 WHERE task_id > ?", (task_id,))
            await connection.commit()

    async def get_completed_tasks(self, user_id: int) -> list:
        result = await self.db_request("SELECT task_id FROM client_tasks WHERE user_id = ?", (user_id,), fetchall=True)
        return [i[0] for i in result]

    async def add_completed_task(self, user_id: int, task_id: int):
        try:
            await self.db_request("INSERT INTO client_tasks VALUES(?, ?)", (user_id, task_id,))
        except aiosqlite.IntegrityError: pass

    async def add_promo(self, promo: str, reward: int):
        try:
            await self.db_request("INSERT INTO promocodes VALUES(?, ?)", (promo, reward,))
        except aiosqlite.IntegrityError: pass

    async def promo_exists(self, promo: str) -> bool:
        result = await self.db_request("SELECT 1 FROM promocodes WHERE promo = ?", (promo,), fetchone=True)
        return bool(result)

    async def delete_promo(self, promo: str):
        await self.db_request("DELETE FROM promocodes WHERE promo = ?", (promo,))

    async def get_promo_reward(self, promo: str) -> int:
        result = await self.db_request("SELECT reward FROM promocodes WHERE promo = ?", (promo,), fetchone=True)
        return result[0]

    async def add_entered_promo(self, user_id: int, promo: str):
        try:
            await self.db_request("INSERT INTO client_promo VALUES (?, ?)", (user_id, promo,))
        except aiosqlite.IntegrityError: pass

    async def is_promo_used(self, user_id: int, promo: str) -> bool:
        result = await self.db_request("SELECT 1 FROM client_promo WHERE promo = ? and user_id = ?", (promo, user_id,), fetchone=True)
        return bool(result)




