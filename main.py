from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

user_dict = dict()


# определяем функцию /start
async def start(update, context):
    # ожидание отправки сообщения по сети - нужен `await`
    text_out = (f'Привет {update.message.from_user.first_name}!{chr(10)}'
                f'Вот описание команд{chr(10)}'
                f'/add имя задачи - добавление задачи в список{chr(10)}'
                f'/list - отображение списка задач{chr(10)}'
                f'/done номер задачи - завершает задачу')
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_out)
    print(update.effective_chat.id)


# Function to add a new task
async def add_task(update, context):
    list_text = update.message.text.split("/add ", 1)
    if len(list_text) > 1:
        task_description = list_text[1]
        # проверяем id, если есть с таким, до добавляем в его список, либо создаём
        if update.effective_chat.id in user_dict.keys():
            user_dict[update.effective_chat.id].append({"description": task_description, "completed": False})
        else:
            user_dict[update.effective_chat.id] = [{"description": task_description, "completed": False}]
        print(user_dict[update.effective_chat.id])
        text_out = f"Task '{task_description}' added successfully!"
    else:
        text_out = "Invalid task description"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_out)


# Function to list all tasks
async def list_tasks(update, context):
    try:
        tasks = user_dict[update.effective_chat.id]
    except KeyError:
        tasks = []
    if not tasks:
        text_out = "No tasks yet!"
    else:
        text_out = "Your tasks:\n"
        for i, task in enumerate(tasks):
            status = "Completed." if task["completed"] else "Not completed."
            text_out += f"{i + 1}. {status} {task['description']}\n"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_out)


# Function to mark a task as completed
async def mark_done(update, context):
    try:
        tasks = user_dict[update.effective_chat.id]
        task_index = int(update.message.text.split("/done ", 1)[1]) - 1
        tasks[task_index]["completed"] = True
        user_dict[update.effective_chat.id] = tasks
        text_out = f"Task {task_index + 1} marked as completed!"
    except ValueError:
        text_out = "Please provide a valid task number."
    except IndexError:
        text_out = "Invalid task number."
    except KeyError:
        text_out = "You don't have any tasks."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_out)


if __name__ == '__main__':
    TOKEN = '7459365443:AAGzy2dL6vnY23BYcePDNdtDCqLlPNGvsjI'
    # создание экземпляра бота через `ApplicationBuilder`
    application = ApplicationBuilder().token(TOKEN).build()
    # создаем обработчик для команды '/start, /add, /list, /done'
    list_handlers = [
        CommandHandler('start', start),
        CommandHandler("add", add_task),
        CommandHandler("list", list_tasks),
        CommandHandler("done", mark_done)
    ]
    # регистрируем обработчик в приложение
    application.add_handlers(list_handlers)
    # запускаем приложение    
    application.run_polling()
