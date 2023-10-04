## Basic chatbot script for interacting with GPT via command line interface. Includes ability to set chatbot "personality" via CLI argument.
## `python chatbot.py --personality="rude and snarky"`

import openai
import argparse

from dotenv import dotenv_values
config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

messages = []

# Utility functions to add color to command line text output, to easily distinguish user messages from chatbot messages
def bold(text):
	bold_start = "\033[1m"
	bold_end = "\033[0m"
	return bold_start + text + bold_end

def blue(text):
	blue_start = "\033[34m"
	blue_end = "\033[0m"
	return blue_start + text + blue_end

def red(text):
	red_start = "\033[31m"
	red_end = "\033[0m"
	return red_start + text + red_end


def main():
	parser = argparse.ArgumentParser(description="Simple command line chatbot using GPT-4")
	parser.add_argument("--personality", type=str, help="A brief summary of the chatbot's desired personality", default="friendly and helpful")
	args = parser.parse_args()

	# Set system message for GPT
	initial_prompt = f"You are a conversational chatbot. Your personality is: {args.personality}"
	messages = [{"role": "system", "content": initial_prompt}]

	while True:
		try:
			# Collect user input & pass to OpenAI API
			user_input = input(bold(blue("You: ")))
			messages.append({"role": "user", "content": user_input})
			res = openai.ChatCompletion.create(
				model="gpt-4",
				messages=messages
			)

			# Store message history so chatbot "remembers"
			messages.append(res["choices"][0]["message"].to_dict())

			# Print chatbot response
			print(bold(red("Assistant: ")), res["choices"][0]["message"]["content"])

		except KeyboardInterrupt:
			print("exiting...")
			break

if __name__ == "__main__":
	main()
