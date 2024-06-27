from dotenv import load_dotenv
import os
load_dotenv()

# просто конфиг, мне нечего сказать, на самом деле можно было бы перенести в main возможно TODO
api_id = os.getenv('ID')
api_hash = os.getenv('HASH')
bot_token = os.getenv('TOKEN')