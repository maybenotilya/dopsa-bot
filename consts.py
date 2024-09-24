class BotCommands:
    start = "start"
    help = "help"
    register = "register"
    contacts = "contacts"
    rasp = "rasp"
    exit = "exit"


divisions_aliases = {
    "Академическая гимназия": "AGSM",
    "Биология": "BIOL",
    "Востоковедение": "ORIS",
    "Журналистика, Прикладные коммуникации": "JOUR",
    "Иностранные языки": "FL",
    "Институт развития конкуренции и антимонопольного регулирования СПбГУ": "IDAR",
    "Искусства": "ARTS",
    "История": "HIST",
    "Когнитивные исследования": "COGN",
    "Колледж физической культуры и спорта, экономики и технологии": "SC",
    "Математика и компьютерные науки": "MCSC",
    "Математика, Механика": "MATH",
    "Медицина": "MEDI",
    "Междисциплинарные программы": "INTD",
    "Международные отношения": "INTR",
    "Менеджмент": "GSOM",
    "Науки о Земле": "EARTH",
    "Онлайн-школа СПбГУ": "OLSC",
    "Педагогика": "PEDG",
    "Политология": "POLS",
    "Процессы управления": "AMCP",
    "Психология": "PSYC",
    "Свободные искусства и науки": "LIAS",
    "Социология": "SOCL",
    "Теология": "THEO",
    "Управление научных исследований": "RD",
    "Физика": "PHYS",
    "Филиал СПбГУ в Ташкенте": "TAS",
    "Филология": "LETT",
    "Философия": "PHIL",
    "Химия": "CHEM",
    "Экономика": "ECON",
    "Юриспруденция": "LAWS",
}


class Messages:
    start_message = """
    Привет! Я Dopsa Bot, бот, уведомляющий о появлении экзаменов и пересдач в расписании на timetable.spbu.ru.\nНапиши /register, чтобы зарегистрироваться или /help, чтобы узнать подробнее о том, что я могу.
    """
    help_message = """
    Я умею следующие команды:\n/start -- увидеть приветственное сообщение\n/help -- список доступных команд\n/register -- зарегистрироваться или перерегистрироваться
    """
    loading_message = "⏳ Загрузка..."
    no_register_message = "Сначала зарегистрируйтесь!"
    no_exams_message = "У вас нет экзаменов на ближайший месяц"
    month_exams_message = "Список экзаменов на ближайший месяц:"
    new_exams_messages = "❗ У вас появились новые экзамены:"
