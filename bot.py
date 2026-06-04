import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
)

# ── Setup ──────────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

BOT_TOKEN = "1094610360:AAETQKhsCWfC6QsttTCUd1JKzQrAcTLzo_8"

# ── All 30 Questions ───────────────────────────────────────────────────────────
# answer = 0 means option a, 1 means option b, 2 means option c

QUESTIONS = [
    # ── Grammar (Q1–Q15) ──────────────────────────────────────────────────────
    {
        "question": "Q1/30\n\nMy brother ________ to the gym every morning before work.",
        "options": ["go", "goes", "going"],
        "answer": 1,
    },
    {
        "question": "Q2/30\n\nI ________ my keys. Have you seen them anywhere?",
        "options": ["lost", "have lost", "lose"],
        "answer": 1,
    },
    {
        "question": "Q3/30\n\nSeldom ________ such a breathtaking sunset in this part of the country.",
        "options": ["we see", "do we see", "we have seen"],
        "answer": 1,
    },
    {
        "question": "Q4/30\n\nThere are three ________ on the kitchen table.",
        "options": ["glass", "glasses", "glass's"],
        "answer": 1,
    },
    {
        "question": "Q5/30\n\nIf I ________ more money, I would buy a house by the beach.",
        "options": ["have", "had", "would have"],
        "answer": 1,
    },
    {
        "question": "Q6/30\n\nIf he had taken the job last year, he ________ in London now.",
        "options": ["would be living", "would have lived", "will live"],
        "answer": 0,
    },
    {
        "question": "Q7/30\n\nYou like Italian food, ________ you?",
        "options": ["don't", "do", "aren't"],
        "answer": 0,
    },
    {
        "question": "Q8/30\n\nThis house ________ since the early 1990s.",
        "options": ["hasn't painted", "hasn't been painted", "wasn't paint"],
        "answer": 1,
    },
    {
        "question": "Q9/30\n\nIt is essential that he ________ the meeting on time tomorrow morning.",
        "options": ["attends", "attend", "will attend"],
        "answer": 1,
    },
    {
        "question": "Q10/30\n\nYesterday, I ________ to the park to meet my friends.",
        "options": ["go", "went", "gone"],
        "answer": 1,
    },
    {
        "question": "Q11/30\n\nI really don't mind ________ for a few more minutes if you are busy.",
        "options": ["to wait", "waiting", "wait"],
        "answer": 1,
    },
    {
        "question": "Q12/30\n\n________ by the sudden news of the accident, she sat down and cried.",
        "options": ["Shook", "Shaken", "Shaking"],
        "answer": 1,
    },
    {
        "question": "Q13/30\n\nThe English lesson starts ________ 8 o'clock sharp.",
        "options": ["in", "on", "at"],
        "answer": 2,
    },
    {
        "question": "Q14/30\n\nHe isn't answering his phone. He ________ have forgotten about our meeting.",
        "options": ["must", "should", "can"],
        "answer": 0,
    },
    {
        "question": "Q15/30\n\nBy the time the sun sets tonight, we ________ for over ten hours.",
        "options": ["will have been walking", "will be walking", "have walked"],
        "answer": 0,
    },
    # ── Vocabulary (Q16–Q30) ──────────────────────────────────────────────────
    {
        "question": "Q16/30\n\nMy favorite fruit is a sweet, red ________.",
        "options": ["apple", "table", "chair"],
        "answer": 0,
    },
    {
        "question": "Q17/30\n\nThe company had to ________ many workers due to the economic recession.",
        "options": ["turn off", "lay off", "put away"],
        "answer": 1,
    },
    {
        "question": "Q18/30\n\nThe politician's speech was full of ________, designed to mislead the public rather than inform them.",
        "options": ["candor", "rhetoric", "platitudes"],
        "answer": 1,
    },
    {
        "question": "Q19/30\n\nI always ________ water when I'm thirsty.",
        "options": ["drink", "eat", "sleep"],
        "answer": 0,
    },
    {
        "question": "Q20/30\n\nShe decided to ________ up painting as a new hobby during the lockdown.",
        "options": ["take", "bring", "make"],
        "answer": 0,
    },
    {
        "question": "Q21/30\n\nThe ancient text was so ________ that only a few scholars could decipher its meaning.",
        "options": ["ambiguous", "obsolete", "recondite"],
        "answer": 2,
    },
    {
        "question": "Q22/30\n\nHe lives in a big ________ with his family.",
        "options": ["car", "house", "school"],
        "answer": 1,
    },
    {
        "question": "Q23/30\n\nDespite repeated warnings, he tends to ________ risks in his business dealings.",
        "options": ["make", "take", "give"],
        "answer": 1,
    },
    {
        "question": "Q24/30\n\nHer ________ for the arts was evident in her vast collection of paintings and sculptures.",
        "options": ["aversion", "predilection", "indifference"],
        "answer": 1,
    },
    {
        "question": "Q25/30\n\nPlease ________ the door when you leave.",
        "options": ["open", "close", "read"],
        "answer": 1,
    },
    {
        "question": "Q26/30\n\nThe new policy aims to ________ the gap between the rich and the poor.",
        "options": ["shorten", "bridge", "cross"],
        "answer": 1,
    },
    {
        "question": "Q27/30\n\nThe dictator's regime was characterized by its ________ disregard for human rights.",
        "options": ["tacit", "flagrant", "spurious"],
        "answer": 1,
    },
    {
        "question": "Q28/30\n\nMy sister is very ________; she loves to draw and paint.",
        "options": ["sad", "tired", "creative"],
        "answer": 2,
    },
    {
        "question": "Q29/30\n\nAfter the long flight, I just wanted to go home and ________.",
        "options": ["unwind", "upset", "overload"],
        "answer": 0,
    },
    {
        "question": "Q30/30\n\nThe witness's testimony was considered ________ because it was inconsistent with the evidence.",
        "options": ["plausible", "coherent", "specious"],
        "answer": 2,
    },
]

# ── Conversation state ─────────────────────────────────────────────────────────
ASKING = 0


# ── Helpers ───────────────────────────────────────────────────────────────────
async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    idx = context.user_data["question_index"]
    q = QUESTIONS[idx]

    keyboard = [
        [InlineKeyboardButton(f"a)  {q['options'][0]}", callback_data="0")],
        [InlineKeyboardButton(f"b)  {q['options'][1]}", callback_data="1")],
        [InlineKeyboardButton(f"c)  {q['options'][2]}", callback_data="2")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.message.reply_text(
            q["question"], reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(q["question"], reply_markup=reply_markup)


# ── Handlers ──────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["score"] = 0
    context.user_data["question_index"] = 0

    await update.message.reply_text(
        "👋 Welcome to the POC English Level Test!\n\n"
        "You will answer 30 questions.\n"
        "Take your time and choose the best answer for each one.\n\n"
        "Let's begin! 🚀"
    )
    await send_question(update, context)
    return ASKING


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    idx = context.user_data["question_index"]
    selected = int(query.data)
    correct = QUESTIONS[idx]["answer"]

    if selected == correct:
        context.user_data["score"] += 1

    context.user_data["question_index"] += 1

    if context.user_data["question_index"] >= len(QUESTIONS):
        score = context.user_data["score"]
        await query.message.reply_text(
            f"🎉 Congratulations! You have completed the test!\n\n"
            f"You answered {score} out of 30 questions correctly.\n\n"
            f"Would you like a personalised consultation to find out your exact English level "
            f"and get a tailored study plan?\n\n"
            f"👉 Contact our consultant here: @asatirezaban_poshtiban"
        )
        return ConversationHandler.END

    await send_question(update, context)
    return ASKING


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASKING: [CallbackQueryHandler(handle_answer)],
        },
        fallbacks=[CommandHandler("start", start)],
        per_user=True,
        per_chat=True,
    )

    app.add_handler(conv_handler)
    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
