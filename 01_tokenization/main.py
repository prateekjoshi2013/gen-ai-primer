import tiktoken

enc=tiktoken.encoding_for_model("gpt-4o")
tokens=enc.encode("Hello, world!")
print(f"Number of tokens: {len(tokens)}")
print(f"Tokens: {tokens}")
decoded=enc.decode(tokens)
print(f"Decoded text: {decoded}")