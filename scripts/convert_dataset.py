import os
import re

INPUT_DIR = "data/raw"
OUTPUT_DIR = "data/processed"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def parse_md(file_path):
    """
    Extract conversation information from markdown
    """

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    lines = text.splitlines()

    conversation_id = "unknown"
    emotion = "unknown"
    situation = ""
    dialogue_lines = []

    in_prompt = False
    in_dialogue = False

    for line in lines:

        line = line.strip()

        if line.startswith("# Conversation"):
            conversation_id = line.split()[-1]

        elif line.startswith("Emotion:"):
            emotion = line.replace("Emotion:", "").strip()

        elif line.startswith("Prompt:"):
            in_prompt = True
            continue

        elif line.startswith("## Dialogue"):
            in_prompt = False
            in_dialogue = True
            continue

        elif in_prompt:
            situation += line + " "

        elif in_dialogue and line:
            dialogue_lines.append(line)

    turns = []

    for i, msg in enumerate(dialogue_lines):

        role = "User" if i % 2 == 0 else "Assistant"
        turns.append((role, msg))

    return {
        "id": conversation_id,
        "emotion": emotion,
        "category": emotion,
        "situation": situation.strip(),
        "turns": turns
    }


def save_standardized(data):
    """
    Save standardized conversation format
    """

    emotion_folder = os.path.join(
        OUTPUT_DIR,
        data["emotion"].lower()
    )

    os.makedirs(emotion_folder, exist_ok=True)

    filename = f"chat_{data['id']}.md"

    path = os.path.join(emotion_folder, filename)

    with open(path, "w", encoding="utf-8") as f:

        f.write(f"# Chat {data['id']}\n\n")

        f.write(f"Emotion: {data['emotion']}\n")
        f.write(f"Category: {data['category']}\n\n")

        f.write("Situation:\n")
        f.write(data["situation"] + "\n\n")

        f.write("Conversation:\n\n")

        for role, msg in data["turns"]:

            msg = msg.strip().replace("\n", " ")

            f.write(f"{role}: {msg}\n\n")


def process_dataset():

    for root, dirs, files in os.walk(INPUT_DIR):

        for file in files:

            if not file.endswith(".md"):
                continue

            file_path = os.path.join(root, file)

            try:

                data = parse_md(file_path)

                save_standardized(data)

                print(f"Processed: {file}")

            except Exception as e:

                print(f"Error processing {file}: {e}")


if __name__ == "__main__":
    process_dataset()